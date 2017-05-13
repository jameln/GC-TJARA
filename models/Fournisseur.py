# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Fournisseur(models.Model):
     _name = 'gctjara.fournisseur'
     
     _rec_name = 'name'
     
     name = fields.Char('Nom', required=True)
     
     matriculefiscal = fields.Char('Matricule fiscale', required=True)
     
     company_name = fields.Char('Company Name')
     
     image = fields.Binary("Image",
                           attachment=True,
                           help="This field holds the image used as avatar for this contact, limited to 1024x1024px",
                           )
     
     email = fields.Char('Email')
     
     phone = fields.Char('Telephone')
     
     fax = fields.Char('Fax')
     
     mobile = fields.Char('Portable')
     
     adresse = fields.Char('Adresse')
     
     street = fields.Char()
    
     zip = fields.Char(change_default=True)
     
     city = fields.Char()
     
     active = fields.Boolean(default=True)
      
     commande_id = fields.One2many(
       string="Commande",
       ondelete='restrict',
       comodel_name='gctjara.cmdfournisseur',
       inverse_name='fournisseur_id',
       )
#       
#      facture_id = fields.One2many(
#         string="Factures",
#         ondelete='restrict',
#         comodel_name='gctjara.factureachat',
#         inverse_name='fournisseur_id',
#         )
#       
#      produit_id = fields.Many2one(
#         string='Prosuits',
#         comodel_name='gctjara.produits'
#        )
#   
