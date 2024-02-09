# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import logging
import boto3

from dataclasses import dataclass
from os import path

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


@dataclass
class AwsS3File:
    key: str
    filename: str
    basename: str
    size: int


class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    server_type = fields.Selection(
        selection_add=[
            ('aws_ses_s3', 'AWS SES S3 Authentication'),
        ],
        ondelete={
            'aws_ses_s3': 'set default',
        }
    )

    aws_ses_s3_access_id = fields.Char(
        string='Access ID',
        groups='base.group_system',
        copy=False,
    )

    aws_ses_s3_access_secret = fields.Char(
        string='Access Secret',
        groups='base.group_system',
        copy=False,
    )

    aws_ses_s3_session_token = fields.Char(
        string='Session Token',
        groups='base.group_system',
        copy=False,
    )

    aws_ses_s3_bucket = fields.Char(
        string='AWS S3 Bucket',
        groups='base.group_system',
        copy=False,
        help='The AWS S3 Bucket name to store email files',
    )

    aws_ses_s3_region = fields.Char(
        string='AWS S3 Region',
        groups='base.group_system',
        copy=False,
        help='The AWS S3 Region used for the authentication',
    )

    aws_ses_s3_object_prefix = fields.Char(
        string='AWS S3 Object Prefix',
        groups='base.group_system',
        copy=False,

        help='The prefix of object key to store email file in S3 Bucket',
    )

    def _compute_server_type_info(self):
        aws_ses_s3_servers = self.filtered(lambda server: server.server_type == 'aws_ses_s3')
        aws_ses_s3_servers.server_type_info = _('Connect your AWS account with the AWS Credentials information.')
        super(FetchmailServer, self - aws_ses_s3_servers)._compute_server_type_info()

    @api.onchange('server_type', 'is_ssl', 'object_id')
    def onchange_server_type(self):
        """Set the default configuration for AWS SES Inbound server."""
        if self.server_type == 'aws_ses_s3':
            self.server = False
            self.is_ssl = False
            self.port = 0
            self.user = False
            self.password = False
        else:
            self.aws_ses_s3_access_id = False
            self.aws_ses_s3_access_secret = False
            self.aws_ses_s3_bucket = False
            self.aws_ses_s3_object_prefix = False
            super(FetchmailServer, self).onchange_server_type()

    def _get_connection_type(self):
        """Return which connection must be used for this mail server (IMAP or POP).
        """
        self.ensure_one()
        return 'aws_ses_s3' if self.server_type == 'aws_ses_s3' else super()._get_connection_type()

    def connect(self, allow_archived=False):
        # Connection variable in parent method is not defined if connection type is not defined.
        try:
            connection = super(FetchmailServer, self).connect(allow_archived)
        except Exception as err:
            connection = False
            if not isinstance(err, UnboundLocalError):
                raise err

        if not connection and self._get_connection_type() == 'aws_ses_s3':
            self._get_s3_email_files()

        return connection

    def fetch_mail(self):
        """ WARNING: meant for cron usage only - will commit() after each email! """
        aws_servers = self.filtered(lambda fms: fms._get_connection_type() == 'aws_ses_s3')
        other_servers = self.filtered(lambda fms: fms._get_connection_type() != 'aws_ses_s3')

        # Fetch other email servers
        res = super(FetchmailServer, other_servers).fetch_mail()

        # Fetch AWS SES S3 email servers
        additionnal_context = {
            'fetchmail_cron_running': True
        }
        MailThread = self.env['mail.thread']
        for server in aws_servers:
            _logger.info('start checking for new emails on %s server %s', server.server_type, server.name)
            additionnal_context['default_fetchmail_server_id'] = server.id
            count, failed = 0, 0
            s3_client = self._get_s3_client()

            try:
                while True:
                    failed_in_loop = 0
                    num = 0
                    files = self._get_s3_email_files()

                    if files:
                        for file in files:
                            try:
                                num += 1

                                res_message = s3_client.get_object(Bucket=self.aws_ses_s3_bucket, Key=file.key)
                                message = res_message['Body'].read()

                                MailThread\
                                    .with_context(**additionnal_context)\
                                    .message_process(
                                        server.object_id.model,
                                        message,
                                        save_original=server.original,
                                        strip_attachments=(not server.attach)
                                    )

                                s3_client.delete_object(Bucket=self.aws_ses_s3_bucket, Key=file.key)
                            except Exception:
                                _logger.info(
                                    'Failed to process mail from %s server %s.',
                                    server.server_type,
                                    server.name,
                                    exc_info=True
                                )
                                failed += 1
                                failed_in_loop += 1

                        _logger.info(
                            'Fetched %d email(s) on %s server %s; %d succeeded, %d failed.',
                            num,
                            server.server_type,
                            server.name,
                            (num - failed_in_loop),
                            failed_in_loop
                        )
                    else:
                        break
            except Exception:
                _logger.info(
                    'General failure when trying to fetch mail from %s server %s.',
                    server.server_type,
                    server.name,
                    exc_info=True
                )

        return res

    def _get_s3_email_files(self) -> list[AwsS3File]:
        self.ensure_one()

        s3_client = self._get_s3_client()
        files = []

        objects = s3_client.list_objects(
            Bucket=self.aws_ses_s3_bucket,
            Delimiter='/',
            Prefix=self.aws_ses_s3_object_prefix.strip('/') + '/' if self.aws_ses_s3_object_prefix else '',
        ).get('Contents', [])

        for obj in objects:
            key = obj.get('Key')
            files.append(AwsS3File(key, path.basename(key), path.dirname(key), obj.get('Size')))

        return files

    def _get_s3_client(self):
        self.ensure_one()

        return boto3.client(
            's3',
            aws_access_key_id=self.aws_ses_s3_access_id or '',
            aws_secret_access_key=self.aws_ses_s3_access_secret or '',
            region_name=self.aws_ses_s3_region or '',
        )
