from odoo import models, fields, api


class StudentSubjects(models.Model):
    _name = 'student.subjects'
    _description = 'Student Subjects'

    name = fields.Char(string = "Subject")
    class_id = fields.Many2one('student.class',string="Subjects")


