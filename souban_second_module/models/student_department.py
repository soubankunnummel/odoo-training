from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Department(models.Model):
    _name = 'student.department'
    _description = 'Department'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)

    student_ids = fields.One2many(
        'student.registration',
        'department_id'
    )

    subject_ids = fields.One2many(
        'student.subject',
        'department_id'
    )

    student_count = fields.Integer(
        compute='_compute_student_count'
    )

    subject_count = fields.Integer(
        compute='_compute_subject_count'
    )

    _unique_department_code = models.Constraint(
        'UNIQUE(code)',
        'Department code must be unique!'
    )

    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    @api.depends('subject_ids')
    def _compute_subject_count(self):
        for rec in self:
            rec.subject_count = len(rec.subject_ids)
