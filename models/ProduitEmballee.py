# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneProduitEmballage(models.Model):
    _name = 'gctjara.produitemballee'
    
    _rec_name = 'name'
       
    _sql_constraints = [
        ('produitemballée', 'unique (emballage_id , produit_id )', 'Cette emballage est déja crée')
    ] 
    
    name = fields.Char(string='Nom' , compute='_compute_name')
    
    @api.depends('produit_id', 'emballage_id')
    def _compute_name(self):
        for r in self:
            if(isinstance(r.produit_id.name , unicode)) and isinstance(r.emballage_id.name,unicode):
                r.name= r.produit_id.name + " "+ r.emballage_id.name
               
   
         
    @api.depends('produit_id')
    def _prix_unit(self):
         for r in self:
            r.prixunit=r.produit_id.prixunit
     
     
  
#     quantite = fields.Integer(
#         string='Quantite',
#         required=True,
#         default=0,
#        
#     )
    
    quantitestocke=fields.Float(
        string ='Stock',
        default=0.0,
        digits=(16, 3)
        )
     
    produit_id = fields.Many2one(
          string='Produit',
          required=True,
          index=True,
          comodel_name='gctjara.produits',
          ondelete='set null'
      )
    
    prixunit= fields.Float(
        related='produit_id.prixunit',
        string='Prix unitaire',
        compute='_prix_unit',
        store=True
    )
    
    emballage_id = fields.Many2one(
         comodel_name='gctjara.emballage',
         string='Emballage',
     )
    
    lignecmd_id = fields.One2many(
        string='Commandes',
        comodel_name='gctjara.lignecmdachat',
        inverse_name='embalageproduit_id'
                        )  
  
