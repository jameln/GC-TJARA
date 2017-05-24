from odoo import api, models

class ParticularReport(models.AbstractModel):
    _name = 'report.gctjara_facturevente.report_facturevente'
    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('gc-tjara.report_facturevente')
        docargs = {
            'doc_ids': docids,
            'doc_model': 'gctjara.facturevente',
            'docs': self,
        }
        return report_obj.render('gc-tjara.report_facturevente', docargs)