# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import logging

_logger = logging.getLogger(__name__)

class Invoice(models.Model):
    _inherit = "account.invoice"
    
    json_erp = fields.Text("JSON ERP")

    @api.multi
    def enviar_venta_erp(self):
        for rec in self:
            data = {
                "idFactura" : rec.number,
                "numeroLineasDetalle" : len(rec.invoice_line_ids),
                "secuencial" : rec.invoice_seq_number,
                "establecimiento" : "",
                "puntoEmision" : "",
                "idCliente" : rec.partner_id.id_ws,
                "idSucursal" : "",
                "idBodega" : "",
                "observacion" : "",
                "usuarioFactura" : "",
                "fechaFactura" : rec.date_invoice.strftime("%Y-%m-%d"),
                "fechaVencimiento" : rec.date_invoice.strftime("%Y-%m-%d"),
                "autorizacionSRI" : "",
                "claveAccesoSRI" : "",
                "totalSinImpuesto" : rec.amount_untaxed,
                "valorConIVA" : rec.amount_total,
                "valorSinIVA" : rec.amount_untaxed,
                "porcentajeIVA" : "12", #account_invoice_tax.tax_id.amount
                "valorIVA" : rec.amount_tax, #account_invoice_tax.amount_total
                "totalDescuentos" : "0",
                "totalPagar" : rec.amount_total,
                "cliente": {
                    "idCliente": rec.partner_id.id_ws,
                    "idClase": "NA",
                    "nombreClase": "NO ASIGNADO",
                    "idTipo": "A2",
                    "tipoPersona": rec.partner_id.tipo_persona,
                    "tipoIdentificacion": rec.partner_id.tipo_identificacion,
                    "numeroIdentificacion": rec.partner_id.vat,
                    "razonSocial": rec.partner_id.name,
                    "telefono": rec.partner_id.phone,
                    "telefonoCelular": rec.partner_id.mobile,
                    "direccion": rec.partner_id.street2,
                    "correoElectronico": rec.partner_id.email,
                    "idPais": rec.partner_id.country_id and rec.partner_id.country_id.code,
                    "idProvincia": rec.partner_id.state_id and rec.partner_id.state_id.code,
                    "idCiudad": rec.partner_id.city,
                    "sexo": rec.partner_id.sexo,
                    "cargo": "Test",
                    "identificacionRepresentanteLegal": "1720485174",
                    "representanteLegal": "Mario Cadena",
                    "estado": rec.partner_id.estado
                },
                "sucursal": {
                    "idSucursal": "I001",
                    "idCliente": "I001",
                    "idClase": "NA",
                    "nombreClase": "NO ASIGNADO",
                    "idTipo": "A2",
                    "tipoIdentificacion": "C",
                    "numeroIdentificacion": "1720485174",
                    "personaContacto": "Mario Cadena",
                    "telefonoContacto": "0",
                    "celularContacto": "0",
                    "direccionesDeEntrega": "QUITO",
                    "idPais": "593",
                    "idProvincia": "17",
                    "idCiudad": "593171",
                    "estado": "A"
                },
                "detalle" : [],
                "pago" : [
                    {
                        "idLineaPago" : "",
                        "codigoFormaPago" : "",
                        "Valor" : "",
                        "numeroDocumento" : "",
                        "numeroCuenta" : "",
                        "codigoInstitucionFinanciera" : "",
                        "fechaTransaccion" : "",
                        "fechaVencimiento" : "",
                        "tipoEmision" : ""

                    }
                ]
            }

            items = []
            for line in rec.invoice_line_ids:
                new_item = {
                    "idLineaDetalle" : line.id,
                    "idBodega" : "",
                    "idProducto" : line.product_id.id_ws,
                    "cantidad" : line.quantity,
                    "precioUnitario" : line.price_unit,
                    "costoUnitario" : line.product_id.standard_price,
                    "porcentajeDescuento1" : "",
                    "valorDescuento1" : "",
                    "porcentajeDescuento2" : "",
                    "valorDescuento2" : "",
                    "porcentajeDescuento3" : "",
                    "valorDescuento3" : "",
                    "totalDescuentos" : line.discount,
                    "subTotal" : line.price_subtotal,
                    "porcentajeIVA" : line.tax_amount,
                    "valorIVA" : line.price_tax, #price_tax
                    "totalLinea" : line.price_total, #price_total
                    "productoPromocional" : line.product_id.tipo_producto == 1 and "S" or "N"
                }
                items.append(new_item)

            data.update({"detalle" : items})

            _logger.info(data)

            rec.json_erp = json.dumps(data)
        
        return True


# class asertia_ventas(models.Model):
#     _name = 'asertia_ventas.asertia_ventas'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100