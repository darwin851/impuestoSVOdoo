# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LibroIvaVentasWizard(models.TransientModel):
    _name = 'libro.iva.ventas.wizard'
    _description = 'Wizard para generar el Libro de IVA Ventas'

    fecha_inicio = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string="Fecha de fin", required=True, default=fields.Date.today)

    def generar_libro_iva_ventas(self):
        # Crear una nueva instancia del modelo libro.iva.ventas
        libro_iva_ventas = self.env['libro.iva.ventas'].create({
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
        })
        # Llamar al método generar_reporte del modelo libro.iva.ventas
        return libro_iva_ventas.generar_reporte()
