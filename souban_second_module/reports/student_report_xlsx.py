import io
import xlsxwriter
from odoo import models


class StudentReportXlsx(models.AbstractModel):
    _name = 'report.souban_second_module.student_xlsx_report'

    def generate_xlsx(self, record_ids):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Students')

        header = workbook.add_format({'bold': True, 'bg_color': '#875A7B', 'font_color': 'white'})

        sheet.write(0, 0, 'Student Code', header)
        sheet.write(0, 1, 'Name', header)
        sheet.write(0, 2, 'Age', header)
        sheet.write(0, 3, 'Email', header)
        sheet.write(0, 4, 'Gender', header)
        sheet.write(0, 5, 'Department', header)
        sheet.write(0, 6, 'Register Date', header)
        sheet.write(0, 7, 'State', header)

        students = self.env['student.registration'].browse(record_ids)

        for row, student in enumerate(students, 1):
            sheet.write(row, 0, student.student_code or '')
            sheet.write(row, 1, student.name or '')
            sheet.write(row, 2, student.age or 0)
            sheet.write(row, 3, student.email or '')
            sheet.write(row, 4, student.gender or '')
            sheet.write(row, 5, student.department_id.name or '')
            sheet.write(row, 6, str(student.register_date) if student.register_date else '')
            sheet.write(row, 7, student.state or '')

        workbook.close()
        output.seek(0)

        return output.read()
