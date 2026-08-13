from odoo import models, fields, api


class StudentDashboardStateLine(models.Model):
    _name = 'student.dashboard.state.line'
    _description = 'Students by State Line'

    dashboard_id = fields.Many2one('student.dashboard')
    state = fields.Char(string='State')
    count = fields.Integer(string='Count')


class StudentDashboardEmailLine(models.Model):
    _name = 'student.dashboard.email.line'
    _description = 'Active Student Email Line'

    dashboard_id = fields.Many2one('student.dashboard')
    email = fields.Char(string='Email')


class StudentDashboardExistsLine(models.Model):
    _name = 'student.dashboard.exists.line'
    _description = 'Record Existence Check Line'

    dashboard_id = fields.Many2one('student.dashboard')
    description = fields.Char(string='Check')
    result = fields.Boolean(string='Exists')


class StudentDashboard(models.Model):
    _name = 'student.dashboard'
    _description = 'Student Dashboard'

    name = fields.Char(string='Dashboard Name', default='Student Dashboard')

    total_students = fields.Integer(compute="_compute_student_statistics")
    draft_students = fields.Integer(compute='_compute_student_statistics')
    confirmed_students = fields.Integer(compute='_compute_student_statistics')
    confirmed_students_ids = fields.One2many(
        'student.registration',
        compute='_compute_confirmed_students',
    )
    state_line_ids = fields.One2many(
        'student.dashboard.state.line',
        'dashboard_id',
        compute='_compute_state_lines',
    )
    email_line_ids = fields.One2many(
        'student.dashboard.email.line',
        'dashboard_id',
        compute='_compute_email_lines',
    )
    all_students = fields.Integer(
        string='All Students',
        compute='_compute_with_context',
    )
    inactive_students = fields.Integer(
        string='Inactive Students',
        compute='_compute_with_context',
    )
    browsed_student_ids = fields.One2many(
        'student.registration',
        compute='_compute_browsed_student',
    )
    all_student_ids = fields.One2many(
        'student.registration',
        compute='_compute_all_students',
    )
    exists_line_ids = fields.One2many(
        'student.dashboard.exists.line',
        'dashboard_id',
        compute='_compute_exists',
    )

    def read(self, fields=None, load='_classic_read'):
        self.env.clear()
        return super().read(fields, load)

    @api.depends()
    def _compute_student_statistics(self):
        Student = self.env['student.registration']
        total = Student.search_count([])
        draft = Student.search_count([('state', '=', 'draft')])
        confirmed = Student.search_count([('state', '=', 'confirmed')])

        for rec in self:
            rec.total_students = total
            rec.draft_students = draft
            rec.confirmed_students = confirmed

    @api.depends()
    def _compute_confirmed_students(self):
        rows = self.env['student.registration'].search_read(
            [('state', '=', 'confirmed')], ['name']
        )
        ids = [row['id'] for row in rows]
        for rec in self:
            rec.confirmed_students_ids = [(6, 0, ids)]

    @api.depends()
    def _compute_state_lines(self):
        Student = self.env['student.registration']
        labels = dict(Student.fields_get(['state'])['state']['selection'])
        groups = Student.read_group([], ['state'], ['state'])

        for rec in self:
            rec.state_line_ids = [(5, 0, 0)] + [(0, 0, {
                'state': labels.get(group['state'], group['state']),
                'count': group['state_count'],
            }) for group in groups]

    @api.depends()
    def _compute_email_lines(self):
        students = self.env['student.registration'].search([])
        emails = students.filtered(lambda rec: rec.active).mapped('email')
        emails = sorted([email for email in emails if email])
        for rec in self:
            rec.email_line_ids = [(5, 0, 0)] + [(0, 0, {'email': email}) for email in emails]

    @api.depends()
    def _compute_with_context(self):
        Student = self.env['student.registration']
        active = Student.search_count([])
        all_records = Student.with_context(active_test=False).search_count([])
        for rec in self:
            rec.all_students = all_records
            rec.inactive_students = all_records - active

    @api.depends()
    def _compute_browsed_student(self):
        Student = self.env['student.registration']
        first = Student.search([], limit=1)
        for rec in self:
            if first:
                record = Student.browse(first.id)
                rec.browsed_student_ids = [(6, 0, [record.id])]
            else:
                rec.browsed_student_ids = [(5, 0, 0)]

    @api.depends()
    def _compute_all_students(self):
        students = self.env['student.registration'].search([])
        for rec in self:
            rec.all_student_ids = [(6, 0, students.ids)]

    @api.depends()
    def _compute_exists(self):
        Student = self.env['student.registration']
        first = Student.search([], limit=1)
        last = Student.search([], order='id desc', limit=1)
        existing_id = first.id if first else False
        missing_id = (last.id + 1) if last else 1
        for rec in self:
            lines = []
            if existing_id:
                lines.append((0, 0, {
                    'description': f'Existng Count({existing_id})',
                    'result': bool(Student.browse(existing_id).exists()),
                }))
            lines.append((0, 0, {
                'description': f'Not exist :({missing_id})',
                'result': bool(Student.browse(missing_id).exists()),
            }))
            rec.exists_line_ids = [(5, 0, 0)] + lines
