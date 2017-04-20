# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommandeClient(models.Model):
     _name = 'gctjara.cmdclient'
     
     numerocmdc = fields.Char('Numero Commande')     
  
     
     datecommande = fields.Date('Date de CMD',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date création')
     
     datereception = fields.Date('Date de reception',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date   reception  de la commande ')
     
     facture_id =fields.One2many( string='Lignes Facture',
                           comodel_name='gctjara.facturevente',
                           inverse_name='commande_id',
                           )
     
     lignecmd_id =fields.One2many( string='Lignes commande',
                           comodel_name='gctjara.lignecmdvente',
                           inverse_name='commande_id',
                           )
     
     client_id=fields.Many2one(   string="Client",
                                  comodel_name='gctjara.client'
                               )
     
     
     