PAYMENT_METHOD = (
    ('efectivo', 'Efectivo'),
    ('credito', 'Credito'),
)

ENVIRONMENT_TYPE = (
    (1, 'PRUEBAS'),
    (2, 'PRODUCCIÓN'),
)

VOUCHER_TYPE = (
    ('01', 'FACTURA'),
    ('03', 'LIQUIDACIÓN DE COMPRA DE BIENES Y PRESTACIÓN DE SERVICIOS'),
    ('04', 'NOTA DE CRÉDITO'),
    ('05', 'NOTA DE DÉBITO'),
    ('06', 'GUÍA DE REMISIÓN'),
    ('07', 'COMPROBANTE DE RETENCIÓN'),
)

EMISSION_TYPE = (
    (1, 'Emisión Normal'),
)

RETENTION_AGENT = (
    ('SI', 'Si'),
    ('NO', 'No'),
)

OBLIGATED_ACCOUNTING = (
    ('SI', 'Si'),
    ('NO', 'No'),
)

IDENTIFICATION_TYPE = (
    ('05', 'CEDULA'),
    ('04', 'RUC'),
    ('06', 'PASAPORTE'),
    ('07', 'VENTA A CONSUMIDOR FINAL*'),
    ('08', 'IDENTIFICACION DELEXTERIOR*'),
)

TAX_CODES = (
    (2, 'IVA'),
    (3, 'ICE'),
    (5, 'IRBPNR'),
)

PAYMENT_METHODS = (
    ('01', 'SIN UTILIZACION DEL SISTEMA FINANCIERO'),
    ('15', 'COMPENSACIÓN DE DEUDAS'),
    ('16', 'TARJETA DE DÉBITO'),
    ('17', 'DINERO ELECTRÓNICO'),
    ('18', 'TARJETA PREPAGO'),
    ('20', 'OTROS CON UTILIZACION DEL SISTEMA FINANCIERO'),
    ('21', 'ENDOSO DE TÍTULOS'),
)

VOUCHER_STATUS = (
    ('stateless', 'Sin estado'),
    ('generated', 'Generados'),
    ('signed', 'Firmados'),
    ('valid', 'Válidos'),
    ('authorized', 'Autorizados'),
    ('mailed', 'Autorizado y enviado por email'),
)

RECEIPT_SUPPORT = (
    ('01', 'Crédito Tributario para declaración de IVA (servicios y bienes distintos de inventarios y activos fijos)'),
    ('02', 'Costo o Gasto para declaración de IR (servicios y bienes distintos de inventarios y activos fijos)'),
    ('03', 'Activo Fijo - Crédito Tributario para declaración de IVA'),
    ('04', 'Activo Fijo - Costo o Gasto para declaración de IR'),
    ('05', 'Liquidación Gastos de Viaje, hospedaje y alimentación Gastos IR (a nombre de empleados y no de la empresa)'),
    ('06', 'Inventario - Crédito Tributario para declaración de IVA'),
    ('07', 'Inventario - Costo o Gasto para declaración de IR'),
    ('08', 'Valor pagado para solicitar Reembolso de Gasto (intermediario)'),
    ('09', 'Reembolso por Siniestros'),
    ('10', 'Distribución de Dividendos, Beneficios o Utilidades'),
    ('11', 'Convenios de débito o recaudación para IFI´s'),
    ('12', 'Impuestos y retenciones presuntivos'),
    ('13', 'Valores reconocidos por entidades del sector público a favor de sujetos pasivos'),
    ('14', 'Valores facturados por socios a operadoras de transporte (que no constituyen gasto de dicha operadora)'),
    ('15', 'Pagos efectuados por consumos propios y de terceros de servicios digitales'),
    ('00', 'Casos especiales cuyo sustento no aplica en las opciones anteriores'),
)