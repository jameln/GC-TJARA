# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommandeFournisseur(models.Model):
     _name = 'gctjara.cmdfournisseur'
     
     _rec_name = 'numero'
     
     _inherit='mail.thread'
     
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
                            help='Date création',
                            readonly=True)
     
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
        string='Confirmé',
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

     lignecmd_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignecmdachat',
        inverse_name='commande_id'
         )

     montant_ht = fields.Float(
         string='Montant HT',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    ) 
     
     montant = fields.Float(
         string='Montant TTC',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
    
     @api.multi
     @api.depends("lignecmd_id")
     def _montant_totale(self):
       montanttot=0
       montantht=0
       for rec in self :
           for lca in rec.lignecmd_id:
                   montanttot += lca.prix_total 
                   montantht +=lca.prix_ht
       self.montant=montanttot
       self.montant_ht=montantht

 
      
  
     
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
                    'prix_ht': r.prix_ht,
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
