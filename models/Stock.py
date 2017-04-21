# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Stock(models.Model):

    _name = 'gctjara.stock'
    
    numero=fields.Char('Ref stock')
#     
#     produit_id =fields.Many2one(
#         comodel_name='gctjara.produits',
#         string='Produit'
#     )
    
#     lignefactureachat_id = fields.One2many(
#         string='Facture achat',
#         required=True,
#         index=True,
#         comodel_name='gctjara.lignefactachat',
#         inverse_name='stock_id'
#     )
#     
#     lignefacturevente_id = fields.One2many(
#         string='Facture vente',
#         required=True,
#         index=True,
#         comodel_name='gctjara.lignefactvente',
#         inverse_name='stock_id'
#     )
#     
#      
#     embalageproduit_id =fields.Many2one(
#         comodel_name='gctjara.ligneprodemballage',
#         string='Produit'
#     )
#     
#     depot_id =fields.Many2one(
#         comodel_name='gctjara.depot',
#         string='Depot'
#     )
#     
#     mouvement_id = fields.One2many(
#         string='Mouvement',
#         required=True,
#         index=True,
#         comodel_name='gctjara.mvtstock',
#         inverse_name='stock_id'
#     )