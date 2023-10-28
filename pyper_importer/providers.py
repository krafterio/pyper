# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api

from abc import ABC, abstractmethod

from datetime import datetime

import copy


class ExtractedItem:
    def __init__(self, origin_data: dict, payload=None):
        self.origin_data = origin_data
        self.payload = payload if payload is not None else {}


class TransformedItem:
    def __init__(self, origin_data: dict, transformed_data: dict, payload=None, skipped: bool = False):
        self.origin_data = origin_data
        self.transformed_data = transformed_data
        self.payload = payload if payload is not None else {}
        self.skipped = skipped


class BaseProvider:
    """Base of Pyper Importer Provider.
    """

    def __init__(self, env: api.Environment, job):
        """
        :param job (Model<pyper.queue.job>): the queue job
        """
        self.env = env
        self.job = job
        self.importer = job.importer_provider_id

    @abstractmethod
    def extract(self, offset: int, started_date: datetime) -> list[ExtractedItem]:
        pass

    @abstractmethod
    def transform(self, extracted_items: list[ExtractedItem]) -> list[TransformedItem]:
        pass

    @abstractmethod
    def load(self, transformed_items: list[TransformedItem]):
        pass


class BatchableProvider(BaseProvider, ABC):
    batch_size: int = 100


class AllowUpdateConfigurableProvider(BaseProvider, ABC):
    pass


class ExtractByOdooModelIdentifiersHelper(BatchableProvider, ABC):
    """
    Helper to iterate into an Odoo model (target) to retrieve the external identifiers and extract all data from remote
    database (origin) using these identifiers.
    This helper batch the Odoo models and search the remote data by the origin identifier. If data is found,
    the Odoo model instance is updated with the transformed data.
    """

    @property
    @abstractmethod
    def target_model(self) -> str:
        pass

    @property
    @abstractmethod
    def target_identifier(self) -> str:
        pass

    @property
    @abstractmethod
    def origin_identifier(self) -> str:
        pass

    @property
    def extract_get_identifiers_order(self) -> str:
        return ''

    def _extract_get_identifiers_domain(self, started_date: datetime) -> list:
        return [(self.target_identifier, '!=', False)]

    def extract(self, offset: int, started_date: datetime) -> list[ExtractedItem]:
        # Create map between record id and identifier
        map_identifiers = {}
        list_identifiers = []
        identifiers = self.env[self.target_model].search_read(
            domain=self._extract_get_identifiers_domain(started_date),
            order=self.extract_get_identifiers_order,
            fields=['id', self.target_identifier],
            limit=self.batch_size,
            offset=offset
        )

        for identifier in identifiers:
            map_identifiers[identifier['id']] = identifier[self.target_identifier]
            list_identifiers.append(identifier[self.target_identifier])

        # Extract and create map between identifier and origin item
        map_res = {}
        origin_data_list = self._extract_by_identifiers(list_identifiers)

        for origin_data in origin_data_list:
            map_res[origin_data[self.origin_identifier]] = origin_data

        # Create list of record and origin data
        result = []
        for record_id in map_identifiers.keys():
            record_identifier = map_identifiers[record_id]
            result.append(ExtractedItem(
                map_res[record_identifier] if record_identifier in map_res else {},
                {
                    'target_model': self.target_model,
                    'target_id': record_id,
                    'target_identifier': self.target_identifier,
                    'identifier': record_identifier,
                    'started_date': started_date,
                    'origin_found': record_identifier in map_res,
                    'origin_identifier': self.origin_identifier,
                }
            ))

        return result

    @abstractmethod
    def _extract_by_identifiers(self, identifiers: list[str]) -> list[dict]:
        pass


class TransformHelper(BaseProvider, ABC):
    def transform(self, extracted_items: list[ExtractedItem]) -> list[TransformedItem]:
        transformed_items = []

        for extracted_item in extracted_items:
            origin_data = extracted_item.origin_data

            try:
                transformed_item = self._transform_item(origin_data, {**extracted_item.payload})

                if not transformed_item.skipped:
                    transformed_items.append(transformed_item)
                elif transformed_item.payload.get('log_skipped', True):
                    self.job.log_skip(name='TransformItemSkip', auto_commit=True)
            except Exception as err:
                origin_identifier = self.origin_identifier if hasattr(self, 'origin_identifier') else 'id'
                self.importer._except_load_exception(self.job, err, origin_data, origin_identifier)

        return transformed_items

    @abstractmethod
    def _transform_item(self, origin_data: dict, payload: dict) -> TransformedItem:
        pass


class LoadHelper(BaseProvider, ABC):
    @property
    @abstractmethod
    def target_model(self) -> str:
        pass

    @property
    @abstractmethod
    def target_identifier(self) -> str:
        pass

    @property
    @abstractmethod
    def origin_identifier(self) -> str:
        pass

    @property
    def use_external_id(self) -> bool:
        return False

    @property
    def external_identifier_module(self) -> str:
        return 'pyper_importer'

    def build_external_id_name(self, item: dict) -> str:
        return (self.target_model.replace('.', '_')
                + '__'
                + str(item.get(self.origin_identifier)))

    def build_external_id(self, item: dict) -> str:
        return (self.external_identifier_module
                + '.'
                + self.build_external_id_name(item))

    def load(self, transformed_items: list[TransformedItem]):
        for transformed_item in transformed_items:
            if self.job.importer_stop_required:
                break

            item = transformed_item.transformed_data

            try:
                if self.use_external_id:
                    existing_item = self.env.ref(self.build_external_id(item), False)

                    if existing_item is None:
                        existing_item = self.env[self.target_model]
                else:
                    existing_item = self.importer.find_record(
                        self.target_model,
                        self.target_identifier,
                        item.get(self.origin_identifier)
                    )
                loaded_id = self._load_item(transformed_item, existing_item, existing_item.id is False)

                if loaded_id != 0:
                    if self.use_external_id:
                        self.env['ir.model.data'].create({
                            'name': self.build_external_id_name(item),
                            'model': self.target_model,
                            'module': self.external_identifier_module,
                            'res_id': loaded_id,
                        })

                    self.job.log_success(
                        auto_commit=True,
                        payload=self.importer._create_log_payload(item, self.origin_identifier, existing_item)
                    )
                else:
                    self.job.log_skip(
                        auto_commit=True,
                        payload=self.importer._create_log_payload(item, self.origin_identifier, existing_item)
                    )

            except Exception as err:
                self.importer._except_load_exception(self.job, err, item, self.origin_identifier)

    @abstractmethod
    def _load_item(self, transformed_item: TransformedItem, existing_item, is_create: bool) -> int:
        """
        :param transformed_item: TransformedItem
        :param existing_item (Model<*>): the existing record
        :return int: the item id if the item is loaded or 0 if not loaded (skipped)
        """
        pass


class LoadByOdooExternalIdentifierHelper(LoadHelper, ABC):
    @property
    def use_external_id(self) -> bool:
        return True


class LoadByOdooModelIdentifiersHelper(BaseProvider, ABC):
    def load(self, transformed_items: list[TransformedItem]):
        for transformed_item in transformed_items:
            if self.job.importer_stop_required:
                break

            origin_identifier = transformed_item.payload.get('origin_identifier')
            target_model = transformed_item.payload.get('target_model')
            record_id = transformed_item.payload.get('target_id')
            origin_found = transformed_item.payload.get('origin_found', False)
            item = transformed_item.transformed_data

            existing_item = self.env[target_model].browse(record_id)

            try:
                loaded_id = 0

                if existing_item:
                    loaded_id = self._load_item(transformed_item, existing_item, origin_found)

                if loaded_id != 0:
                    self.job.log_success(
                        auto_commit=True,
                        payload=self.importer._create_log_payload(item, origin_identifier, existing_item)
                    )
                else:
                    self.job.log_skip(
                        auto_commit=True,
                        payload=self.importer._create_log_payload(item, origin_identifier, existing_item)
                    )
            except Exception as err:
                self.importer._except_load_exception(self.job, err, item, origin_identifier, existing_item)

    @abstractmethod
    def _load_item(self, transformed_item: TransformedItem, existing_item, origin_found: bool) -> int:
        """
        :param transformed_item: TransformedItem
        :param existing_item (Model<*>): the existing record
        :return int: the item id if the item is loaded or 0 if not loaded (skipped)
        """
        pass


def convert_extracted_items_to_transformed_items(extracted_items: list[ExtractedItem]) -> list[TransformedItem]:
    transformed_items = []

    for extracted_item in extracted_items:
        transformed_items.append(convert_extracted_item_to_transformed_item(extracted_item))

    return transformed_items


def convert_extracted_item_to_transformed_item(extracted_item: ExtractedItem) -> TransformedItem:
    return TransformedItem(
        extracted_item.origin_data,
        copy.deepcopy(extracted_item.origin_data),
        {**extracted_item.payload}
    )
