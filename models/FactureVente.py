# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FactureVente(models.Model):
    
     _name = 'gctjara.facturevente'
     
#      _inherit = 'mail.thread'
     
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
#      lignereglementvente_id = fields.One2many(
#          string='Règlement',
#          comodel_name='gctjara.ligneregvente',
#          inverse_name='facture_id',
#          )
#       
#  
#    
# #   
# #      
#      client_id = fields.Many2one('gctjara.client',
#                                     string="lient",
#                                     ondelete='restrict'
#                                     )
#       
#      commande_id = fields.Many2one(string="Commande",
#                                     ondelete='restrict',
#                                     comodel_name='gctjara.cmdclient'
#                                     )
#         
#         
#     
     attachment = fields.One2many('ir.attachment',
                               'facturevente',
                                string='Pièce jointe'
                                )
     
     
     def write(self, values):
        print values
        if values.has_key('state'):
            if values.get('state') == 'sa':
                values['state'] = 'br'
        result = super(FactureVente, self).write(values)
        return result

     @api.multi
     def afficher(self):
        print "afficher()"
        raise ValidationError('id facture : ' + str(self.id))
        return True

     def fctvente_brouillon(self):
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
     def fctvente_valider(self):
        
#         self.message_post(type='notification',
#                           subtype='mt_comment',
#                           subject='Note d\'information: Validation Facture N ' + self.name,
#                           body='La Facture N ' + self.name + ' a ete valide par : ' + str(self.env.user.name),
#                           partner_ids=[self.client_id.id])
                          
        self.write({
            'state': 'va',
            'description': 'facture valide le: ' +
                           fields.datetime.now().strftime('%d/%m/%Y %H:%M')
        })
        return True

     def fctvente_payer(self):
        self.write({'state': 'pa'})
        return True

     def fctvente_annuler(self):
        if self.valid:
            raise ValidationError("Cette facture est verouillee!")
        self.write({'state': 'an'})
        return True
#      
class Attachment(models.Model):
 
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
      
     facturevente = fields.Many2one(
        'gctjara.facturevente',
        string="Facture"
    )  
