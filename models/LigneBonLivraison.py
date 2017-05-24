# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneBonLivraison(models.Model):
    
    _name = 'gctjara.lignebonlivraison'
    
    _rec_name='name'
   
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
    prixvente= fields.Float(
       string='Prix unitaire',
       digits=(16, 3),
       store=True
    )
    tva = fields.Integer(
        string='TVA',
        default='6',
        digits=(16, 3),
    )
    commande_id = fields.Many2one(
         required=True,
         index=True,
         comodel_name='gctjara.cmdclient',
          
     )
    embalageproduit_id = fields.Many2one(
         comodel_name='gctjara.produitemballee',
         string='Emballages'
     )
    
    bonlivraison_id = fields.Many2one(
         required=True,
         index=True,
         comodel_name='gctjara.bonlivraison',
          
     )
     
    @api.depends("quantite" , "embalageproduit_id")
    def prixtot(self):
        for pe in self:
            tauxtva=float(pe.tva)/100
            prixht=pe.quantite * pe.embalageproduit_id.prixvente*pe.embalageproduit_id.emballage_id.poids
           
            pe.prix_total =prixht*(1+tauxtva)
            
    prix_total = fields.Float(
        string='Prix Tot',
        compute="prixtot",
        digits=(16, 3),
        store=True
    )