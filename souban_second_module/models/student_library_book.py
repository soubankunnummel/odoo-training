from odoo import api, fields, models


class StudentLibraryBook(models.Model):
    _name = 'student.library.book'
    _description = 'Library Book'

    name = fields.Char(string='Book Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN')
    available = fields.Boolean(string='Available', default=True)
    borrower_id = fields.Many2one('student.registration', string='Borrowed By')
    category = fields.Selection([
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('textbook', 'Textbook'),
    ], string='Category')

    @api.onchange('borrower_id')
    def _onchange_borrower_id(self):
        for record in self:
            if record.borrower_id:
                record.available = False
            else:
                record.available = True

    def action_borrow_book(self):
        """Borrow book - Operator (4) Link"""
        self.ensure_one()
        if not self.available:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Cannot Borrow',
                    'message': 'This book is already borrowed.',
                    'type': 'warning',
                },
            }
        if not self.borrower_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Select Student',
                    'message': 'Please select a student first.',
                    'type': 'warning',
                },
            }
        self.write({'available': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Book Borrowed',
                'message': f'{self.name} borrowed by {self.borrower_id.name}.',
                'type': 'success',
            },
        }

    def action_return_book(self):
        """Return book - Operator (3) Unlink"""
        self.ensure_one()
        self.write({'borrower_id': False, 'available': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Book Returned',
                'message': f'{self.name} returned successfully.',
                'type': 'success',
            },
        }
