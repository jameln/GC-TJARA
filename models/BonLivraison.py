# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BonLivraison(models.Model):
     _name = 'gctjara.bonlivraison'
     
     numero = fields.Char('Numero ',
          required=True,
          index=True,
          size=50,)
     
     datebl = fields.Date('Date BL',
                         required=True,
                         default=fields.datetime.now(),
                         help='La date de  bon de livraison')
     
     
     
#      
#      lignereglementvente_id = fields.One2many(
#         string='Règlement',
#         comodel_name='gctjara.ligneregvente',
#         inverse_name='bonlivraison_id',
#         )
#       
#      mouvement_id = fields.One2many(
#         string='Mouvement',
#         comodel_name='gctjara.mvtstock',
#         inverse_name='bonlivaison_id',
#         )
# #      
