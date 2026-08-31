from odoo import http
from odoo.http import request, content_disposition


class StudentXlsxController(http.Controller):

    @http.route('/student/xlsx/report/<int:record_id>', type='http', auth='user')
    def download_student_xlsx(self, record_id=None, **kw):
        report = request.env['report.souban_second_module.student_xlsx_report']
        file_content = report.generate_xlsx([record_id])

        filename = 'student_report.xlsx'

        return request.make_response(
            file_content,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition(filename))
            ]
        )