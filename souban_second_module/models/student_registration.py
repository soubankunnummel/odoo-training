from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    _name = "student.registration"
    _description = "Student Registration"
    # _order = 'id desc'

    name = fields.Char(string="Student Name", required=True)
    student_code = fields.Char(
        string="Student Code",
        readonly=True,
        required=True,
        copy=False,
        index="trigram",
        default=lambda self: _("New"),
    )
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    active = fields.Boolean(string="Active", default=True)
    photo = fields.Image(string="Photo")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender"
    )
    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("completed", "Completed")],
        string="State",
        default="draft",
    )

    # relatoinal fields
    department_id = fields.Many2one("student.department", string="Department")
    subject_ids = fields.Many2many("student.subject", string="Subjects")
    register_date = fields.Date(string="Register Date", default=fields.Date.today)
    notes = fields.Text(string="Notes")


    # compute field
    classmate_count = fields.Integer(compute="_compute_classmate_count")

    # sql constraine
    _unique_student_emails = models.Constraint("UNIQUE(email)", "Email already exists!")

    # related fields
    subject_department_code = fields.Char(
        related='subject_ids.department_id.code',
        string='Subject Dept Code',
        readonly=True
    )
    user_id = fields.Many2one('res.users',string ="Related User")
    user_email = fields.Char(related='user_id.email',string="Related user Email",readonly=True)
    user_name = fields.Char(related='user_id.name',string="Related user Name",readonly=True)
    guardian_id = fields.Many2one('res.partner', string='Guardian')
    guardian_email = fields.Char(related='guardian_id.email', string='Guardian Email', readonly=True)
    guardian_phone = fields.Char(related='guardian_id.phone', string='Guardian Phone', readonly=True)
    guardian_name = fields.Char(related='guardian_id.name', string='Guardian Name', readonly=True)





    @api.depends("department_id")
    def _compute_classmate_count(self):
        for rec in self:
            if rec.department_id:
                rec.classmate_count = self.env["student.registration"].search_count(
                    [("department_id", "=", rec.department_id.id)]
                )
            else:
                rec.classmate_count = 0

    def action_view_classmates(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Classmates",
            "res_model": "student.registration",
            "view_mode": "list,form",
            "domain": [("department_id", "=", self.department_id.id)],
            "target": "new",
        }

    @api.onchange("department_id")
    def _onchange_department(self):
        if self.department_id:
            self.subject_ids = self.department_id.subject_ids.ids

    @api.constrains("age")
    def _check_age(self):
        for record in self:
            if record.age is not None and (record.age < 1 or record.age > 100):
                raise ValidationError("Age must be between 1 and 100.")

    def action_confirm(self):
        self.state = "confirmed"

    def action_set_draft(self):
        self.state = "draft"

    def action_complete(self):
        self.state = "completed"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("student_code") or vals.get("student_code") == _("New"):
                vals["student_code"] = self.env["ir.sequence"].with_company(
                    vals.get("company_id")
                ).next_by_code("student.registration") or _("New")

        students = super().create(vals_list)
        template = self.env.ref('souban_second_module.email_template_student_welcome')
        for student in students:
            if student.email:
                template.send_mail(student.id, force_send=True)
        return students

    def action_deactivate(self):
        self.write({"active": False})

    def unlink(self):
        for rec in self:
            if rec.state == "confirmed":
                raise ValidationError(_("Confirmed students cannot be deleted."))

        return super().unlink()

    def action_read_recent_students(self):
        recent_students = self.search([], order="register_date desc", limit=5)
        if not recent_students:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Recent Students",
                    "message": "No recent students found.",
                    "type": "warning",
                    "sticky": False,
                },
            }
        return {
            "type": "ir.actions.act_window",
            "name": "Recent Students",
            "res_model": "student.registration",
            "view_mode": "list,form",
            "domain": [("id", "in", recent_students.ids)],
            "target": "new",
        }

    def action_duplicate_active_students(self):
        duplicated_students = self.filtered(lambda rec: rec.active)
        copies = []
        for student in duplicated_students:
            copied = student.copy({"name": f"{student.name} (Copy)"})
            copies.append(copied)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Duplicate Active",
                "message": f"Duplicated {len(copies)} active student(s).",
                "type": "success",
                "sticky": False,
            },
        }

    def action_bulk_confirm_draft(self):
        draft_students = self.filtered(lambda r: r.state == "draft")
        draft_students.action_confirm()

    def action_bulk_draft_confirm(self):
        draft_students = self.filtered(lambda r: r.state == "confirmed")
        draft_students.action_set_draft()

    def action_change_department(self):
        wizard = self.env["student.transfer.wizard"].create(
            {"student_ids": [(6, 0, self.ids)]}
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Transfer Students",
            "res_model": "student.transfer.wizard",
            "res_id": wizard.id,
            "view_mode": "form",
            "target": "new",
        }

    # cron job fn
    @api.model
    def _cron_auto_complete_students(self):
        confirmed_students = self.search([
            ('state' , '=', 'confirmed')
        ])
        for student in confirmed_students:
            if student.register_date:
                days = (fields.Date.today() - student.register_date).days
                if days >= 30:
                    student.action_complete()

    @api.model
    def _cron_auto_deactivate_old_students(self):
        students = self.search([
            ('department_id','=',False),
            ('active','=',True)
        ])
        for student in students:
            if student.register_date:
                days = (fields.Date.today() - student.register_date).days
                if days >= 60 :
                    student.action_deactivate()

    @api.model
    def _cron_send_completion_reminder(self):
        print("--------------------working-----------------------------------")
        print("--------------------working-----------------------------------")

        confirmed_students = self.search([
        ('state', '=', 'confirmed'),
        ('register_date', '!=', False),
        ('email', '!=', False),
        ])
        template = self.env.ref('souban_second_module.email_template_completion_reminder')
        for student in confirmed_students:
            days = (fields.Date.today() - student.register_date).days
            if 7 <= days < 30:
            # if days >= 0:
                template.send_mail(student.id, force_send=True)

    # def action_print_xlsx(self):
    #     import base64
    #     report = self.env['report.souban_second_module.student_xlsx_report']
    #     file_data = report.generate_xlsx(self.ids)
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Student_Report.xlsx',
    #         'type': 'binary',
    #         'datas': base64.b64encode(file_data),
    #         'res_model': 'student.registration',
    #         'res_id': self.ids[0],
    #     })
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': '/web/content/%d?download=true' % attachment.id,
    #         'target': 'self',
    #     }
    def action_print_xlsx(self):
            return {
                'type': 'ir.actions.act_url',
                'url': '/student/xlsx/report/%d' % self.ids[0],
                'target': 'self',
            }

