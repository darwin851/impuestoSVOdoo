# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LibroIvaComprasWizard(models.TransientModel):
    _name = 'libro.iva.compras.wizard'
    _description = 'Wizard para generar el Libro de IVA Compras'

    fecha_inicio = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string="Fecha de fin", required=True, default=fields.Date.today)

    def generar_libro_iva_compras(self):
        # Crear una nueva instancia del modelo libro.iva.compras
        libro_iva_compras = self.env['libro.iva.compras'].create({
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
        })
        # Llamar al método generar_reporte del modelo libro.iva.compras
        return libro_iva_compras.generar_reporte()
