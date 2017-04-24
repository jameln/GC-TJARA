# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommandeFournisseur(models.Model):
     _name = 'gctjara.cmdfournisseur'
     
     numero = fields.Char(
         string='Numero ',
         default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.cmdfrs.seq')
     )
     
     datecommande = fields.Date('Date',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date création')
     
     datereception = fields.Date('Date de reception',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date   reception  de la commande ')
     
     description = fields.Text(
         String='Description'
         )
     
     fournisseur_id = fields.Many2one(
                                    comodel_name='gctjara.fournisseur',
                                    string="Fournisseur",
                                    ondelete='restrict'
                                   )
      
     attachment = fields.One2many(
         'ir.attachment',
         'cmdfournisseur',
         string='Pièces jointes'
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
        result = super(CommandeFournisseur, self).write(values)
        return result

     @api.multi
     def afficher(self):
        print "afficher()"
        raise ValidationError('id commande : ' + str(self.id))
        return True

     def cmdfrs_brouillon(self):

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
     def cmdfrs_valider(self):
              
        self.write({
            'state': 'va',
            'description': 'Commande fournisseur valide le: ' +
                           fields.datetime.now().strftime('%d/%m/%Y %H:%M')
        })
    
        self.env['gctjara.factureachat'].write({
                'numero' :  "ff",#lambda self: self.env['ir.sequence'].next_by_code('gctjara.factureachat.seq'),
                'datefact': self.datereception
                })

               
        return True

     def cmdfrs_terminer(self):
        self.write({'state': 'tr'})
        return True
    
     def cmdfrs_annuler(self):
        if self.valid:
            raise ValidationError("Cette commande fournisseur est verouillee!")
        self.write({'state': 'an'})
        return True
class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     cmdfournisseur = fields.Many2one(
        'gctjara.cmdfournisseur',
        string="Pièces jointes"
    ) 
     

#      lignecmd_id = fields.One2many(string='Lignes commande',
#                           comodel_name='gctjara.lignecmdachat',
#                           inverse_name='commande_id',
#                           )
#       

# 
#      facture_id = fields.One2many(string='Lignes Facture',
#                          comodel_name='gctjara.factureachat',
#                          inverse_name='commande_id',
#                          )