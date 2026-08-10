from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    _name = 'student.registration'
    _description = 'Student Registration'
    # _order = 'id desc'

    name = fields.Char(string='Student Name', required=True)
    student_code = fields.Char(string='Student Code', readonly=True, required=True, copy=False, index="trigram",  default=lambda self: _('New'))
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email')
    active = fields.Boolean(string='Active', default=True)
    photo = fields.Image(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed')
    ], string='State', default='draft')
    department_id = fields.Many2one('student.department', string='Department')
    subject_ids = fields.Many2many('student.subject', string='Subjects')
    register_date = fields.Date(string='Register Date', default=fields.Date.today)
    notes = fields.Text(string='Notes')

    _unique_student_emails = models.Constraint(
        'UNIQUE(email)',
        'Email alredy exists!'
    )

    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id:
            self.subject_ids = self.department_id.subject_ids.ids
        

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age is not None and (record.age < 1 or record.age > 100):
                raise ValidationError('Age must be between 1 and 100.')

    def action_confirm(self):
        self.state =  'confirmed'

    def action_set_draft(self):
        self.state = 'draft'

    def action_complete(self):
        self.state = 'completed'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('student_code') or vals.get('student_code') == _("New"):
                vals['student_code'] = self.env['ir.sequence'].with_company(
                    vals.get('company_id')
                ).next_by_code('student.registration') or _("New")

        return super().create(vals_list)

    @api.model
    def get_student_summary(self):
        return {
            'total': self.search_count([]),
            'draft': self.search_count([('state', '=', 'draft')]),
            'confirmed': self.search_count([('state', '=', 'confirmed')]),
        }

    def action_show_summary(self):
        summary = self.get_student_summary()
        message = (
            f"Total Students: {summary['total']}\n"
            f"Draft: {summary['draft']}\n"
            f"Confirmed: {summary['confirmed']}"
        )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Student Summary',
                'message': message,
                'type': 'success',
                'sticky': False,
            },
        }