# -*- coding: utf-8 -*-

from odoo import models, fields, api


class F1IvaWizard(models.TransientModel):
    _name = 'f1.iva.wizard'
    _description = 'Wizard para generar F1 IVA'

    fecha_inicio = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.today)
    fecha_fin = fields.Date(string="Fecha de fin", required=True, default=fields.Date.today)

    def generar_f1_iva(self):
        # Crear una nueva instancia del modelo f1.iva
        f1_iva = self.env['f1.iva'].create({
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
        })
        # Llamar al método generar_reporte del modelo f1.iva
        return f1_iva.generar_reporte()