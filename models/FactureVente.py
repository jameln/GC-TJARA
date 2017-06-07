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


     lignefact_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignefactvente',
        inverse_name='facture_id'
         )
     
     client_id = fields.Many2one('gctjara.client',
                                   string="Client",
                                   ondelete='restrict'
                                   )

     adresse = fields.Char(
         string='Adresse',
         related='client_id.adresse',
         readonly="1",
         store=True
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
     montantremise = fields.Float(
         string='Remise',
         compute='_montant_totale',
         digits=(16, 3),
         default=0.0,
         store=True
     )

     @api.one
     @api.depends('montantttc')
     def _amount_in_words(self):
         self.amount_to_text = amount_to_text_fr(self.montantttc, self.env.user.company_id.currency_id.symbol)

     amount_to_text = fields.Text(
         string='In Words',
         store=True,
         readonly=True,
         compute='_amount_in_words'
     )

     @api.multi
     @api.depends("lignefact_id")
     def _montant_totale(self):
        montanttot=0
        mht=0
        montantremise=0
        for lfa in self.lignefact_id:
               montanttot = montanttot + lfa.prix_total 
               mht+= lfa.prix_ht
               montantremise += lfa.prix_ht * (float(lfa.remise / 100))
        self.montant=montanttot
        self.montantht=mht
        self.montantremise=montantremise

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
    number = '%.3f' % numbers
    units_name = currency
    liste = str(number).split('.')
    start_word = french_number(abs(int(liste[0])))
    end_word = french_number(int(liste[1]))
    cents_number = int(liste[1])
    cents_name = (cents_number > 1) and ' Millime' or ' Millime'
    final_result = start_word + ' ' + units_name + ' ' + end_word + ' ' + cents_name
    return final_result