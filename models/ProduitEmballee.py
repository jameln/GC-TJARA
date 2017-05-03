# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneProduitEmballage(models.Model):
    _name = 'gctjara.produitemballee'
       
    _sql_constraints = [
        ('produitemballée', 'unique (emballage_id , produit_id )', 'Cette emballage est déja crée')
    ] 
    
    name = fields.Char(string='Nom' , compute='_compute_name')
    
    @api.depends('produit_id', 'emballage_id')
    def _compute_name(self):
        for r in self:
            if(isinstance(r.produit_id.name , unicode)) and isinstance(r.emballage_id.name,unicode):
                r.name= r.produit_id.name + " "+ r.emballage_id.name
        
    
    
  
    quantite = fields.Integer(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
    )
     
    produit_id = fields.Many2one(
          string='Produit',
          required=True,
          index=True,
          comodel_name='gctjara.produits',
          ondelete='set null'
      )
    
    emballage_id = fields.Many2one(
         comodel_name='gctjara.emballage',
         string='Emballage',
     )
    

    prix_total = fields.Float(
        string='Montant',
        digits=(16, 3)
    )


#     stock_id = fields.One2many(
#          string='Stock',
#          required=True,
#          index=True,
#          comodel_name='gctjara.stock',
#          inverse_name='embalageproduit_id'
#      )
#     
    cmdachat_id = fields.One2many(
         string='Commandes',
         index=True,
         comodel_name='gctjara.lignecmdachat',
         inverse_name='embalageproduit_id'
     )
     
#     cmdvente_id = fields.One2many(
#          string='Commande Vente',
#          required=True,
#          index=True,
#          comodel_name='gctjara.lignecmdvente',
#          inverse_name='embalageproduit_id'
#      )
