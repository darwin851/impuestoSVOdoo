# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LibroIvaCompras(models.Model):
    _name = 'libro.iva.compras'
    _description = 'Libro de IVA Compras'

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_name(self):
        for rec in self:
            # Asegurarse de que fecha_inicio y fecha_fin sean fechas válidas
            if rec.fecha_inicio and rec.fecha_fin:
                rec.name = 'Libro IVA Compras ' + rec.fecha_inicio.strftime(
                    '%Y-%m-%d') + ' - ' + rec.fecha_fin.strftime('%Y-%m-%d')
            else:
                rec.name = 'Libro IVA Compras'  # Asignar un nombre por defecto si las fechas no están definidas

    name = fields.Char(compute='_compute_name', string="Nombre")
    company_id = fields.Many2one('res.company', string="Compañía", default=lambda self: self.env.company)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)
    libro_iva_compras_line_ids = fields.One2many('libro.iva.compras.line', 'libro_iva_compras_id',
                                                 string="Líneas de Libro IVA Compras")

    def generar_reporte(self):
        self.ensure_one()
        self.libro_iva_compras_line_ids.unlink()

        # Obtener las facturas de compra pagadas en el rango de fechas
        facturas_compra = self.env['purchase.order'].search([
            ('state', '=', 'purchase'),  # Estado "Pagado" en el módulo de compras
            ('date_order', '>=', self.fecha_inicio),
            ('date_order', '<=', self.fecha_fin),
            ('company_id', '=', self.company_id.id),
        ])

        # Crear las líneas del Libro de IVA Compras
        for factura in facturas_compra:
            # Obtener el tipo de comprobante (FC o CCF) - Ajustar si es necesario
            tipo_comprobante = factura.tipo_comprobante

            # Obtener la información de la factura
            correlativo = factura.name  # Número de documento de la factura de compra
            nit = factura.partner_id.vat
            fecha = factura.date_order
            compras_exentas = 0  # Ajustar según la lógica de tu negocio
            compras_gravadas = factura.amount_untaxed
            iva_credito_fiscal = factura.amount_tax
            total = factura.amount_total

            self.env['libro.iva.compras.line'].create({
                'libro_iva_compras_id': self.id,
                'correlativo': correlativo,
                'nit': nit,
                'fecha': fecha,
                'tipo_comprobante': tipo_comprobante,
                'compras_exentas': compras_exentas,
                'compras_gravadas': compras_gravadas,
                'iva_credito_fiscal': iva_credito_fiscal,
                'total': total,
            })

        # Abrir la vista de árbol del Libro de IVA Compras
        return {
            'type': 'ir.actions.act_window',
            'name': _('Libro de IVA Compras'),
            'res_model': 'libro.iva.compras.line',
            'view_mode': 'tree',
            'domain': [('libro_iva_compras_id', '=', self.id)],
            'target': 'current',
        }