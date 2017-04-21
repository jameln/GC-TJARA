# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FactureAchat(models.Model):
     _name = 'gctjara.factureAchat'
    
     
     numero = fields.Char(
        string='N° facture',
        required=True,
        index=True,
        size=50,
       
    )
    
     datefact = fields.Date(
        string='Date facture',
        required=True,
        default=fields.datetime.now(),
        help='La date de création de la facture'
    )
    
     datepayfact = fields.Date(
        string='Date payment',
        
        default=fields.datetime.now(),
        help='La date de payment de la facture'
    )

     description = fields.Text(
        string='Commentaire',
        required=False,
        help='Champ libre pour la saisie de commentaires'
    )

  
     valid = fields.Boolean(
        string='Ne pas annuler',
        default=True
    )
#      lignes_id = fields.One2many(
#         string='Stock',
#         comodel_name='gctjara.lignefactachat',
#         inverse_name='facture_id',
#     )
#      
#      lignefacturevente_id = fields.One2many(
#         string='Facture',
#         required=True,
#         index=True,
#         comodel_name='gctjara.lignefactvente',
#         inverse_name='facture_id'
#     )
#      
#      lignereglementachat_id = fields.One2many(
#          string='Règlement',
#          comodel_name='gctjara.ligneregachat',
#          inverse_name='facture_id',
#          )
#      

     state = fields.Selection(
        string='Etat',
        default='sa',
        selection=[
            ('sa', 'Saisie'),
            ('br', 'Brouillon'),
            ('va', 'Validee'),
            ('pa', 'Payee'),
            ('an', 'Annulee')
        ]
    )

    
#      
#      fournisseur_id = fields.Many2one('gctjara.fournisseur',
#                                     string="Fournisseur",
#                                     ondelete='restrict'
#                                     )
#      
#      commande_id = fields.Many2one(string="Commande",
#                                     ondelete='restrict',
#                                     comodel_name='gctjara.cmdfournisseur'
#                                     )
#        
#        
#     
#      attachment = fields.One2many('ir.attachment',
#                                 'facture_rel',
#                                  string='Pièce jointe'
#                                  )
#       
# class Attachment(models.Model):
#  
#      _inherit = 'ir.attachment'
#      _name = 'ir.attachment'
#       
#      facture_rel = fields.Many2one(
#         'gctjara.factureAchat',
#         string="Facture"
#     )     

     
