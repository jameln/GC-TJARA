# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Produits(models.Model):

    _name = 'gctjara.produits'
    
    _rec_name = 'name'

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
    
    prixunit=fields.Float(
        string='Prix unitaire',
        default=0.0,
        digits=(16, 3)
        )
    
   
#     prixachat = fields.Float(
#         string='Prix d\'achat'
#         )
    
    prixvente = fields.Float(
        string='Prix de vente'
        )
    
#     quantite = fields.Float(
#         string='Quantite',
#         required=True,
#         default=0.0,
#         digits=(16, 3)
#     )
    
#     fournisseur_id = fields.One2many(
#         comodel='gctjara.fournisseur',
#         string="Fournisseur",
#         ondelete='restrict',
#         inverse_name='produit_id'
#         )
       
#     client_id = fields.One2many(
#         comodel='gctjara.client',
#         string="Clients",
#         inverse_name='produits_id'
#         )
#        
#     stock_id = fields.One2many(
#         comodel_name='gctjara.stock',
#         string='Stock',
#         inverse_name='produit_id'
#     )
#       
    produitemballee_ids = fields.One2many(
        comodel_name='gctjara.produitemballee',
        string='Emballage',
        inverse_name='produit_id'
    )
    
    emballages_id = fields.Many2many('gctjara.emballage', string='Emballages', store=False)
    
#     states=fields.Char('Status', default ='able')
#               
#     def create_produitemballee(self):
#         
#         self.env['gctjara.produitemballee'].write({
#             'quantite':50,
#             'produit_id' :  self.name,
#             'emballage_id': 1,
#             'prix_total':1200
#               
#             })
#         self.states='enable'
#         return True
#     
   
   
    
