from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    # private attribute, sebagai identitas dari class
    _name = "estate.property"
    _description = "Estate Property"
    
    # untuk mendefinisikan field, digunakan untuk membuat fields di db atau tabel, di dalam tabel estate property ada field yang bernama name
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3)) # mencegah copy value saat di-duplicate & default availability date is in 3 months  
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False) # tidak bisa input di view
    bedrooms = fields.Integer(default=2) # default value 
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    active = fields.Boolean(default=False) # jika active = false, maka tidak akan bisa dicari

    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )


