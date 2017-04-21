# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LignefactureVente(models.Model):
    
   _name = 'gctjara.lignefactvente'
   
   
   quantite = fields.Float(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
    )
#    
#    stock_id = fields.Many2one(
#         string='Produit',
#         required=True,
#         index=True,
#         comodel_name='gctjara.stock',
#         ondelete='set null'
#     )
#    
#    facture_id = fields.Many2one(
#         required=True,
#         index=True,
#         comodel_name='gctjara.facturevente',
#         ondelete='cascade'
#     )
#    
   prix_total = fields.Float(
        string='Prix TTC',
        compute="prixtot",
        digits=(16, 3)
    )



     