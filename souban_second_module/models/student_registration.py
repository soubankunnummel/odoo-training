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

    classmate_count = fields.Integer(
        compute='_compute_classmate_count'
    )

    _unique_student_emails = models.Constraint(
        'UNIQUE(email)',
        'Email already exists!'
    )

    @api.depends('department_id')
    def _compute_classmate_count(self):
        for rec in self:
            if rec.department_id:
                rec.classmate_count = self.env['student.registration'].search_count([
                    ('department_id', '=', rec.department_id.id)
                ])
            else:
                rec.classmate_count = 0

    def action_view_classmates(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Classmates',
            'res_model': 'student.registration',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.department_id.id)],
            'target': 'new',
        }

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
        self.state = 'confirmed'

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

    def action_deactivate(self):
        self.write({
            'active': False
        })

    def unlink(self):
        for rec in self:
            if rec.state == 'confirmed':
                raise ValidationError(
                    _("Confirmed students cannot be deleted.")
                )

        return super().unlink()

    # def action_remove_student(self):
    #     name = self.name
    #     self.unlink()
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': 'Remove Student',
    #             'message': f"Deleted student {name}.",
    #             'type': 'success',
    #             'sticky': False,
    #         },
    #     }

    def action_read_recent_students(self):
        recent_students = self.search([], order='register_date desc', limit=5)
        if not recent_students:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Recent Students',
                    'message': 'No recent students found.',
                    'type': 'warning',
                    'sticky': False,
                },
            }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recent Students',
            'res_model': 'student.registration',
            'view_mode': 'list,form',
            'domain': [('id', 'in', recent_students.ids)],
            'target': 'new',
        }


    def action_duplicate_active_students(self):
        duplicated_students = self.filtered(lambda rec: rec.active)
        copies = []
        for student in duplicated_students:
            copied = student.copy({
                'name': f"{student.name} (Copy)"
            })
            copies.append(copied)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Duplicate Active',
                'message': f"Duplicated {len(copies)} active student(s).",
                'type': 'success',
                'sticky': False,
            },
        }




