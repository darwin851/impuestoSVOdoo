# -*- coding: utf-8 -*-

from odoo import models, fields


class F2RentaLine(models.Model):
    _name = 'f2.renta.line'
    _description = 'Línea de F2 Renta'

    f2_renta_id = fields.Many2one('f2.renta', string="F2 Renta", ondelete='cascade')
    nit = fields.Char(string="NIT")
    ventas_no_sujetas = fields.Float(string="Ventas No Sujetas")
    ventas_gravadas_renta = fields.Float(string="Ventas Gravadas Renta")
    renta_retenida = fields.Float(string="Renta Retenida")
    total = fields.Float(string="Total")
