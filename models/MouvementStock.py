# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MouvementStock(models.Model):

    _name = 'gctjara.mvtstock'
    
    _rec_name = 'numero'
    
    numero = fields.Char('Numero mvt')
    date = fields.Date('Date de Mvt' ,
                     default=fields.datetime.now() 
        )
    
#     bonentree_id = fields.Many2one(
#         string='Bon d\'entrée',
#         comodel_name='gctjara.bonentree',
#           
#         )
#      
#     bonlivaison_id = fields.Many2one(
#         string='Bon de livraison',
#         comodel_name='gctjara.bonlivraison',
#           
#         )
#      
#      
#     stock_id = fields.Many2one(
#         string='Bon d\'entrée',
#         comodel_name='gctjara.bonentree',
#           
#         )
