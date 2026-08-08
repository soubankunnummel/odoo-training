{
    'name': 'Student Management Training',
    'version': '19.0.0.1',
    'summary': 'Simple module for student registration, departments and subjects',
    'description': 'A simple Odoo training module with registration, department and subject models.',
    'category': 'Training',
    'author': 'Truslink Trading LLC',
    'website': 'https://trusholding.com/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_views.xml',
        'views/subject_views.xml',
        'views/student_registration_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}



