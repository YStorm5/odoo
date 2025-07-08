{
    'name': 'POS UOM Selector',
    'version': '1.0',
    'author': 'Panha',
    'website':'https://github.com/YStorm5',
    'category': 'Point of Sale',
    'summary': 'Allow selecting different UOMs in POS with different prices',
    'depends': ['point_of_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/inherited_product_template_views.xml",
        "views/inherited_pos_order_view.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_uom_selector/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
}