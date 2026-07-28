from odoo import models,fields

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
    student_class = fields.Selection([
    ('a', 'Class A'),
    ('b', 'Class B'),
    ('c', 'Class C'),
    ], string="Class")




