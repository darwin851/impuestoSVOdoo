# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class F1Iva(models.Model):
    _name = 'f1.iva'
    _description = 'F1 IVA'

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_name(self):
        for rec in self:
            # Asegurarse de que fecha_inicio y fecha_fin sean fechas válidas
            if rec.fecha_inicio and rec.fecha_fin:
                rec.name = 'F1 IVA ' + rec.fecha_inicio.strftime('%Y-%m-%d') + ' - ' + rec.fecha_fin.strftime(
                    '%Y-%m-%d')
            else:
                rec.name = 'F1 IVA'  # Asignar un nombre por defecto si las fechas no están definidas

    name = fields.Char(compute='_compute_name', string="Nombre")
    company_id = fields.Many2one('res.company', string="Compañía", default=lambda self: self.env.company)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de fin", required=True)
    f1_iva_line_ids = fields.One2many('f1.iva.line', 'f1_iva_id', string="Líneas de F1 IVA")

    def generar_reporte(self):
        self.ensure_one()
        self.f1_iva_line_ids.unlink()
        # Obtener todas las facturas de clientes en el rango de fechas especificado
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.fecha_inicio),
            ('invoice_date', '<=', self.fecha_fin),
            ('company_id', '=', self.company_id.id),
        ])

        # Agrupar las facturas por número de correlativo y número de DUI/NIT
        grouped_invoices = {}
        for invoice in invoices:
            correlativo = invoice.correlativo_fiscal
            nit = invoice.partner_id.vat
            if not nit:
                continue
            key = (correlativo, nit)
            if key not in grouped_invoices:
                grouped_invoices[key] = []
            grouped_invoices[key].append(invoice)

        # Crear las líneas del F1 IVA
        for key, invoices_group in grouped_invoices.items():
            correlativo, nit = key
            total_amount = sum(inv.amount_total for inv in invoices_group)
            self.env['f1.iva.line'].create({
                'f1_iva_id': self.id,
                'correlativo': correlativo,
                'nit': nit,
                'ventas_exentas': total_amount,  # Ajustar según la lógica de tu negocio
                'ventas_gravadas': 0,  # Ajustar según la lógica de tu negocio
                'iva_retenido': 0,  # Ajustar según la lógica de tu negocio
                'total': total_amount,
            })

        # Abrir la vista de árbol del F1 IVA (usando action_view_form)
        return {
            'type': 'ir.actions.act_window',
            'name': _('F1 IVA'),
            'res_model': 'f1.iva.line',  # <---  Cambiado a 'f1.iva.line'
            'view_mode': 'tree',
            'domain': [('f1_iva_id', '=', self.id)],  # <---  Cambiado a 'f1_iva_id'
            'target': 'current',  # Abre la vista en la misma ventana
        }