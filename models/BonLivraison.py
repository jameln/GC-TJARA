# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

        inverse_name='bonlivraison_id'
         )
     
     
     commande_id = fields.Many2one(
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
       self.write({'state': 'lv'})
       sequences = self.env['ir.sequence'].next_by_code('gctjara.facturevente.seq') 
       record = self.env['gctjara.facturevente'].create({
             
             'numero' :  sequences,
             'datefact': self.datereception,
             'client_id':self.client_id.id,
             'commande_id' : self.id,
 
           })

       for rec in self:
           for r in rec.lignebonlivraison_id :
               r.bonlivraison_id = record.id
               record1 = self.env['gctjara.lignefactvente'].create({
                   'quantite':r.quantite,
                   'embalageproduit_id':r.embalageproduit_id.id,
                   'prix_total':r.prix_total,
                   'facture_id':record.id,
                   'prixunit':r.prixunit,
                   'tva':r.tva
                   })
       if self.creat_mvtstock():
            self.maj_produits()

       return True

 
     @api.multi
     def creat_mvtstock(self):
       self.write({'state': 'lv'})
       sequencesmvt = self.env['ir.sequence'].next_by_code('gctjara.mvtstock.seq')
       self.env['gctjara.mvtstock'].create({
             'numero' :  sequencesmvt,
             'date': fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
             'quantite':self.quantite,
             'produit':self.produit.id,
             'bonlivraison_id': self.id,
             'type':'Sortie'

           })

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


     @api.multi
     def maj_produits(self):
       qteprod = int(self.produit.quantitestocke) - int(self.quantite)

       product = self.env['gctjara.produitemballee']
       product_id = self.produit.id
       package_product = product.browse(product_id)
       package_product.quantitestocke = qteprod

       return True


