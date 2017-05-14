# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BonEntree(models.Model):
    
    _name = 'gctjara.bonentree'
    
    _rec_name='numero'
     
    numero = fields.Char(
        string='Numéro',
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.bonentree.seq'))
     
    date = fields.Date(
         string='Date bon d\'entrée',
         required=True,
         default=fields.datetime.now(),
         help='La date de  bon de livraison'
        )
    
    produit=fields.Many2one(
        string='Produits',
        comodel_name='gctjara.produitemballee')
    
    quantite=fields.Integer(string ='Quantité' , default=0)
      
    state = fields.Selection(
        string='Etat',
        default='nr',
        selection=[
            ('nr', 'non reçu'),
            ('rc', 'reçu'),
            ('lv', 'livrée'),
           
        ]
    )
    @api.multi 
    def action_draft(self):
        self.state = 'nr'
    @api.multi 
    def cmd_livree(self):
        self.write({'state': 'lv'})
        return True

    @api.multi  
    def creat_mvtstock(self):
        self.write({'state': 'rc'})
        sequencesmvt =   self.env['ir.sequence'].next_by_code('gctjara.mvtstock.seq') 
        self.env['gctjara.mvtstock'].create({
              'numero' :  sequencesmvt,
              'date': fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
              'quantite':self.quantite,
              'produit':self.produit.id,
              'bonentree_id': self.id,
              'type':'Entrée'
              
            })
        print "*************maj stock ******************* "
        self.maj_produits()
        print "*************fin stock stock ******************* "
        return True
    
    
    
    @api.multi 
    def maj_produits(self):
        qteprod= int(self.produit.quantitestocke) + int(self.produit.quantitestocke)
        for allrec in self.env['gctjara.produitemballee']:
             if allrec.id == self.produit.id:
                self.env['gctjara.produitemballee'].write({
                    'quantitestocke': qteprod,
                    })
        return True
    
    