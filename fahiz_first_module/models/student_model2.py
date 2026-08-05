from odoo import models,fields

class DepartmentModel(models.Model):
    _name = "department.one"
    _description = "this is department model"

    

    name = fields.Char(string="Department Name", required=False)
    code = fields.Char(string="Department Code")
    description = fields.Text(string="Description")
    established_date = fields.Date(string="Established Date")
    active = fields.Boolean(string="Active", default=True)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('inactive', 'Inactive')
        ],
        string="Status",
        default='draft'
    )

    student_ids = fields.One2many(
    'student.one',
    'department_id',
    string="Students"
)