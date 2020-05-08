# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.tools import float_is_zero

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    margin_reco = fields.Float(string='Recommendation', 
                               default=lambda self: self.parent_id.margin_reco if self.parent_id else 0.0)
    
    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id.margin_reco:
            self.margin_reco = self.parent_id.margin_reco
            
    def action_popup(self):
        msg = 'test test test'
        return {
            'type': 'ir.actions.act_window',
            'name': 'title',
            'src_model': 'product.category',
            'res_model': 'wizard.popup',
            'view_mode': 'form',
            'views_id': {'ref': "stock_margin.wizard_popup"},
            'context': {'message': msg},
            'target': 'new',
        }
            