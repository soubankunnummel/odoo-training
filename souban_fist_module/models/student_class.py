from odoo import models,fields


class StudentClass(models.Model):
    _name = "student.class"
    _description = "Student Class"

    name = fields.Char(string="Class Name")
    code = fields.Char(string="Class Code")
    section = fields.Char(string="Section")
    academic_year = fields.Date(string="Academic Year")

    # teacher_id = fields.Many2one(
    #     'hr.employee',
    #     string="Class Teacher"
    # )

    student_ids = fields.One2many(
        'student.student',
        'student_class_id',
        string="Students"
    )



    subject_ids = fields.Many2many(
        'student.subjects',
        'class_subject_rel',
        'class_id',
        'subject_id',
        string = "Subjects"
    )

    # student_count = fields.Integer(
    #     string="Total Students",
    #     compute="_compute_student_count"
    # )

    active = fields.Boolean(default=True)