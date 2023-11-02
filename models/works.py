from odoo import models, fields, api, _


class WorkAssignmentCheckList(models.Model):
    _name = 'work.assignment.check.list'
    _description = 'Work Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    branch = fields.Selection([('corporate_office', 'Corporate Office'), ('cochin_campus', 'Cochin Campus'),
                               ('kottayam_campus', 'Kottayam Campus'), ('calicut_campus', 'Calicut Campus'),
                               ('malappuram_campus', 'Malappuram Campus'), ('trivandrum_campus', 'Trivandrum Campus'),
                               ('palakkad_campus', 'Palakkad Campus'), ('dubai_campus', 'Dubai Campus')],
                              string='Branch')
    work_ids = fields.One2many('works.lists', 'work_id', string='Works')
    date = fields.Date(string='Date')

    @api.onchange('branch')
    def _batch_class_rooms(self):
        self.class_room_id = False
        class_room = self.env['check.list.class.room'].sudo().search([('branch', '=', self.branch)])
        rec = []
        rec.clear()
        for room in class_room:
            rec.append(room.id)
        domain = [('id', 'in', rec)]
        return {'domain': {'class_room_id': domain}}

    class_room_id = fields.Many2one('check.list.class.room', string='Class Room',
                                    domain=_batch_class_rooms)


class WorksLists(models.Model):
    _name = 'works.lists'
    _description = 'Works Lists'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    work = fields.Many2one('work.lists.check.list', string='Works')
    assign_to = fields.Many2one('res.users', string='Assign To')
    work_id = fields.Many2one('work.assignment.check.list', string='Work')


class WorkListsCheckList(models.Model):
    _name = 'work.lists.check.list'
    _description = 'Work Lists'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
