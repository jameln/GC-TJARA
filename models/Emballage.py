# -*- coding: utf-8 -*-

from odoo import fields , models, api


class Emballage(models.Model):
     _name = 'gctjara.emballage'
     
     type = fields.Char('Type d\'emballage')
     
     poids = fields.Char('Poids unitaire')
     
     produitemballee_id = fields.One2many(
        comodel_name='gctjara.produitemballee',
        string='Produits',
        inverse_name='emballage_id'
    )
  
       
