# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneProduitEmballage(models.Model):
    _name = 'gctjara.produitemballee'
   
    quantite = fields.Integer(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
    )
     
    produit_id = fields.Many2one(
          string='Produit',
          required=True,
          index=True,
          comodel_name='gctjara.produits',
          ondelete='set null'
      )
    
    emballage_id = fields.Many2one(
         comodel_name='gctjara.emballage',
         string='Emballage',
     )
#    

    prix_total = fields.Float(
        string='Prix TTC',
        
        digits=(16, 3)
    )


#     stock_id = fields.One2many(
#          string='Stock',
#          required=True,
#          index=True,
#          comodel_name='gctjara.stock',
#          inverse_name='embalageproduit_id'
#      )
#     
#     cmdachat_id = fields.One2many(
#          string='Commande Achat',
#          required=True,
#          index=True,
#          comodel_name='gctjara.lignecmdachat',
#          inverse_name='embalageproduit_id'
#      )
#     
#     cmdvente_id = fields.One2many(
#          string='Commande Vente',
#          required=True,
#          index=True,
#          comodel_name='gctjara.lignecmdvente',
#          inverse_name='embalageproduit_id'
#      )
