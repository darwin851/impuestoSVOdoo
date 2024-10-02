# -*- coding: utf-8 -*-

from odoo import models, fields


class LibroIvaVentasLine(models.Model):
    _name = 'libro.iva.ventas.line'
    _description = 'Línea de Libro de IVA Ventas'

    libro_iva_ventas_id = fields.Many2one('libro.iva.ventas', string="Libro IVA Ventas", ondelete='cascade')
    correlativo = fields.Char(string="Correlativo")
    nit = fields.Char(string="NIT")
    fecha = fields.Date(string="Fecha")
    tipo_comprobante = fields.Selection([
        ('FC', 'Factura de Consumidor Final'),
        ('CCF', 'Crédito Fiscal'),
    ], string="Tipo de Comprobante", default='FC')
    ventas_exentas = fields.Float(string="Ventas Exentas")
    ventas_gravadas = fields.Float(string="Ventas Gravadas")
    iva_debito_fiscal = fields.Float(string="IVA Débito Fiscal")
    total = fields.Float(string="Total")
