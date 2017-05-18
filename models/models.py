# -*- coding: utf-8 -*-

from odoo import models, fields, api

import BonEntree
import BonLivraison
import Client
import Fournisseur
import CommandeClient
import CommandeFournisseur
import FactureAchat
import FactureVente
import Produits
import Emballage
import ReglementAchat
import ReglementVente
import LigneCommandeAchat
import LigneCommandeVente
import LigneFactureAchat
import amount_to_text_fr
import LigneBonLivraison
import LigneFactureVente
import ProduitEmballee
import MouvementStock



