# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BonLivraison(models.Model):
     _name = 'gctjara.bonlivraison'
     
        
     _rec_name = 'numero'
     
     numero = fields.Char(
        string='Numéro',
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.bonlivraison.seq')
        )
     
     date = fields.Date(
         string='Date bon livraison',
         required=True,
         default=fields.datetime.now(),
         help='La date de  bon de livraison'
        )
    

      
     state = fields.Selection(
        string='Etat',
        default='at',
        selection=[
            ('at', 'en attente'),
            ('lv', 'livrée'),
            ('an', 'annulée'),

        ]
     )
     
     client_id = fields.Many2one(
          string="Client",
          ondelete='restrict',
          comodel_name='gctjara.client'
                             )
     
     lignebonlivraison_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignebonlivraison',
        inverse_name='bonlivraison_id',
        store=True
         )
     
     
     commande_id = fields.Many2one(
         string='Commande',
         required=True,
         index=True,
         comodel_name='gctjara.cmdclient',
          
     )

     @api.multi
     def action_attente(self):
         self.state = 'at'

     @api.multi 
     def action_draft(self):
       self.state = 'an'

     @api.multi 
     def create_factvente(self):
       print("********************* Création du facture***********************")
       sequences = self.env['ir.sequence'].next_by_code('gctjara.facturevente.seq')
       record = self.env['gctjara.facturevente'].create({
             
             'numero' :  sequences,
             'datefact': self.date,
             'client_id':self.client_id.id,
             'bonlivraison_id' : self.id,
 
           })

       for rec in self:
           for rlf in rec.lignebonlivraison_id :
               print ("*******************Création du ligne facture*************")
               self.state = 'lv'
#                rlf.bonlivraison_id = record.id
               record1 = self.env['gctjara.lignefactvente'].create({
                   'quantite':rlf.quantite,
                   'embalageproduit_id':rlf.embalageproduit_id.id,
                   'prix_total':rlf.prix_total,
                   'facture_id':record.id,
                   'prixvente':rlf.prixvente,
                   'tva':rlf.tva
                   })
           self.creat_mvtstock()
       return True

 
     @api.multi
     def creat_mvtstock(self):
         for rec in self:
             for rbl in rec.lignebonlivraison_id:
                 print("*********Création mouvement de stock ****************")
                 sequencesmvt = self.env['ir.sequence'].next_by_code('gctjara.mvtstock.seq')
                 self.env['gctjara.mvtstock'].create({
                         'numero' :  sequencesmvt,
                         'date': fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
                         'quantite':rbl.quantite,
                         'produit':rbl.embalageproduit_id.id,
                         'bonlivraison_id': self.id,
                         'type':'Sortie'
                 })
         self.maj_produits()

         return True



     @api.multi
     def maj_produits(self):
         for rec in self:
             for rbl in rec.lignebonlivraison_id:
                 
                   qteprod = int(rbl.embalageproduit_id.quantitestocke) - int(rbl.quantite)
                   print("quantité stockée ====> " + str(qteprod))
                   if qteprod <= 0 :
                       raise ValidationError(
                           'Impossible de poursuit cette opération , le stock du ' + str(rbl.embalageproduit_id.name) + ' est épuisé')
                       return False
                   else :
                       product = self.env['gctjara.produitemballee']
                       product_id = rbl.embalageproduit_id.id
                       package_product = product.browse(product_id)
                       package_product.quantitestocke = qteprod
         return True


     def getProductID(self):
           if self.produit:
               return {
                   'name' : 'Produit',
                   'res_model':'gctjara.produitemballee',
                   'res_id':self.produit.id,
                   'view_type':'form',
                   'view_mode':'form',
                   'type':'ir.actions.act_window'

                   }
