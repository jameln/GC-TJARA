# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Depot(models.Model):

    _name = 'gctjara.depot'
    
    nomdepot = fields.Char('Nom de depot', required=True)
    
    adressedepot = fields.Char('Adresse de depot')
    
    
#     stock_id = fields.One2many(
#         string='Stock',
#         required=True,
#         index=True,
#         comodel_name='gctjara.stock',
#         inverse_name='depot_id'
#     )
