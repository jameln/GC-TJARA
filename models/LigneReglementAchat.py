# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneReglementAchat(models.Model):
   _name = 'gctjara.ligneregachat'
   

   
   facture_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name='gctjara.factureAchat',
        ondelete='cascade'
    )
   
   bonentree_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name='gctjara.bonentree',
        ondelete='cascade'
    )
   
   reglement_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name='gctjara.factureAchat',
        ondelete='cascade'
    )
   
   
   