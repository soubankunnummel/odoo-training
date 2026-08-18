from odoo import fields, models


class Subject(models.Model):
    _name = 'student.subject'
    _description = 'Subject'
    # _order = 'name'

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Subject Code', required=True)
    credits = fields.Float(string='Credits')
    department_id = fields.Many2one('student.department', string='Department')
    student_ids = fields.Many2many('student.registration', string='Students')
    active = fields.Boolean(string='Active', default=True)

    _unique_subject_code = models.Constraint(
        'UNIQUE(code)',
        'Subject code must be unique!'
    )
    department_code = fields.Char(related="department_id.code", string ="Dept Code",readonly=True)
