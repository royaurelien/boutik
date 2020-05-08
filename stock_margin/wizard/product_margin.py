# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context

_logger = logging.getLogger(__name__)

class ProductMargin(models.TransientModel):
    _name = 'product.margin'
    _description = 'Product Margin Calc'

    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, readonly=True)
    product_has_variants = fields.Boolean('Has variants', default=False, required=True, readonly=True)
    margin_reco = fields.Float(related='product_tmpl_id.categ_id.margin_reco', readonly=True, required=True)
    standard_price = fields.Float(related='product_id.standard_price', readonly=True, required=True)
    list_price = fields.Float(related='product_tmpl_id.list_price', readonly=True, required=True)
    lst_price = fields.Float(related='product_id.lst_price', readonly=True, required=True)
    price = fields.Float(required=True)
    margin = fields.Float(compute='_compute_margin', required=True)
    margin_rate = fields.Float(compute='_compute_margin', required=True)
    formula = fields.Selection("_get_formula", required=True)
    round_method = fields.Selection([('up', 'up')])

    @api.model
    def _get_formula(self):
        return [('percent', 'percent'), 
               ('recommendation', 'reco')]
    
    @api.model
    def default_get(self, fields):
        _logger.warning("XXX")
        res = super(ProductMargin, self).default_get(fields)
        
        if self.env.context.get('default_product_id'):
            product_id = self.env['product.product'].browse(self.env.context['default_product_id'])
            product_tmpl_id = product_id.product_tmpl_id
            res['product_tmpl_id'] = product_id.product_tmpl_id.id
            res['product_id'] = product_id.id
        elif self.env.context.get('default_product_tmpl_id'):
            product_tmpl_id = self.env['product.template'].browse(self.env.context['default_product_tmpl_id'])
            res['product_tmpl_id'] = product_tmpl_id.id
            res['product_id'] = product_tmpl_id.product_variant_id.id
            if len(product_tmpl_id.product_variant_ids) > 1:
                res['product_has_variants'] = True

        _logger.warning(repr(res))
        return res

    @api.onchange('formula', 'round_method')
    def _onchange_calc(self):
        price = 0.0
        if self.formula == 'reco':
            self.margin = self.margin_reco
            price = self.list_price + self.list_price * self.margin_reco  
        
        price = round(price) if self.round_method == 'up' else price
    
        self.price = price

    @api.depends('standard_price')
    def _compute_margin(self):
        for record in self:
            values = record.product_tmpl_id._prepare_margin()
            record.margin = values.get('margin', 0.0)
            record.margin_rate = values.get('margin_rate', 0.0)        
        
    def update_price(self):
        try:
            product = 'product.product' if self.product_has_variants else 'product.template'
            values = self._prepare_values()
            self.env[model].update(values)
            
        except UserError as error:
            raise UserError(error)

    def _prepare_values(self):

        values = {
            'standard_price': self.standard_price,
        }
        return values
