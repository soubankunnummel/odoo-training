from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import date


class StudentModel(models.Model):
    _name = "student.one"
    _description = "this is student model"

    name = fields.Char(string = "Name")
    description = fields.Text(string = "Description")
    age = fields.Integer(string = "Age")
    salary = fields.Float(string = "Salary")
    marks = fields.Float(string = "Marks")
    dob = fields.Date(string = "Date of Birth")
    joining_datetime = fields.Datetime(string = "Joining Time")
    gender = fields.Selection([('male','Male'),('female','Female')],string = "Gender")
    image = fields.Image(string="Student Photo")
    document = fields.Binary(string="Document")
    document_name = fields.Char(String ="File Name")
    state = fields.Selection([
    ('draft', 'Draft'),
    ('confirm', 'Confirmed'),
    ('cancel', 'Cancelled'),
    ('done', 'Done')
    ], string="Status",default='draft')

    # relational fields

    department_id = fields.Many2one('department.one', string="Department Name")

    user_id = fields.Many2one('res.users',string="Academic Counsellor" )

    # many2many field to link student with certifications

    certification_ids = fields.Many2many(
        'certification.one', #target model
        'student_certification_rel', #table name
        'student_id', #current model field
        'certification_id', #target model field
        string="Certifications"
    )
    ce_marks = fields.Float(string="Certification Marks")
    total_marks = fields.Float(string="Total Marks", compute="_compute_total_marks", store=True)

    expiry_date = fields.Date(string="Expiry Date")
    is_expired = fields.Boolean(string = "Expired", compute="_compute_is_expired", store=True)



    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        if self.age < 18:
            raise ValidationError("Student age must be greater than 18")
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_done(self):
        self.state = 'done'

    @api.onchange('gender')
    def _onchange_gender(self):
        if self.gender == 'male':
            self.description = "This is a male student"
        elif self.gender == 'female':
            self.description = "This is a female student"
        elif self.gender == 'other':
            self.description = "This is a student with other gender"
        else:
            self.description = ""

    @api.onchange('marks')
    def _onchange_marks(self):
        if self.marks < 0:
            raise ValidationError("Marks cannot be negative")
        elif self.marks > 1000:
            raise ValidationError("Marks cannot be greater than 1000")
        else:
            self.description = "Marks are within the valid range"

    @api.depends('marks','ce_marks')
    def _compute_total_marks(self):
        for rec in self:
            rec.total_marks = rec.marks + rec.ce_marks

    
    @api.depends('expiry_date')
    def _compute_is_expired(self):
        for rec in self:
            rec.is_expired = rec.expiry_date and rec.expiry_date < date.today()

        




