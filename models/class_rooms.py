from odoo import models, fields, api, _


class CheckListClassRoom(models.Model):
    _name = 'check.list.class.room'
    _description = 'Class Room'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    branch = fields.Selection([('corporate_office', 'Corporate Office'), ('cochin_campus', 'Cochin Campus'),
                               ('kottayam_campus', 'Kottayam Campus'), ('calicut_campus', 'Calicut Campus'),
                               ('malappuram_campus', 'Malappuram Campus'), ('trivandrum_campus', 'Trivandrum Campus'),
                               ('palakkad_campus', 'Palakkad Campus'), ('dubai_campus', 'Dubai Campus')],
                              string='Branch')
    assets = fields.Many2many('class.room.assets', string='Assets')
    capacity = fields.Integer(string='Capacity')

