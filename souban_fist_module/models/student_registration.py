from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    bio_html = fields.Html(string="Bio")
    age = fields.Integer(string="Age")
    marks = fields.Float(string="Marks")
    is_active = fields.Boolean(string="Is Active", default=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    register_time = fields.Datetime(string="Register Time")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    image = fields.Image(string="Student Photo")
    document = fields.Binary(string="Document")
    document_name = fields.Char(string="File Name")
    # student_class = fields.Selection(
    #     [
    #         ("a", "Class A"),
    #         ("b", "Class B"),
    #         ("c", "Class C"),
    #     ],
    #     string="Class",
    # )
    student_class_id = fields.Many2one("student.class", string="Class")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("progress", "In Progress"),
            ("done", "Done"),
        ],
        default="draft",
    )

    subject_ids = fields.Many2many(
        'student.subjects',
        relation = 'student_subject_rel',
        column1= 'student_id',
        column2= 'subject_id',
        string = 'Subjects',

    )

    teachers_id = fields.Many2many(
        'res.users',
        relation = 'student_teacher_rel',
        column1 = 'studnet_id',
        column2 = 'teacher_id',
        string= 'Teachers'
    )


    advisor_id = fields.Many2one('res.users',string="Student Advisory", )

    def action_status_progres(self):
        self.state = "progress"

    def action_status_done(self):
        self.state = "done"

    def action_status_draft(self):
        self.state = "draft"

    def action_open_popup(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Student Details",
            "res_model": "student.student",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref("souban_fist_module.student_form_popup_view").id,
            "target": "new",
        }

    def action_edit_student(self):

        return {
            "type": "ir.actions.act_window",
            "res_model": "student.student",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref("souban_fist_module.student_model_form_view").id,
            "target": "current",
        }

    @api.constrains("age")
    def _check_age(self):
        for rec in self:
            if rec.age < 18:
                raise ValidationError(
                    "Student age must be greater than  to 18."
                )
