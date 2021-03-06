# -*- coding: utf-8 -*-
""" init object """
from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    total_discount = fields.Float(compute='compute_total_qty_discount',store=True )
    total_quantity = fields.Float(compute='compute_total_qty_discount',store=True )
    receipt_note = fields.Text( compute='compute_reciept_not')

    @api.multi
    @api.depends('order_line','order_line.discount','order_line.price_subtotal','order_line.product_qty')
    # @api.depends('order_line','order_line.price_subtotal','order_line.product_qty')
    def compute_total_qty_discount(self):
        for rec in self:
            qty = 0.0
            discount = 0.0
            for line in rec.order_line:
                qty += line.product_qty
                total_without_discount = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id,
                                                  line.product_qty, product=line.product_id,
                                                  partner=line.order_id.partner_id)['total_included']
                discount += total_without_discount - line.price_total

            rec.total_discount = discount
            rec.total_quantity = qty

    def compute_reciept_not(self):
        for rec in self:
            receipt_note = ''
            for s in rec.picking_ids:
                receipt_note += s.note or '\n'

            rec.receipt_note = receipt_note





