# -*- coding: utf-8 -*-

from odoo import fields , models, api


class Emballage(models.Model):
     _name = 'gctjara.emballage'
     
     _rec_name= 'type'
     
     name = fields.Char(string='Nom' , compute='_compute_name')
     
     @api.depends('type', 'poids')
     def _compute_name(self):
        for r in self:
            r.name= r.type + " "+ r.poids
        
       
     type = fields.Char('Type d\'emballage')
     
     poids = fields.Char('Poids unitaire')
     
     produitemballee_id = fields.One2many(
        comodel_name='gctjara.produitemballee',
        string='Produits',
        inverse_name='emballage_id'
    )
  
       
