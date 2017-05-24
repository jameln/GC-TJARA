# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LignefactureVente(models.Model):
    
    _name = 'gctjara.lignefactvente'
    
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
       store=True,
      digits=(16, 3)
    )
    tva = fields.Integer(
        string='TVA',
        default='6',
      
    )
    facture_id = fields.Many2one(
         required=True,
         index=True,
         comodel_name='gctjara.facturevente',
          
     )
    embalageproduit_id = fields.Many2one(
         comodel_name='gctjara.produitemballee',
         string='Emballages'
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
    
    @api.depends("quantite" , "embalageproduit_id")
    def prixht(self):
        for pht in self:
            prixht=pht.quantite * pht.embalageproduit_id.prixvente*pht.embalageproduit_id.emballage_id.poids
            pht.prix_ht =prixht
            
    prix_ht = fields.Float(
        string='Prix ht',
        compute="prixht",
        digits=(16, 3),
        store=True
    )
    
  