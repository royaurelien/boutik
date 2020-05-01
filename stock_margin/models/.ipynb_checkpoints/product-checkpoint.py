# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.tools import float_is_zero

class ProductTemplate(models.Model):
    _inherit = 'product.template'
     
    margin = fields.Float(string="Margin", compute="_compute_margin", store=True)
    margin_rate = fields.Float(string="Margin rate (%)", compute="_compute_margin", store=True)

    @api.depends('list_price', 'lst_price', 'standard_price')
    def _compute_margin(self):
        for record in self:
            if record.product_variant_count == 1 and not record.is_product_variant:
                record.margin = record.list_price - record.standard_price
                record.margin_rate = (record.margin / record.standard_price)
            else:
                record.margin = record.margin_rate = 0.0

    def action_recalc_margin(self):
        for record in self:
            record._compute_margin()
            
    def action_check_margin(self):
        for record in self:
            msg = False
            if float_is_zero(record.margin, precision_rounding=0.001):
                msg = 'Margin is equal to zero.'
            elif record.margin < 0.0:
                msg = 'Margin is negative.'
            if msg: 
                self._log_exception_activity(record, msg)
            
    def _log_exception_activity(self, product_id, note):
        existing_activity = self.env['mail.activity'].search([
            ('res_id', '=',  product_id.id), 
            ('res_model_id', '=', self.env.ref('product.model_product_template').id), 
            ('note', '=', note)])
        
        if not existing_activity:
            # If the user deleted warning activity type.
            try:
                activity_type_id = self.env.ref('mail.mail_activity_data_warning').id
            except:
                activity_type_id = False
                
            self.env['mail.activity'].create({
                'activity_type_id': activity_type_id,
                'note': note,
                'user_id': product_id.responsible_id.id or SUPERUSER_ID,
                'res_id': product_id.id,
                'res_model_id': self.env.ref('product.model_product_template').id,
            })        
        
class ProductProduct(models.Model):
    _inherit = 'product.product'
     
    margin = fields.Float(string="Margin", compute="_compute_margin", store=True)
    margin_rate = fields.Float(string="Margin rate (%)", compute="_compute_margin", store=True)

    @api.depends('list_price', 'lst_price', 'standard_price')
    def _compute_margin(self):
        for record in self:
            if record.is_product_variant:
                record.margin = record.lst_price - record.standard_price
                record.margin_rate = (record.margin / record.lst_price)            

