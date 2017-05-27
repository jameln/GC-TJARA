# -*- coding: utf-8 -*-

from odoo import fields , models, api


class Emballage(models.Model):
     _name = 'gctjara.emballage'
     
     _rec_name= 'name'
     
     name = fields.Char(string='Nom' ,default="Produit" ,compute='_compute_name')
     
    
       
     type = fields.Char('Type d\'emballage', default='Type', placeholder="Type")
     
     poids = fields.Integer(string='Poids unitaire', placeholder="0")
     
     produitemballee_id = fields.One2many(
        comodel_name='gctjara.produitemballee',
        string='Produits',
        inverse_name='emballage_id'
    )
     @api.depends('type', 'poids')
     def _compute_name(self):
        for r in self:
            r.name= r.type + " "+ str(r.poids)
        
       
