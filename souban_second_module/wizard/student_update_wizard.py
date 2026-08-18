from odoo import models, fields, api


class UpdateStudent(models.TransientModel):
    _name = "student.update.wizard"
    _description = "Update Students"

    student_id = fields.Many2one(
        "student.registration", string="Student", required=True
    )
    name = fields.Char(string="Student Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender"
    )
    department_id = fields.Many2one("student.department", string="Department")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")

        if active_id:
            student = self.env["student.registration"].browse(active_id)
            res.update(
                {
                    "student_id": student.id,
                    "name": student.name,
                    "age": student.age,
                    "email": student.email,
                    "gender": student.gender,
                    "department_id": student.department_id.id,
                }
            )
            return res

    def action_update_student(self):
        self.student_id.write(
            {
                "name": self.name,
                "age": self.age,
                "email": self.email,
                "gender": self.gender,
                "department_id": self.department_id.id,
            }
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Update Complete",
                "message": f"Student {self.student_id.name} updated successfully.",
                "type": "success",
                "sticky": False,
            },
        }
