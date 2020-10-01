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
            fac_numbers = rec.number.split("-")
            data = {
                "idFactura" : "O" + rec.number.replace("-", ""),
                "numeroLineasDetalle" : str(len(rec.invoice_line_ids)),
                "secuencial" : fac_numbers[2],
                "establecimiento" : fac_numbers[0],
                "puntoEmision" : fac_numbers[1],
                "idCliente" : "O" + rec.partner_id.id_ws,
                "idSucursal" : "O" + rec.partner_id.id_ws,
                "idBodega" : "O400",
                "observacion" : "",
                "usuarioFactura" : rec.user_id.name,
                "fechaFactura" : rec.date_invoice.strftime("%Y-%m-%d 00:00:00"),
                "fechaVencimiento" : rec.date_invoice.strftime("%Y-%m-%d 00:00:00"),
                "autorizacionSRI" : rec.access_code,
                "claveAccesoSRI" : rec.access_code,
                "totalSinImpuesto" : "%.2f" % rec.amount_untaxed,
                "valorConIVA" : "%.2f" % rec.amount_total,
                "valorSinIVA" : "%.2f" % rec.amount_untaxed,
                "porcentajeIVA" : "12", #account_invoice_tax.tax_id.amount
                "valorIVA" : "%.2f" % rec.amount_tax, #account_invoice_tax.amount_total
                "totalDescuentos" : "0.00",
                "totalPagar" : "%.2f" % rec.amount_total,
                "cliente": {
                    "idCliente": "O" + rec.partner_id.id_ws,
                    "idClase": "61",
                    "nombreClase": "CONSUMIDOR FINAL",
                    "idTipo": "NM",
                    "tipoPersona": rec.partner_id.tipo_persona,
                    "tipoIdentificacion": rec.partner_id.tipo_identificacion,
                    "numeroIdentificacion": rec.partner_id.vat,
                    "razonSocial": rec.partner_id.name,
                    "telefono": rec.partner_id.phone or ".",
                    "telefonoCelular": rec.partner_id.mobile or ".",
                    "direccion": rec.partner_id.street2 or ".",
                    "correoElectronico": rec.partner_id.email or ".",
                    "idPais": "593",
                    "idProvincia": "17",
                    "idCiudad": "593178",
                    "sexo": rec.partner_id.sexo,
                    "cargo": "",
                    "identificacionRepresentanteLegal": "",
                    "representanteLegal": "",
                    "estado": rec.partner_id.estado
                },
                "sucursal": {
                    "idSucursal": "O" + rec.partner_id.id_ws,
                    "idCliente": "O" + rec.partner_id.id_ws,
                    "idClase": "61",
                    "nombreClase": "CONSUMIDOR FINAL",
                    "idTipo": "NM",
                    "tipoIdentificacion": "C",
                    "numeroIdentificacion": "1720485174",
                    "personaContacto": ".",
                    "telefonoContacto": ".",
                    "celularContacto": ".",
                    "direccionesDeEntrega": ".",
                    "idPais": "593",
                    "idProvincia": "17",
                    "idCiudad": "593178",
                    "estado": "A"
                },
                "detalle" : [],
                "pago" : []
            }

            pagos = []
            if rec.pos_id:
                for pago in rec.pos_id.statement_ids:
                    new_pago = {
                        "idLineaPago" : pago.id,
                        "codigoFormaPago" : "0",
                        "Valor" : "%.2f" % pago.amount,
                        "numeroDocumento" : "",
                        "numeroCuenta" : "",
                        "codigoInstitucionFinanciera" : "",
                        "fechaTransaccion" : data["fecha_factura"],
                        "fechaVencimiento" : data["fecha_factura"],,
                        "tipoEmision" : "E"
                    }
                    pagos.append(new_pago)
            

            items = []
            for line in rec.invoice_line_ids:
                new_item = {
                    "idLineaDetalle" : str(line.id),
                    "idBodega" : "O400",
                    "idProducto" : line.product_id.id_ws,
                    "cantidad" : str(line.quantity),
                    "precioUnitario" : str(line.price_unit),
                    "costoUnitario" : str(line.product_id.standard_price),
                    "porcentajeDescuento1" : "0.00",
                    "valorDescuento1" : "0.00",
                    "porcentajeDescuento2" : "0.00",
                    "valorDescuento2" : "0.00",
                    "porcentajeDescuento3" : "0.00",
                    "valorDescuento3" : "0.00",
                    "totalDescuentos" : "%.2f" % line.discount,
                    "subTotal" : "%.2f" % line.price_subtotal,
                    "porcentajeIVA" : "%.2f" % line.tax_amount,
                    "valorIVA" : "%.2f" % line.price_tax, #price_tax
                    "totalLinea" : "%.2f" % line.price_total, #price_total
                    "productoPromocional" : line.product_id.tipo_producto == 1 and "S" or "N"
                }
                items.append(new_item)

            data.update({"detalle" : items, "pago" : pagos})

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