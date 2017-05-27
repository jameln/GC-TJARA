# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneCommandeAchat(models.Model):
    _name = 'gctjara.lignecmdachat'
    
    _rec_name = 'name'
    
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
    
    tva = fields.Selection(
        string='TVA',
        default='6',
        selection=[
            ('0', '0'),
            ('6', '6'),
            ('12', '12'),
            ('18', '18'),
            ('22', '22')
        ]
    )
    @api.depends('embalageproduit_id')
    def _prix_unit(self):
         for r in self:
            r.prixunit=r.embalageproduit_id.prixunit
            
    prixunit= fields.Float(
        related='embalageproduit_id.prixunit',
        string='Prix unitaire',
        compute='_prix_unit',
        store=True
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
    @api.multi 
    @api.depends("quantite" , "embalageproduit_id")
    def prixtot(self):

        for pe in self:
            tauxtva=float(pe.tva)/100
            prixht=pe.quantite * pe.embalageproduit_id.prixunit*pe.embalageproduit_id.emballage_id.poids
            print ("tva ===> "+str(tauxtva))
            print("prixht ==>" + str(prixht))
            pe.prix_ht=prixht
            pe.prix_total =prixht*(1+tauxtva)
            
    prix_total = fields.Float(
        string='Prix Tot',
        compute="prixtot",
        digits=(16, 3),
        store=True
    )
    prix_ht = fields.Float(
        string='Prix HT',
        compute="prixtot",
        digits=(16, 3),
        store=True
    )
    reffact=fields.Char()

    def is_empty(any_structure):
        if any_structure:
           print('Structure is not empty.')
           return  True
        else:
            print('Structure is empty.')
            return False
         

  