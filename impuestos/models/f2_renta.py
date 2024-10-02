# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class F2Renta(models.Model):
    _name = 'f2.renta'
    _description = 'F2 Renta'

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_name(self):
        for rec in self:
            # Asegurarse de que fecha_inicio y fecha_fin sean fechas válidas
            if rec.fecha_inicio and rec.fecha_fin:
                rec.name = 'F2 Renta ' + rec.fecha_inicio.strftime('%Y-%m-%d') + ' - ' + rec.fecha_fin.strftime('%Y-%m-%d')
            else:
                rec.name = 'F2 Renta'  # Asignar un nombre por defecto si las fechas no están definidas

    name = fields.Char(compute='_compute_name', string="Nombre")
    company_id = fields.Many2one('res.company', string="Compañía", default=lambda self: self.env.company)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)
    f2_renta_line_ids = fields.One2many('f2.renta.line', 'f2_renta_id', string="Líneas de F2 Renta")

    def generar_reporte(self):
        self.ensure_one()
        self.f2_renta_line_ids.unlink()
        # Obtener todas las facturas de clientes en el rango de fechas especificado
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.fecha_inicio),
            ('invoice_date', '<=', self.fecha_fin),
            ('company_id', '=', self.company_id.id),
        ])

        # Agrupar las facturas por número de DUI/NIT
        grouped_invoices = {}
        for invoice in invoices:
            nit = invoice.partner_id.vat
            if not nit:
                continue
            if nit not in grouped_invoices:
                grouped_invoices[nit] = []
            grouped_invoices[nit].append(invoice)

        # Crear las líneas del F2 Renta
        for nit, invoices_group in grouped_invoices.items():
            total_amount = sum(inv.amount_total for inv in invoices_group)
            self.env['f2.renta.line'].create({  # <-- Llamar al modelo 'f2.renta.line'
                'f2_renta_id': self.id,
                'nit': nit,
                'ventas_no_sujetas': total_amount,  # Ajustar según la lógica de tu negocio
                'ventas_gravadas_renta': 0,  # Ajustar según la lógica de tu negocio
                'renta_retenida': 0,  # Ajustar según la lógica de tu negocio
                'total': total_amount,
            })

        # Abrir la vista de árbol del F2 Renta (usando action_view_form)
        return {
            'type': 'ir.actions.act_window',
            'name': _('F2 Renta'),
            'res_model': 'f2.renta.line',  # <--- Cambiado a 'f2.renta.line'
            'view_mode': 'tree',
            'domain': [('f2_renta_id', '=', self.id)],  # <--- Cambiado a 'f2_renta_id'
            'target': 'current',  # Abre la vista en la misma ventana
        }