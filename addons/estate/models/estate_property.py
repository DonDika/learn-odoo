from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    # private attribute, sebagai identitas dari class
    _name = "estate.property"
    _description = "Estate Property"
    
    # untuk mendefinisikan field, digunakan untuk membuat fields di db atau table, di dalam table estate_property ada field di bawah ini
    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3)) # mencegah copy value saat di-duplicate & default availability date is in 3 months  
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False) # tidak bisa input di view
    bedrooms = fields.Integer(default=2) # default value 
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
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

    # relasi Many2One ke table estate_property_type
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # mengambil data karywan/salesperson dari table res_users. Mendapatkan data current user=self.env.user
    salesperson_id = fields.Many2one("res.users", string="Salesman", index=True, default=lambda self: self.env.user) 

    # mengambil data buyer dari table res_partner
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)

    # relasi Many2Many ke table estate_property_tag
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")

    # relasi One2Many | reference second parameter, relasinya nyambung lewat field property_id yang ada di model estate.property.offer
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    

    # computed field
    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)")

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
         'The selling price must be positive')
    ]


    # api decorator
    @api.depends("living_area", "garden_area") # parameter apa yg dibutuhkan
    def _compute_total_area(self):
        # ambil data self
        for record in self:
            # masukkan data ke total_area
            record.total_area = sum([record.living_area, record.garden_area])

    
    @api.depends("offer_ids.price") # parameter apa yg dibutuhkan
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0
        

    @api.onchange("garden") # parameter apa yg mau diubah
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return {'warning': {
                'title': _("Warning"),
                'message': ("This option will enable Garden Area (default: 10) & orientation (default: North)")
            }} 
        else:
            self.garden_area = None
            self.garden_orientation = None
    

    # a public method should always return something so that it can be called through XML-RPC. 
    # When in doubt, just return True.
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled property cannot be sold")
            record.state = "sold"
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be canceled")
            record.state = "canceled"
        return True


    @api.constrains("expected_price","selling_price")
    def _check_selling_price(self):
        precision = 2
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=precision):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=precision) < 0:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price")
                


    