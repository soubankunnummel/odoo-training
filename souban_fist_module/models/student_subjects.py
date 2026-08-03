from odoo import models, fields, api


class StudentSubjects(models.Model):
    _name = 'student.subjects'
    _descriptoin = 'Student Subjects'

    name = fields.Char(string = "Subject")
