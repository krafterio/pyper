# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from odoo import models
from PyPDF2 import PdfFileReader, PdfFileWriter
import io
import base64

class IrActionReport(models.AbstractModel):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        result = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)
        
        pdf_name = self._get_report(report_ref).report_name
        if pdf_name == 'pyper_custom_report.custom_report_template':
            sales_orders = self.env['sale.order'].browse(res_ids)
            for order in sales_orders:
                main_pdf_content, _ = self.env['ir.actions.report']._get_report_from_name('sale.report_saleorder')._render_qweb_pdf('sale.report_saleorder', [order.id])
                initial_stream = io.BytesIO(main_pdf_content)
                template_pdf = order.template_attachment_id
                if not template_pdf or not template_pdf.datas:
                    writer = PdfFileWriter()
                    self._add_pages_to_writer(writer, initial_stream.getvalue())
                    result[order.id].update({'stream': initial_stream})
                    continue

                writer = PdfFileWriter()
                self._add_pages_to_writer(writer, initial_stream.getvalue())
                
                self._add_pages_to_writer(writer, base64.b64decode(template_pdf.datas))

                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    stream = io.BytesIO(_buffer.getvalue())
                
                result[order.id].update({'stream': stream})
        
        return result

    def _add_pages_to_writer(self, writer, document):
        reader = PdfFileReader(io.BytesIO(document), strict=False)
        for page_id in range(0, reader.getNumPages()):
            page = reader.getPage(page_id)
            writer.addPage(page)
