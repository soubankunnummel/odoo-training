from odoo import fields, models, api


class StudentBookWishlist(models.Model):
    _name = 'student.book.wishlist'
    _description = 'Book Wishlist'

    student_id = fields.Many2one('student.registration', string='Student', required=True)
    book_ids = fields.Many2many('student.library.book', string='Wishlist Books')
    note = fields.Text(string='Note')

    def action_add_wishlist_books_to_borrow(self):
        for record in self:
            for book in record.book_ids:
                book.write({'borrower_id': record.student_id.id, 'available': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Books Borrowed',
                'message': f'{len(record.book_ids)} book(s) borrowed.',
                'type': 'success',
            },
        }
