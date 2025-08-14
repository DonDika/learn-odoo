from odoo import api, fields, models
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('acccepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    
    # relasi Many2One mengambil data ke table res_partner
    partner_id = fields.Many2one("res.partner", required=True)
    
    # relasi Many2One, property_id adalah link balik ke model estate.property.
    property_id = fields.Many2one("estate.property", required=True)



    validity = fields.Integer(string="Validity (days)", default=7)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    # ambil data
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

     

