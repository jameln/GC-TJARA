# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneFactureAchat(models.Model):
    _name = 'gctjara.lignefactachat'
   
    _rec_name = 'embalageproduit_id'
    
    name =fields.Char(
        string='Nom:',
        compute='_compute_name'
                      )
    
    @api.depends('embalageproduit_id')
    def _compute_name(self):
        for r in self:
            if(isinstance(r.embalageproduit_id.name , unicode)) :
                r.name= r.embalageproduit_id.name 
   
    quantite = fields.Integer(
        string='Quantite',
        required=True,
          )
    prixunit= fields.Float(
       string='Prix unitaire',
       store=True
    )
    tva = fields.Integer(
        string='TVA',
        default='6',
        digits=(16, 3),
    )
    facture_id = fields.Many2one(
         required=True,
         index=True,
         comodel_name='gctjara.factureachat',
          
     )
    embalageproduit_id = fields.Many2one(
         comodel_name='gctjara.produitemballee',
         string='Emballages'
     )
     
    @api.depends("quantite" , "embalageproduit_id")
    def prixtot(self):
        for pe in self:
            pe.prix_total = pe.quantite * pe.embalageproduit_id.prixunit*pe.embalageproduit_id.emballage_id.poids
            
    prix_total = fields.Float(
        string='Prix Tot',
        compute="prixtot",
        digits=(16, 3),
        store=True
    )
    
  
