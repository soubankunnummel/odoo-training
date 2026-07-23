from odoo import models, fields

class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    bio_html = fields.Html(string="Bio")

    age = fields.Integer(string="Age")
    marks = fields.Float(string="Marks")

    is_active = fields.Boolean(
        string="Is Active",
        default=True
    )

    date_of_birth = fields.Date(
        string="Date Of Birth",
        required=True
    )

    register_time = fields.Datetime(
        string="Register Time"
    )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")

    image = fields.Image(
        string="Student Photo"
    )

    document = fields.Binary(
        string="Document"
    )

    document_name = fields.Char(
        string="File Name"
    )

    student_class = fields.Selection([
    ('a', 'Class A'),
    ('b', 'Class B'),
    ('c', 'Class C'),
    ], string="Class")