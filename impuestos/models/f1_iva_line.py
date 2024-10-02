# -*- coding: utf-8 -*-

from odoo import models, fields

class F1IvaLine(models.Model):
    _name = 'f1.iva.line'
    _description = 'Línea de F1 IVA'

    f1_iva_id = fields.Many2one('f1.iva', string="F1 IVA", ondelete='cascade')
    correlativo = fields.Char(string="Correlativo")
    nit = fields.Char(string="NIT")
    ventas_exentas = fields.Float(string="Ventas Exentas")
    ventas_gravadas = fields.Float(string="Ventas Gravadas")
    iva_retenido = fields.Float(string="IVA Retenido")
    total = fields.Float(string="Total")