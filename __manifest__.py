# -*- coding: utf-8 -*-
{
    'name': "GC-TJARA",

    'summary': """
    Dans le cadre de PFE de Mr JAMEL NEFZI :
         Solution pour la gestion de l'activité commerciale d'une entreprise (PME)

""",

    'description': """
        Application Gestion commercial T-JARA pour les PME 
    """,

    'author': "Khidma",
    'website': "http://khidma.tn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','report','board','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/BonEntree.xml',
        'views/BonLivraison.xml',
        'views/Client.xml',
        'views/Fournisseur.xml',
        'views/CommandeClient.xml',
        'views/CommandeFournisseur.xml',
        'views/FactureAchat.xml',
        'views/FactureVente.xml',
        'views/ReglementAchat.xml',
        'views/ReglementVente.xml',
        'views/Depot.xml',
        'views/Stock.xml',
        'views/Produits.xml',
        'views/MouvementStock.xml',
        'views/Emballages.xml',
              
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
    'css' : ['static/src/css/*.css']
}