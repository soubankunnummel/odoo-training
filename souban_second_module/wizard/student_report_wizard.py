import base64
from odoo import models, fields, api


class StudentReportWizard(models.TransientModel):
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    department_id = fields.Many2one('student.department', string='Department')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ], string='State')
    report_format = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'Excel'),
    ], string='Report Format', required=True, default='pdf')

    def action_generate_report(self):
        domain = []

        if self.date_from:
            domain.append(('register_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('register_date', '<=', self.date_to))
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        if self.state:
            domain.append(('state', '=', self.state))

        students = self.env['student.registration'].search(domain)

        if not students:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Records',
                    'message': 'No students found matching your filter.',
                    'type': 'warning',
                    'sticky': False,
                },
            }

        if self.report_format == 'xlsx':
            ids_str = ','.join(str(id) for id in students.ids)
            return {
                'type': 'ir.actions.act_url',
                'url': '/student/xlsx/report?ids=%s' % ids_str,
                'target': 'self',
            }
        else:
            valid_students = students.filtered(lambda s: s.exists())
            if not valid_students:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'No Records',
                        'message': 'No valid students found.',
                        'type': 'warning',
                        'sticky': False,
                    },
                }
            return self.env.ref('souban_second_module.action_student_report_custom').report_action(valid_students)
