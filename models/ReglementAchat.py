# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ReglementAchat(models.Model):

    _name = 'gctjara.regachat'
    
    _rec_name = 'numero'
    
    numero = fields.Char(
        string='Numero règlement',
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.regachat.seq')
                         )
    
    date = fields.Date(string='Date règlement',
                      required=True,
                      default=fields.datetime.now(),
                      help='La date de création de la facture'
                      )
    
    datevaleur = fields.Date(string='Date valeur',
                            default=fields.datetime.now(),
                            )
    
    dateoperation=fields.Date(
        string='Date d\'opération',
        default=fields.datetime.now(),
                            )
    
    daterecption = fields.Date(string='Date réception',
                             default=fields.datetime.now(),
                             )
    
    tauxtva = fields.Char(
        string='TVA',
     
        digits=(16, 3)
    )
    prixht = fields.Float(
        string='Prix HT',
       
        digits=(16, 3)
    )
   
    prixttc = fields.Float(
        string='Prix TTC',
        
        digits=(16, 3)
    )

    facture_id = fields.Many2one(
        string='Réf. facture',
        comodel_name='gctjara.factureachat'
    )

    modepayment=fields.Selection(
        string='Mode de payment',
        default='',
        selection=[
            ('ch', 'Chèque'),
            ('es', 'Espèce'),
            ('vr', 'Virement'),
            ('tr', 'Traite'),
            ('pr', 'Prélevement')
        ]
    )
    etatrapp=fields.Selection(
        string='Etat de rapprochement',
        default='',
        selection=[
            ('cd', 'A céditer'),
            ('db', 'A débiter'),
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),
        
        ]
    )

    
    description = fields.Text(
        string='Description',
       
    )
    upload_file=fields.Binary(string='Upload File')
    
    file_name=fields.Char(string='File Name')

