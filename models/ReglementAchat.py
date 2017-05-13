# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ReglementAchat(models.Model):

    _name = 'gctjara.regachat'
    
    _rec_name = 'numero'
    
    numero = fields.Char(string='Numero règlement',
                         required=True,
                         )
    
    date = fields.Date(string='Date règlement',
                      required=True,
                      default=fields.datetime.now(),
                      help='La date de création de la facture'
                      )
    
    datevaleur = fields.Date(string='Date valeur',
                            default=fields.datetime.now(),
                            )
    
    daterecption = fields.Date(string='Date réception',
                             default=fields.datetime.now(),
                             )
    
    tauxtva = fields.Char(
        string='TVA',
        compute="tauxtva",
        digits=(16, 3)
    )
    prixht = fields.Float(
        string='Prix HT',
        compute="prixht",
        digits=(16, 3)
    )
   
    prixttc = fields.Float(
        string='Prix TTC',
        compute="prixttc",
        digits=(16, 3)
    )
    description = fields.Text(
        string='Description',
       
    )
    attachment = fields.One2many('ir.attachment',
                               'regachat',
                                string='Pièces jointes'
                                )
       
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     regachat = fields.Many2one(
        'gctjara.regachat',
        string="Pièces jointes"
    )     
  
#      
#     lignereglementachat_id = fields.One2many(
#          string='Ligne règlement',
#          index=True,
#          comodel_name='gctjara.ligneregachat',
#          inverse_name='reglement_id',
#           
#          )
#       
# # 
#    
    
