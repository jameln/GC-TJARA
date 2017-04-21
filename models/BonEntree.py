# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BonEntree(models.Model):
     _name = 'gctjara.bonentree'
     
     numero = fields.Integer('Numéro')
     
     date = fields.Date(string='Date bon d\'entrée',
                          
                         required=True,
                         default=fields.datetime.now(),
                         help='La date de  bon de livraison'
                         )
#      
#      lignereglementachat_id = fields.One2many(
#          string='Ligne règlement',
#          index=True,
#          comodel_name='gctjara.ligneregachat',
#          inverse_name='bonentree_id',
#          
#          )
#      
#      mouvement_id = fields.One2many(
#          string='Mouvement de stock',
#          comodel_name='gctjara.mvtstock',
#          inverse_name='bonentree_id',
#          
#          )
#      
#      
#      
#      
     
     
