# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime


class FactureAchat(models.Model):
    
    _name = 'gctjara.factureachat'
    
    _rec_name = 'numero'
    
    _inherit='mail.thread'
       
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
    
    prix_ht = fields.Float(
         string='Montant HT',
         compute='montant_ht',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
    montant = fields.Float(
         string='Montant',
         compute='montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
  
    montantttc=fields.Float(
         string='Montant TTC',
         compute='montant_ttc',
         digits=(16, 3),
         default = 0.0,
         store=True
        )
    
    refregachat=fields.Many2one(comodel_name='gctjara.regachat',string='Réf reglement')
    
    def getReglementID(self):
        if self.refregachat: 
            return {
                'name' : 'Règlement',
                'res_model':'gctjara.regachat',
                'res_id':self.refregachat.id,
                'view_type':'form',
                'view_mode':'form',
                'type':'ir.actions.act_window'
                
                }
    
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self:self.env.user.company_id.currency_id
    )

    montantremise = fields.Float(
        string='Remise',
        compute='montant_totale',
        digits=(16, 3),
        default=0.0,
        store=True
    )

    @api.one
    @api.depends("lignefact_id")
    def montant_ht(self):
       montantht=0
       for lfa in self.lignefact_id:
           montantht += lfa.prix_ht
       self.prix_ht=montantht
       
    @api.multi
    @api.depends("lignefact_id")
    def montant_totale(self):
       montanttot=0
       montantremise=0
       for rec in self :
           for lfa in rec.lignefact_id:
                   montanttot +=   lfa.prix_total
                   montantremise+=lfa.prix_ht*(float(lfa.remise/100))
       self.montant=montanttot
       self.montantremise=montantremise

    @api.one
    @api.depends("montant")
    def montant_ttc(self):
       mmttc=0
       for mnt in self:
               mmttc = self.montant + self.timbre
       self.montantttc=mmttc


class FactureAchatTemp(models.TransientModel):

    _name = "gctjara.factureachatregle"
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
            ('tr', 'Traite')
        ]
    )
    etatrapp=fields.Selection(
        string='Etat de rapprochement',
        default='',
        selection=[
            ('db', 'A débiter'),
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),
        
        ]
    )
    numerochq=fields.Char(string='Numero')
    @api.multi
    def Paiement(self):
        for facture_id in self.env.context.get('active_ids'):
            factures=self.env['gctjara.factureachat'].search([('id','=',facture_id)])
           
         
            if(factures.etatreglement == u"Réglée"):
                raise ValidationError('La facture numéro  ' + str(factures.numero) + ' est déja réglée')
                return False
                              
            record=self.env['gctjara.regachat'].create({
                  'numero' : self.env['ir.sequence'].next_by_code('gctjara.regachat.seq'),
                  'date':fields.datetime.now(),
                  'dateoperation':self.dateoperation,
                  'datevaleur': self.datevaleur,
                  'dateecheance':self.dateecheance,
                  'tauxtva':'18',
                  'prixht':factures.montant,
                  'prixttc': factures.montantttc,
                  'etatrapp':self.etatrapp,
                  'modepayment':self.modepayment,
                  'numerochq':self.numerochq,
                  'facture_id':factures.id
                   })
            factures.etatreglement= 'Réglée'
            factures.refregachat=record.id
        return True
    
    
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     factureachat = fields.Many2one(
        'gctjara.factureachat',
        string="Facture"
    )   
     
