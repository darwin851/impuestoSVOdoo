# -*- coding: utf-8 -*-
{
    'name': "Reportes de Impuestos El Salvador",

    'summary': """
        Genera reportes para impuestos en El Salvador""",

    'description': """
        Genera los siguientes reportes:
            - F1 IVA
            - F2 Renta
            - Libro de IVA Compras
            - Libro de IVA Ventas
    """,

    'author': "Darwin González",
    'website': "https://www.lcgroup.tech, versión 17 community",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Localizations/Account Charts',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/f1_iva_view.xml',
        'views/f2_renta_view.xml',
        'views/libro_iva_compras_view.xml',
        'views/libro_iva_ventas_view.xml',
        'wizard/f1_iva_wizard_view.xml',
        'wizard/f2_renta_wizard_view.xml',
        'wizard/libro_iva_compras_wizard_view.xml',
        'wizard/libro_iva_ventas_wizard_view.xml',
        'views/maintenance_menus.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
