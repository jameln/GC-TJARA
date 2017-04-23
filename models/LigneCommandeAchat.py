# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneCommandeAchat(models.Model):
    _name = 'gctjara.lignecmdachat'
   
    quantite = fields.Float(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
    )
    
#     commande_id = fields.Many2one(
#          required=True,
#          index=True,
#          comodel_name='gctjara.cmdfournisseur',
#          
#      )
#     embalageproduit_id = fields.Many2one(
#          comodel_name='gctjara.ligneprodemballage',
#          string='Emballage'
#      )
