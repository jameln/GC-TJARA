# -*- coding: utf-8 -*-

from odoo import fields , models, api


class Emballage(models.Model):
     _name = 'gctjara.emballage'
     
     type=fields.Char('Type d\'emballage')
     
     poids = fields.Char('Poids unitaire')
     
     embalageproduit_id =fields.Many2one(
        comodel_name='gctjara.ligneprodemballage',
        string='Produits'
    )

     