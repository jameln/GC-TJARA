# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime


class FactureAchat(models.Model):
    
    _name = 'gctjara.factureachat'
    
    _rec_name = 'numero'
       
    numero = fields.Char(
        string='N° facture',
        required=True,
        index=True,
        size=50,
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.factureachat.seq')
       
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
        default=False
    )
    
  
       
    fournisseur_id = fields.Many2one('gctjara.fournisseur',
                                   string="Fournisseur",
                                   ondelete='restrict',
                                   store=True
                                   )
       
    commande_id = fields.Many2one(
        string="Commande",
        ondelete='restrict',
        comodel_name='gctjara.cmdfournisseur'
          )

    
    lignefact_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignefactachat',
#         compute='reffact',
        inverse_name='facture_id'
         )
        
    lignecmd_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignecmdachat',
        inverse_name='commande_id'
         )
    etatreglement=fields.Char(
        string='Etat facture',
        readonly='1',
        store=True,
        default=''
        )
       
      
    attachment = fields.One2many('ir.attachment',
                               'factureachat',
                                string='Pièce jointe'
                                )
    
    timbre=fields.Float(
        string ='Timbre',
        default=0.5,
        store=True
        )
    
   
    montant = fields.Float(
         string='Montant',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
    montantttc=fields.Float(
         string='Montant TTC',
         compute='_montant_ttc',
         digits=(16, 3),
         default = 0.0,
         store=True
        )
    
    @api.one
    @api.depends("lignefact_id")
    def _montant_totale(self):
       montanttot=0
       for lfa in self.lignefact_id:
               montanttot = montanttot + lfa.prix_total 
       self.montant=montanttot

    @api.one
    @api.depends("montant")
    def _montant_ttc(self):
       mmttc=0
       for mnt in self:
               mmttc = self.montant + self.timbre
       self.montantttc=mmttc
  
  

class FactureAchatTemp(models.TransientModel):
    _name = "gctjara.factureachatregle"
    
    datereception=fields.Date(string='Date réception')
    datevaleur=fields.Date(string='Date valeur')
    dateoperation=fields.Date(string='Date opération')
    dateecheance=fields.Date(string='Date écheance')
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

    @api.multi
    def Payment(self):
        for facture_id in self.env.context.get('active_ids'):
            factures=self.env['gctjara.factureachat'].search([('id','=',facture_id)])
           
         
            if(factures.etatreglement == u"Réglée"):
                raise ValidationError('La facture numéro  ' + str(factures.numero) + ' est déja réglée')
                return False

                              
            self.env['gctjara.regachat'].create({
                  'numero' : self.env['ir.sequence'].next_by_code('gctjara.regachat.seq'),
                  'date':fields.datetime.now(),
                  'dateoperation':self.dateoperation,
                  'datevaleur':self.datevaleur,
                  'daterecption':self.dateecheance,
                  'tauxtva':'18',
                  'prixht':factures.montant,
                  'prixttc': factures.montantttc,
                  'etatrapp':self.etatrapp,
                 ' modepayment':self.modepayment
                  
                   })
               
            factures.etatreglement='Réglée'
       
        return True
    
    
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     factureachat = fields.Many2one(
        'gctjara.factureachat',
        string="Facture"
    )   