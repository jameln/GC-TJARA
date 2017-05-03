from odoo import api, models

class ParticularReport(models.AbstractModel):
    _name = 'report.gctjara_factureachat.report_factureachat'
    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('gc-tjara.report_factureachat')
        docargs = {
            'doc_ids': docids,
            'doc_model': 'gctjara.factureachat',
            'docs': self,
        }
        return report_obj.render('gc-tjara.report_factureachat', docargs)