# =====================================================================
# ESTRUCTURAS DE DATOS INICIALES (Base de datos simulada)
# =====================================================================

configuracion_puntos = {
    "pesos_necesarios": 1000,
    "puntos_ganados": 10
}

cliente_inicial = {
    "nombre": "Lucia",
    "suscripcion": "Premium",
    "saldo_puntos": 0
}

compras_mensuales_inicial = [
    {"producto": "Cafe Colombia 500g", "monto": 18000},
    {"producto": "Cafe Brasil 1kg", "monto": 30000},
    {"producto": "Cafe Molido 250g", "monto": 12000}
]

recompensas_inicial = {
    "1": {"nombre": "Descuento 10%", "costo": 100, "solo_premium": False},
    "2": {"nombre": "Envio gratis", "costo": 150, "solo_premium": False},
    "3": {"nombre": "Taza exclusiva", "costo": 300, "solo_premium": True},
    "4": {"nombre": "Cafe premium gratis", "costo": 500, "solo_premium": True}
}

planes_iniciales = {
    "Basico": {"precio": 0, "beneficio": "Puntos normales", "multiplicador": 1},
    "Explorer": {"precio": 17999, "beneficio": "50% mas puntos", "multiplicador": 1.5},
    "Premium": {"precio": 29999, "beneficio": "Puntos dobles y beneficios VIP", "multiplicador": 2}
}

historial_compras_inicial = []

clientes_ranking_inicial = [
    {"nombre": "Sofia", "suscripcion": "Premium", "total_gastado": 85000},
    {"nombre": "Mateo", "suscripcion": "Premium", "total_gastado": 76000},
    {"nombre": "Valentina", "suscripcion": "Premium", "total_gastado": 63000},
    {"nombre": "Martin", "suscripcion": "Basico", "total_gastado": 90000}
]


# =====================================================================
# SECCION DE FUNCIONES DEL MODULO SMARTCLUB
# =====================================================================

#========== #consigna 1: Calcular puntos por una compra #========
def obtener_multiplicador(suscripcion, planes):
    suscripcion = suscripcion.strip().capitalize()

    if suscripcion in planes:
        return planes[suscripcion]["multiplicador"]

    return 1

#========== #consigna 2: Calcular puntos por una compra #========
def calcular_puntos(monto, suscripcion, configuracion, planes):
    try:
        monto_num = float(monto)
        if monto_num <= 0:
            return 0

        pesos_necesarios = configuracion["pesos_necesarios"]
        puntos_ganados = configuracion["puntos_ganados"]
        multiplicador = obtener_multiplicador(suscripcion, planes)

        puntos = int(monto_num // pesos_necesarios) * puntos_ganados
        puntos = int(puntos * multiplicador)

        return puntos
    except ValueError:
        return 0


#========== #consigna 3: Procesar lote de compras mensuales #========
def procesar_lote_compras(cliente, lista_compras, historial, configuracion, planes):
    puntos_totales = 0

    for compra in lista_compras:
        producto = compra["producto"]
        monto = compra["monto"]
        puntos = calcular_puntos(monto, cliente["suscripcion"], configuracion, planes)

        nueva_compra = {
            "producto": producto,
            "monto": monto,
            "puntos_obtenidos": puntos
        }

        historial.append(nueva_compra)
        cliente["saldo_puntos"] += puntos
        puntos_totales += puntos

    return puntos_totales
