from odoo import models, fields, api, _


class CheckList(models.Model):
    _name = 'logic.check.list'
    _description = 'Check List'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'class_id'

    branch = fields.Selection([('corporate_office', 'Corporate Office'), ('cochin_campus', 'Cochin Campus'),
                               ('kottayam_campus', 'Kottayam Campus'), ('calicut_campus', 'Calicut Campus'),
                               ('malappuram_campus', 'Malappuram Campus'), ('trivandrum_campus', 'Trivandrum Campus'),
                               ('palakkad_campus', 'Palakkad Campus'), ('dubai_campus', 'Dubai Campus')],
                              string='Branch', required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    assigned_date = fields.Date(string='Assigned Date')
    state = fields.Selection(selection=[
        ('draft', 'Draft'), ('completed', 'Completed'), ('cancelled', 'Cancelled')
    ], default='draft', string='State')
    reference_no = fields.Char(string='Works', required=True,
                               readonly=True, default=lambda self: _('New'))
    work_progress_ids = fields.One2many('work.progress', 'work_progress_id', string='Work Progress')

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'logic.check.list') or _('New')
        res = super(CheckList, self).create(vals)
        return res

    @api.onchange('branch')
    def _batch_class_rooms(self):
        self.class_id = False
        class_room = self.env['check.list.class.room'].sudo().search([('branch', '=', self.branch)])
        rec = []
        rec.clear()
        for room in class_room:
            rec.append(room.id)
        domain = [('id', 'in', rec)]
        return {'domain': {'class_id': domain}}

    class_id = fields.Many2one('check.list.class.room', string='Class Room', required=True, domain=_batch_class_rooms)

    @api.onchange('class_id', 'branch', 'assigned_date')
    def _onchange_work_progress(self):
        works = self.env['work.assignment.check.list'].sudo().search([])
        unlink_commands = [(3, child.id) for child in self.work_progress_ids]
        self.write({'work_progress_ids': unlink_commands})
        for work in works:
            datas = []

            if self.class_id == work.class_room_id and self.branch == work.branch and self.assigned_date == work.date:
                print(work.name, 'ola')

                for i in work.work_ids:
                    res_list = {
                        'works': i.work.id,
                        'assigned_to': i.assign_to.id,

                    }
                    datas.append((0, 0, res_list))
                self.work_progress_ids = datas

            else:
                # self.work_progress_ids.unlink()
                print('not work')

    def action_completed(self):
        self.state = 'completed'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_return_to_draft(self):
        self.state = 'draft'


class WorkProgress(models.Model):
    _name = 'work.progress'
    _description = 'Work Progress'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    works = fields.Many2one('work.lists.check.list', string='Works')
    assigned_to = fields.Many2one('res.users', string='Assign To')
    date = fields.Date(string='Date')
    status = fields.Boolean(string='Status')
    work_progress_id = fields.Many2one('logic.check.list', string='Work')

    @api.onchange('date', 'status')
    def _onchange_work_completed_date(self):
        if self.status == True:
            self.date = fields.Date.today()
