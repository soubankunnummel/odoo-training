{
    'name': 'Student Management Training',
    'version': '19.0.0.9',
    'summary': 'Simple module for student registration, departments and subjects',
    'description': 'A simple Odoo training module with registration, department and subject models.',
    'category': 'Training',
    'author': 'Truslink Trading LLC',
    'website': 'https://trusholding.com/',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/ir_cron_job.xml',
        'data/mail_template_data.xml',
        'reports/student_report.xml',
        'reports/student_report_templates.xml',
        'reports/student_report_custom.xml',
        'reports/student_report_custom_templates.xml',
        'wizard/student_transfer_wizard_views.xml',
        'wizard/student_update_wizard_views.xml',
        'wizard/student_report_wizard_views.xml',
        'views/student_dashboard.xml',
        'views/department_views.xml',
        'views/subject_views.xml',
        'views/student_registration_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}



