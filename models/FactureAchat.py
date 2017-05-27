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
    
    currency_id = fields.Many2one('res.currency',string='Currency',default=lambda self:self.env.user.company_id.currency_id)
    
    @api.one
    @api.depends("lignefact_id")
    def montant_ht(self):
       montantht=0       
       for lfa in self.lignefact_id:
           montantht += lfa.prix_ht
       self.prix_ht=montantht
       
    @api.one
    @api.depends("lignefact_id")
    def montant_totale(self):
       montanttot=0
       for rec in self :
           for lfa in rec.lignefact_id:
                   montanttot +=   lfa.prix_total 
       self.montant=montanttot

    @api.one
    @api.depends("montant")
    def montant_ttc(self):
       mmttc=0
       for mnt in self:
               mmttc = self.montant + self.timbre
       self.montantttc=mmttc
    
    @api.one
    @api.depends('montantttc')
    def _amount_in_words(self):
        self.amount_to_text = amount_to_text_fr(self.montantttc, 'dinars')
    
    
    amount_to_text = fields.Text(
        string='In Words',
        store=True, 
        readonly=True, 
        compute='_amount_in_words'
        )
    
  
  

class FactureAchatTemp(models.TransientModel):

    _name = "gctjara.factureachatregle"
    datereception=fields.Date(string='Date réception')
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
                  'daterecption':self.dateecheance,
                  'tauxtva':'18',
                  'prixht':factures.montant,
                  'prixttc': factures.montantttc,
                  'etatrapp':self.etatrapp,
                  'modepayment':self.modepayment,
                  'numerochq':self.numerochq,
                  'facture_id':factures.id
                   })
            print ("recored id  >>>> " + str(record.id))
            factures.etatreglement= 'Réglée'
            factures.refregachat=record.id
            print ("recored id  >>>> " + str(record.id))
        return True
    
    
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     factureachat = fields.Many2one(
        'gctjara.factureachat',
        string="Facture"
    )   
     


to_19_fr = (u'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six',
          'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
          'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf')
tens_fr = ('vingt', 'trente', 'quarante', 'Cinquante', 'Soixante', 'Soixante-dix', 'Quatre-vingts', 'Quatre-vingt Dix')
denom_fr = ('',
          'Mille', 'Millions', 'Milliards', 'Billions', 'Quadrillions',
          'Quintillion', 'Sextillion', 'Septillion', 'Octillion', 'Nonillion',
          'Décillion', 'Undecillion', 'Duodecillion', 'Tredecillion', 'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Icosillion', 'Vigintillion')

def _convert_nn_fr(val):
    """ convert a value < 100 to French
    """
    if val < 20:
        return to_19_fr[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_fr)):
        if dval + 10 > val:
            if val % 10:
                if dval == 70 or dval == 90:
                    return tens_fr[dval / 10 - 3] + '-' + to_19_fr[val % 10 + 10]
                else:
                    return dcap + '-' + to_19_fr[val % 10]
            return dcap

def _convert_nnn_fr(val):
    """ convert a value < 1000 to french
    
        special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        if rem == 1:
            word = 'Millime'
        else:
            word = to_19_fr[rem] + ' Cent'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_fr(mod)
    return word

def french_number(val):
    if val < 100:
        return _convert_nnn_fr(val)
        # return _convert_nn_fr(val)

    if val < 1000:
        return _convert_nnn_fr(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_fr))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            if l == 1:
                ret = denom_fr[didx]
            else:
                ret = _convert_nnn_fr(l) + ' ' + denom_fr[didx]
            if r > 0:
                ret = ret + ', ' + french_number(r)
            return ret

def amount_to_text_fr(numbers, currency):
    number = '%.2f' % numbers
    units_name = currency
    liste = str(number).split('.')
    start_word = french_number(abs(int(liste[0])))
    end_word = french_number(int(liste[1]))
    cents_number = int(liste[1])
    cents_name = (cents_number > 1) and ' Millime' or ' Millime'
    final_result = start_word + ' ' + units_name + ' ' + end_word + ' ' + cents_name
    return final_result