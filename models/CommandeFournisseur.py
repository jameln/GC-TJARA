# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommandeFournisseur(models.Model):
     _name = 'gctjara.cmdfournisseur'
     
     numero = fields.Char('Numero Commande')
     
     datecommande = fields.Date('Date de CMD',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date création')
     
     datereception = fields.Date('Date de reception',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date   reception  de la commande ')
     
#      facture_id = fields.One2many(string='Lignes Facture',
#                            comodel_name='gctjara.factureAchat',
#                            inverse_name='commande_id',
#                            )
#      
#      lignecmd_id = fields.One2many(string='Lignes commande',
#                            comodel_name='gctjara.lignecmdachat',
#                            inverse_name='commande_id',
#                            )
#      
#      fournisseur_id = fields.Many2one(
#                                     comodel_name='gctjara.fournisseur',
#                                     string="Fournisseur",
#                                     ondelete='restrict'
#                                     )
#      
#      
#      
#      
