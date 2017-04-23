# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Produits(models.Model):

    _name = 'gctjara.produits'

    name = fields.Char(
        string='Appelation',
        required=True,
        index=True,
        help='Le nom du produit',
        size=50,
        )    

    code = fields.Char(
        string='Code',
        required=True,
        index=True,
        help='Le code du produit',
        size=50
        )

    dateexpiration = fields.Datetime(
        string='Date Expiration',
        default=fields.datetime.now(),
        )
    
    description = fields.Text(
        string='Description'
        )
    
   
    prixachat = fields.Float(
        string='Prix d\'achat'
        )
    
    prixvente = fields.Float(
        string='Prix de vente'
        )
    
    quantite = fields.Float(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
    )
    
#     fournisseur_id = fields.One2many(
#         comodel='gctjara.fournisseur',
#         string="Fournisseur",
#         ondelete='restrict',
#         inverse_name='produit_id'
#         )
#       
#     client_id = fields.One2many(
#         comodel='gctjara.client',
#         string="Clients",
#         ondelete='restrict',
#         inverse_name='produit_id'
#         )
#       
#     stock_id = fields.One2many(
#         comodel_name='gctjara.stock',
#         string='Stock',
#         inverse_name='produit_id'
#     )
#       
#     embalageproduit_id = fields.Many2one(
#         comodel_name='gctjara.ligneprodemballage',
#         string='Emballage',
#     )
