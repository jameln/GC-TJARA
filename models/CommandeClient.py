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
     
     attachment = fields.One2many('ir.attachment',
                               'cmdclient',
                                string='Pièces jointes'
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
     
     def write(self, values):
        print values
        if values.has_key('state'):
            if values.get('state') == 'sa':
                values['state'] = 'br'
        result = super(Facture, self).write(values)
        return result

     @api.multi
     def afficher(self):
        print "afficher()"
        raise ValidationError('id facture : ' + str(self.id))
        return True

     def fct_brouillon(self):
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
     def fct_valider(self):
        
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

     def fct_payer(self):
        self.write({'state': 'pa'})
        return True

     def fct_annuler(self):
        if self.valid:
            raise ValidationError("Cette facture est verouillee!")
        self.write({'state': 'an'})
        return True
       
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     cmdclient = fields.Many2one(
        'gctjara.cmdclient',
        string="Pièces jointes"
    ) 
#      
#      facture_id = fields.One2many(string='Lignes Facture',
#                           comodel_name='gctjara.facturevente',
#                           inverse_name='commande_id',
#                           )
#       
#      lignecmd_id = fields.One2many(string='Lignes commande',
#                           comodel_name='gctjara.lignecmdvente',
#                           inverse_name='commande_id',
#                           )
#       
#      client_id = fields.Many2one(string="Client",
#                                  comodel_name='gctjara.client'
#                               )
#    
