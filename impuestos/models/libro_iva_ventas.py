# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LibroIvaVentas(models.Model):
    _name = 'libro.iva.ventas'
    _description = 'Libro de IVA Ventas'

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_name(self):
        for rec in self:
            # Asegurarse de que fecha_inicio y fecha_fin sean fechas válidas
            if rec.fecha_inicio and rec.fecha_fin:
                rec.name = 'Libro IVA Ventas ' + rec.fecha_inicio.strftime('%Y-%m-%d') + ' - ' + rec.fecha_fin.strftime(
                    '%Y-%m-%d')
            else:
                rec.name = 'Libro IVA Ventas'  # Asignar un nombre por defecto si las fechas no están definidas

    name = fields.Char(compute='_compute_name', string="Nombre")
    company_id = fields.Many2one('res.company', string="Compañía", default=lambda self: self.env.company)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)
    libro_iva_ventas_line_ids = fields.One2many('libro.iva.ventas.line', 'libro_iva_ventas_id',
                                                string="Líneas de Libro IVA Ventas")

    def generar_reporte(self):
        self.ensure_one()
        self.libro_iva_ventas_line_ids.unlink()
        # Obtener todas las facturas de clientes en el rango de fechas especificado
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.fecha_inicio),
            ('invoice_date', '<=', self.fecha_fin),
            ('company_id', '=', self.company_id.id),
        ])

        # Crear las líneas del Libro de IVA Ventas
        for invoice in invoices:
            tipo_comprobante = invoice.tipo_comprobante  # Obtener el tipo de comprobante de la factura
            self.env['libro.iva.ventas.line'].create({
                'libro_iva_ventas_id': self.id,
                'correlativo': invoice.correlativo_fiscal,
                'nit': invoice.partner_id.vat,
                'fecha': invoice.invoice_date,
                'tipo_comprobante': tipo_comprobante,  # Ajustar según el tipo de comprobante
                'ventas_exentas': 0,  # Ajustar según la lógica de tu negocio
                'ventas_gravadas': invoice.amount_untaxed,  # Ajustar según la lógica de tu negocio
                'iva_debito_fiscal': invoice.amount_tax,  # Ajustar según la lógica de tu negocio
                'total': invoice.amount_total,
            })

        # Abrir la vista de árbol del Libro de IVA Ventas (usando action_view_form)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Libro de IVA Ventas'),
            'res_model': 'libro.iva.ventas.line',  # <--- Cambiado a 'libro.iva.ventas.line'
            'view_mode': 'tree',
            'domain': [('libro_iva_ventas_id', '=', self.id)],  # <--- Cambiado a 'libro_iva_ventas_id'
            'target': 'current',  # Abre la vista en la misma ventana
        }
