{
    'name': 'WellnessCheck',
    'version': '1.0',
    'summary': 'Empowering HR with Daily Wellness Insights',
    'description': 'A module for HR to track employee wellness through anonymous daily check-ins.',
    'category': 'Human Resources',
    'author': 'Antigravity',
    'depends': ['base', 'web', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/wellness_data.xml',
        'wizard/wellness_check_wizard_views.xml',
        'views/wellness_check_views.xml',
        'views/wellness_question_views.xml',
        'views/wellness_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'wellness_check/static/src/js/wellness_check_service.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
