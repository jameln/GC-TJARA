# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
  
  
  
    def write(self, values):
        print values
        if values.has_key('state'):
            if values.get('state') == 'sa':
                values['state'] = 'br'
        result = super(FactureAchat, self).write(values)
        return result

    @api.multi
    def afficher(self):
        print "afficher()"
        raise ValidationError('id facture : ' + str(self.id))
        return True

    def fctachat_brouillon(self):
        self.write({'state': 'br'})
        return True
    
    def getClientID(self):
        if self.client_id: 
            return {
                'name' : 'client',
                'res_model':'res.partner',
                'res_id':self.client_id.id,
                'view_type':'form',
                'view_mode':'form',
                'type':'ir.actions.act_window'
                
                }
    
    @api.one
    def fctachat_valider(self):
        
        self.message_post(type='notification',
                          subtype='mt_comment',
                          subject='Note d\'information: Validation Facture N ' + self.name,
                          body='La Facture N ' + self.name + ' a ete valide par : ' + str(self.env.user.name),
                          partner_ids=[self.client_id.id])
                          
        self.write({
            'state': 'va',
            'description': 'facture valide le: ' +
                           fields.datetime.now().strftime('%d/%m/%Y %H:%M')
        })
        return True

    def fctachat_payer(self):
        self.write({'state': 'pa'})
        return True

    def fctachat_annuler(self):
        if self.valid:
            raise ValidationError("Cette facture est verouillee!")
        self.write({'state': 'an'})
        return True
    
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     factureachat = fields.Many2one(
        'gctjara.factureachat',
        string="Facture"
    )   