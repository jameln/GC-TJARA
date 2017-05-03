# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneCommandeAchat(models.Model):
    _name = 'gctjara.lignecmdachat'
    
    _rec_name = 'embalageproduit_id'
   
    quantite = fields.Float(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
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
    
    prix_total = fields.Float(
        string='Montant',
        digits=(16, 3)
    )
    
    
    montant = fields.Float(
        string='Montant :',
        compute="montanttot",
        digits=(16, 3),
        default = 0.0
    )
    
    @api.depends("prix_total")
    def montanttot(self):
        
        for lca in self:
            lca.montant = lca.montant + lca.prix_total 

