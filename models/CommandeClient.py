# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommandeClient(models.Model):
     _name = 'gctjara.cmdclient'
     
     numerocmdc = fields.Char(
         string='Numéro',
         default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.cmdclt.seq'),
          )     
  
     
     datecommande = fields.Date(
         string='Date',
         required=True,
         default=fields.datetime.now(),
         help='Date création')
     
     datereception = fields.Date(
         'Date de reception',
         required=True,
         default=fields.datetime.now(),
         help='Date   reception  de la commande '
         )
     
     attachment = fields.One2many(
         'ir.attachment',
         'cmdclient',
         string='Pièces jointes'
                                )
     
     description = fields.Text(
         String='Description'
         )
     
        
     quantite = fields.Float(
        string='Quantite',
        required=True,
        default=1.0,
        digits=(16, 3)
    )
    
     valid = fields.Boolean(
        string='Ne pas annuler',
        default=False
    )
     
     client_id = fields.Many2one(string="Client",
                                comodel_name='gctjara.client'
                             )
     
     
     state = fields.Selection(
        string='Etat',
        default='sa',
        selection=[
            ('sa', 'Saisie'),
            ('br', 'Brouillon'),
            ('va', 'Validee'),
            ('tr', 'Terminee'),
            ('an', 'Annulee')
        ]
    )
     
     def write(self, values):
        print values
        if values.has_key('state'):
            if values.get('state') == 'sa':
                values['state'] = 'br'
        result = super(CommandeClient, self).write(values)
        return result

     @api.multi
     def afficher(self):
        print "afficher()"
        raise ValidationError('id commande : ' + str(self.id))
        return True

     def cmdclt_brouillon(self):
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
            
              
     def create_factvente(self):
        sequences =   self.env['ir.sequence'].next_by_code('gctjara.facturevente.seq') 
        self.env['gctjara.facturevente'].create({
              'numero' :  sequences,
              'datefact': self.datereception,
              
            })
        return True
    
    
     @api.one
     def cmdclt_valider(self):
        
#         self.message_post(type='notification',
#                           subtype='mt_comment',
#                           subject='Note d\'information: Validation commande N ' + self.numerocmdc,
#                           body='La commande N ' + self.numerocmdc + ' a ete valide par : ' + str(self.env.user.name),
#                           partner_ids=[self.client_id.id])
                          
        self.write({
            'state': 'va',
            'description': 'Commande valide le: ' + fields.datetime.now().strftime('%d/%m/%Y %H:%M')
        })
        
        
        self.create_factvente()
         
        return True
    
     def cmdclt_terminer(self):
        self.write({'state': 'tr'})
        return True
    
     def cmdclt_annuler(self):
        if self.valid:
            raise ValidationError("Cette commande est verouillee!")
        self.write({'state': 'an'})
        return True
       

      
     facture_id = fields.One2many(string='Lignes Facture',
                         comodel_name='gctjara.facturevente',
                         inverse_name='commande_id',
                         )
       
#      lignecmd_id = fields.One2many(string='Lignes commande',
#                           comodel_name='gctjara.lignecmdvente',
#                           inverse_name='commande_id',
#                           )
#       
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     cmdclient = fields.Many2one(
        'gctjara.cmdclient',
        string="Pièces jointes"
    ) 
    