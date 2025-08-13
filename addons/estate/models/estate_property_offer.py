from odoo import fields, models

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

