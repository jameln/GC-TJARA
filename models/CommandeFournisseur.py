# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommandeFournisseur(models.Model):
     _name = 'gctjara.cmdfournisseur'
     
     _rec_name = 'numero'
     
     numero = fields.Char(
         string='Numero ',
        # default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.cmdfrs.seq')
        default=lambda self: self._newrecord(),
        store=True,
        readonly=True
        
     )
     @api.model
     def _newrecord(self):
         sequence = self.env['ir.sequence'].search([('code','=','gctjara.cmdfrs.seq')])
         next= sequence.get_next_char(sequence.number_next_actual)
         return next
     
     @api.model
     def create(self, vals):
        vals['numero'] = self.env['ir.sequence'].next_by_code('gctjara.cmdfrs.seq')
        return super(CommandeFournisseur, self).create(vals)
     
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
#      produitembalee=fields.Many2many(
#          string='Produits',
#          comodel_name='gctjara.produitemballee',
#          relation='lignecommandeachat',
#          column1='commande_id',
#          column2='embalageproduit_id'
#         
#          )
#      
     lignecmd_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignecmdachat',
        inverse_name='commande_id'
         )
      



#  
#      facture_id = fields.Many2one(
#          string='Facture',
#          comodel_name='gctjara.factureachat',
         
#                         )
     
     montant = fields.Float(
         string='Montant',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
    
     @api.one
     @api.depends("lignecmd_id")
     def _montant_totale(self):
       montanttot=0
       for lca in self.lignecmd_id:
               montanttot = montanttot + lca.prix_total 
       self.montant=montanttot
 
      
  
     
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
            
#      @api.multi
#      @api.depends('lignecmd_id')
#      def ligneproduit(self):
#         for rec in self :
#             for r in self.lignecmd_id :
#                 r.produit_ids=rec.lignecmd_id
#                 r.quantite= rec.lignecmd_id.quantite
#                 r.prix_tot= rec.lignecmd_id.prix_total
            
     def create_factachat(self):
        sequences = self.env['ir.sequence'].next_by_code('gctjara.factureachat.seq') 
        record = self.env['gctjara.factureachat'].create({
            
              'numero' :  sequences,
              'datefact': self.datereception,
              'fournisseur_id':self.fournisseur_id.id,
              'commande_id' : self.id, 

            })
        
        for rec in self:
            for r in rec.lignecmd_id :
                r.reffact=  record.id
                record1 = self.env['gctjara.lignefactachat'].create({
                    'quantite':r.quantite,
                    'embalageproduit_id':r.embalageproduit_id.id,
                    'prix_total':r.prix_total,
                    'facture_id':record.id,
                    'prixunit':r.prixunit,
                    'tva':r.tva
                    })
        return True
    
     def create_bon_entree(self):
          for rec in self:
              for r in rec.lignecmd_id :
                  rec.env['gctjara.bonentree'].create({
                      'numero':self.env['ir.sequence'].next_by_code('gctjara.bonentree.seq') ,
                      'date':fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
                      'produit' : r.embalageproduit_id.id,
                      'quantite': str(r.quantite)
                      })   
          
          return True
    
    
    
     @api.one
     def cmdfrs_valider(self):
      
        self.write({
            'state': 'va',
            'description': 'Commande fournisseur valide le: ' + fields.datetime.now().strftime('%d/%m/%Y %H:%M'),
            })
        self.create_factachat()

        return True

     def cmdfrs_terminer(self):
        self.write({'state': 'tr'})
        self.create_bon_entree()
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
