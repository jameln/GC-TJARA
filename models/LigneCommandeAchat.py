# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneCommandeAchat(models.Model):
    _name = 'gctjara.lignecmdachat'
    
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
    
    commande_id = fields.Many2one(
         required=True,
         index=True,
         comodel_name='gctjara.cmdfournisseur',
          
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
    reffact=fields.Char()
    
#     @api.model
#     @api.depends('reffact')
#     def create(self,vals):
#         result = super(LigneCommandeAchat, self).create(vals)
#         record = self.env['gctjara.lignefactachat'].create({
#                     'quantite':self.quantite,
#                     'embalageproduit_id':vals['embalageproduit_id'],
#                     'prix_total':self.prix_total,
#                     'facture_id':nextval('gctjara_lignefactachat_id_seq')
#                     })
#         return result
    
    def is_empty(any_structure):
        if any_structure:
           print('Structure is not empty.')
           return  True
        else:
            print('Structure is empty.')
            return False
         
#   
#     self._create_lignefacture()
#                

  