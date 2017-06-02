# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FactureVente(models.Model):
    
     _name = 'gctjara.facturevente'
     
     _rec_name = 'numero'
     
     _inherit = 'mail.thread'
     
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
        default=False
    )
     
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

#      lignes_id = fields.One2many(
#         string='Lignes Facture',
#         comodel_name='gctjara.lignefactvente',
#         inverse_name='facture_id',
#     )
#       
     lignefact_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignefactvente',
        inverse_name='facture_id'
         )
     
     client_id = fields.Many2one('gctjara.client',
                                   string="Client",
                                   ondelete='restrict'
                                   )

     bonlivraison_id = fields.Many2one(
         string="Bon livraison N°",
         ondelete='restrict',
         comodel_name='gctjara.bonlivraison'
                                   )
         
         
    
     attachment = fields.One2many(
         'ir.attachment',
         'facturevente',
          string='Pièce jointe'
                                )
     
     etatreglement=fields.Char(
        string='Etat facture',
        readonly='1',
        store=True,
        default=''
        )
     refregvente = fields.Many2one(comodel_name='gctjara.regvente',string='Réf reglement')
      
     attachment = fields.One2many('ir.attachment',
                               'factureachat',
                                string='Pièce jointe'
                                )

     currency_id = fields.Many2one('res.currency', string='Currency',
                                   default=lambda self: self.env.user.company_id.currency_id)

     timbre=fields.Float(
        string ='Timbre',
        default=0.500,
        digits=(16, 3),
        store=True
        )
    
     montantht = fields.Float(
         string='Montant HT',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
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
        mht=0
        for lfa in self.lignefact_id:
               montanttot = montanttot + lfa.prix_total 
               mht+= lfa.prix_ht
        self.montant=montanttot
        self.montantht=mht

     @api.one
     @api.depends("montant")
     def _montant_ttc(self):
       mmttc=0
       for mnt in self:
               mmttc = self.montant + self.timbre
       self.montantttc=mmttc
    

class FactureVenteTemp(models.TransientModel):
    _name = "gctjara.factureventeregle"
    
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
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),
        
        ]
    )
    numerochq=fields.Char(string='Numero')


    @api.multi
    def Paiement(self):
        for facture_id in self.env.context.get('active_ids'):
            factures=self.env['gctjara.facturevente'].search([('id','=',facture_id)])
           
         
            if(factures.etatreglement == u"Réglée"):
                raise ValidationError('La facture numéro  ' + str(factures.numero) + ' est déja réglée')
                return False

                              
            record=self.env['gctjara.regvente'].create({
                  'numero' : self.env['ir.sequence'].next_by_code('gctjara.regvente.seq'),
                  'date':fields.datetime.now(),
                  'dateoperation':self.dateoperation,
                  'datevaleur':self.datevaleur,
                  'daterecption':self.dateecheance,
                  'tauxtva':'18',
                  'prixht':factures.montant,
                  'prixttc': factures.montantttc,
                  'etatrapp':self.etatrapp,
                  'modepayment':self.modepayment,
                  'numerochq':self.numerochq,
                  'facture_id':factures.id
                  
                   })
               
            factures.etatreglement='Réglée'
            factures.refregvente = record.id
       
        return True
    
 