# -*- coding: utf-8 -*-

from odoo import models, fields, api

import Client
import Fournisseur
import Produits
import Emballage
# import Stock
import CommandeClient
import CommandeFournisseur
# import FactureVente
# import FactureAchat
# import ReglementAchat
# import ReglementVente
# import BonEntree
# import BonLivraison
# import LigneCommandeAchat
# import LigneCommandeVente
# import LigneFactureAchat
# import LigneReglementAchat
# import LigneReglementVente
# import LigneFactureVente
# import MouvementStock
import Depot
# import LigneProduitEmballage


# class gc-tjara(models.Model):
#     _name = 'gc-tjara.gc-tjara'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
