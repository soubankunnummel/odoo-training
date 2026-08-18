from odoo import models, fields, api


class StudentTransferWizard(models.TransientModel):
    _name = 'student.transfer.wizard'
    _description = 'Transfer Students to Department'

    department_id = fields.Many2one(
        'student.department',
        string='Target Department',
        # required=True,
    )
    student_ids = fields.Many2many(
        'student.registration',
        string='Students to Transfer',
    )


    def action_confirm_transfer(self):
        if not self.department_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Department',
                    'message': 'Please select a target department.',
                    'type': 'warning',
                    'sticky': False,
                },
            }
        for student in self.student_ids:
            student.write({
                'department_id': self.department_id.id,
                'subject_ids': [(6, 0, self.department_id.subject_ids.ids)],
                'state': 'draft',
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Transfer Complete',
                'message': f"{len(self.student_ids)} student(s) moved to {self.department_id.name}.",
                'type': 'success',
                'sticky': False,
            },
        }