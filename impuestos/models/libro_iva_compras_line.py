# -*- coding: utf-8 -*-

from odoo import models, fields


class LibroIvaComprasLine(models.Model):
    _name = 'libro.iva.compras.line'
    _description = 'Línea de Libro de IVA Compras'

    libro_iva_compras_id = fields.Many2one('libro.iva.compras', string="Libro IVA Compras", ondelete='cascade')
    correlativo = fields.Char(string="Correlativo")
    nit = fields.Char(string="NIT")
    fecha = fields.Date(string="Fecha")
    tipo_comprobante = fields.Selection([
        ('FC', 'Factura de Consumidor Final'),
        ('CCF', 'Crédito Fiscal'),
    ], string="Tipo de Comprobante", default='FC')
    compras_exentas = fields.Float(string="Compras Exentas")
    compras_gravadas = fields.Float(string="Compras Gravadas")
    iva_credito_fiscal = fields.Float(string="IVA Crédito Fiscal")
    total = fields.Float(string="Total")
