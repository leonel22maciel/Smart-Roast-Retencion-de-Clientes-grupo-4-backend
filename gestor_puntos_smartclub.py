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
    "saldo_puntos": 0,
    "activo": True,
    "descuento_pendiente": 0.0
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


#========== #consigna 4: Registrar una compra individual #========
def calcular_monto_con_descuento(cliente, monto):
    descuento = cliente.get("descuento_pendiente", 0.0)
    if descuento <= 0:
        return monto

    monto_descuento = monto * (1 - descuento)
    cliente["descuento_pendiente"] = 0.0
    return round(monto_descuento, 2)


def registrar_compra(cliente, historial, producto, monto, configuracion, planes):
    try:
        monto_num = float(monto)
        if monto_num <= 0:
            return False, 0

        monto_final = calcular_monto_con_descuento(cliente, monto_num)
        puntos = calcular_puntos(monto_final, cliente["suscripcion"], configuracion, planes)

        compra = {
            "producto": producto,
            "monto": monto_num,
            "monto_final": monto_final,
            "puntos_obtenidos": puntos
        }

        historial.append(compra)
        cliente["saldo_puntos"] += puntos

        return True, puntos
    except ValueError:
        return False, 0


#========== #consigna 5: Consultar saldo de puntos #========
def consultar_saldo(cliente):
    return cliente["saldo_puntos"]


#========== #consigna 6: Buscar recompensa por ID #========
def buscar_recompensa(recompensas, id_recompensa):
    if id_recompensa in recompensas:
        return recompensas[id_recompensa]
    else:
        return None


#========== #consigna 7: Canjear recompensa validando saldo #========
def canjear_recompensa(cliente, recompensas, id_recompensa):
    recompensa = buscar_recompensa(recompensas, id_recompensa)

    if recompensa is None:
        return False, "La recompensa no existe."

    if recompensa["solo_premium"] and cliente["suscripcion"].lower().strip() != "premium":
        return False, "Esta recompensa es solo para clientes Premium."

    costo = recompensa["costo"]

    if cliente["saldo_puntos"] < costo:
        return False, "Saldo insuficiente. No se puede dejar saldo negativo."

    cliente["saldo_puntos"] -= costo

    if recompensa["nombre"].lower().startswith("descuento 10"):
        cliente["descuento_pendiente"] = 0.10
        return True, "Canje realizado correctamente. Se aplicara un 10% de descuento en la siguiente compra."

    return True, "Canje realizado correctamente."


def actualizar_estado_cliente(cliente, activo):
    cliente["activo"] = bool(activo)
    return cliente["activo"]


def buscar_cliente(clientes, nombre):
    nombre = nombre.strip().lower()
    for cliente in clientes:
        if cliente["nombre"].strip().lower() == nombre:
            return cliente
    return None


def dar_alta_cliente(clientes, nombre, suscripcion, saldo_puntos=0, descuento_pendiente=0.0):
    if buscar_cliente(clientes, nombre) is not None:
        return False, "Ya existe un cliente con ese nombre."

    cliente_nuevo = {
        "nombre": nombre.strip().title(),
        "suscripcion": suscripcion.strip().capitalize(),
        "saldo_puntos": saldo_puntos,
        "activo": True,
        "descuento_pendiente": descuento_pendiente
    }
    clientes.append(cliente_nuevo)
    return True, f"Cliente {cliente_nuevo['nombre']} dado de alta correctamente."


def dar_baja_cliente(clientes, nombre):
    cliente = buscar_cliente(clientes, nombre)
    if cliente is None:
        return False, "No se encontro el cliente."

    clientes.remove(cliente)
    return True, f"Cliente {cliente['nombre']} eliminado del registro."


def seleccionar_cliente(clientes):
    if len(clientes) == 0:
        return None
    if len(clientes) == 1:
        return clientes[0]

    print("\nClientes registrados:")
    for cliente in clientes:
        estado = "Activo" if cliente.get("activo", False) else "Inactivo"
        print(f"- {cliente['nombre']} | {cliente['suscripcion']} | {estado}")

    nombre = input("Ingrese el nombre del cliente: ").strip()
    cliente = buscar_cliente(clientes, nombre)
    if cliente is None:
        print("Cliente no encontrado. Seleccione una opcion valida.")
    return cliente


def recategorizar_suscripcion(cliente, nueva_suscripcion, planes):
    if nueva_suscripcion.strip().capitalize() not in planes:
        return False, "El plan de suscripcion no existe."

    cliente["suscripcion"] = nueva_suscripcion.strip().capitalize()
    return True, f"Suscripcion actualizada a {cliente['suscripcion']}."


#========== #consigna 8: Listar recompensas disponibles #========
def listar_recompensas_disponibles(cliente, recompensas):
    disponibles = []

    for id_recompensa, datos in recompensas.items():
        if datos["solo_premium"] and cliente["suscripcion"].lower().strip() != "premium":
            continue

        disponibles.append({
            "id": id_recompensa,
            "nombre": datos["nombre"],
            "costo": datos["costo"]
        })

    return disponibles


#========== #consigna 9: Mostrar planes de suscripcion #========
def listar_planes(planes):
    lista_planes = []

    for nombre_plan, datos in planes.items():
        lista_planes.append({
            "plan": nombre_plan,
            "precio": datos["precio"],
            "beneficio": datos["beneficio"],
            "multiplicador": datos["multiplicador"]
        })

    return lista_planes


#========== #consigna 10: Obtener Top Premium #========
def obtener_top_premium(clientes):
    premium = []

    for cliente in clientes:
        if cliente["suscripcion"].lower().strip() == "premium":
            premium.append(cliente)

    premium.sort(key=lambda dato: dato["total_gastado"], reverse=True)
    return premium[:10]


#========== #consigna 11: Mostrar historial de compras #========
def mostrar_historial_compras(historial):
    return historial


# =====================================================================
# MENU DEL SISTEMA (Para probar el modulo en consola)
# =====================================================================

def mostrar_menu():
    print("\n" + "=" * 55)
    print("        SISTEMA SMARTCLUB - COFFEE CLUB")
    print("=" * 55)
    print("1. Procesar lote mensual de compras")
    print("2. Registrar una compra individual")
    print("3. Consultar saldo de puntos")
    print("4. Ver historial de compras")
    print("5. Ver recompensas disponibles")
    print("6. Canjear recompensa")
    print("7. Ver planes de suscripcion")
    print("8. Ver Top Premium")
    print("9. Dar de alta un nuevo cliente")
    print("10. Dar de baja un cliente")
    print("11. Recategorizar un cliente")
    print("0. Salir")
    print("=" * 55)


def main():
    clientes = [cliente_inicial.copy()]
    compras_mensuales = compras_mensuales_inicial.copy()
    recompensas = recompensas_inicial.copy()
    planes = planes_iniciales.copy()
    historial = historial_compras_inicial.copy()
    ranking = clientes_ranking_inicial.copy()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            print("Gracias por usar SmartClub.")
            break

        elif opcion == "1":
            print("\n--- PROCESAR LOTE MENSUAL ---")
            cliente = seleccionar_cliente(clientes)
            if cliente is None:
                print("No hay clientes registrados.")
            else:
                puntos = procesar_lote_compras(cliente, compras_mensuales, historial, configuracion_puntos, planes)
                print(f"Se procesaron las compras del mes para {cliente['nombre']}. Puntos generados: {puntos}")
                print(f"Saldo actual: {cliente['saldo_puntos']} puntos")

        elif opcion == "2":
            print("\n--- REGISTRAR COMPRA ---")
            cliente = seleccionar_cliente(clientes)
            if cliente is None:
                print("No hay clientes registrados.")
            else:
                producto = input("Ingrese el producto comprado: ").strip()
                monto = input("Ingrese el monto gastado: ").strip()
                exito, puntos = registrar_compra(cliente, historial, producto, monto, configuracion_puntos, planes)

                if exito:
                    print(f"Compra registrada para {cliente['nombre']}. Puntos obtenidos: {puntos}")
                else:
                    print("Error: revise que el monto sea valido.")

        elif opcion == "3":
            print("\n--- CONSULTAR SALDO ---")
            cliente = seleccionar_cliente(clientes)
            if cliente is None:
                print("No hay clientes registrados.")
            else:
                print(f"Cliente: {cliente['nombre']}")
                print(f"Suscripcion: {cliente['suscripcion']}")
                print(f"Saldo: {consultar_saldo(cliente)} puntos")

        elif opcion == "4":
            print("\n--- HISTORIAL DE COMPRAS ---")
            historial_actual = mostrar_historial_compras(historial)

            if len(historial_actual) == 0:
                print("Todavia no hay compras registradas.")
            else:
                for compra in historial_actual:
                    print(f"* {compra['producto']} | ${compra['monto']} | {compra['puntos_obtenidos']} puntos")
        elif opcion == "5":
            print("\n--- RECOMPENSAS DISPONIBLES ---")
            cliente = seleccionar_cliente(clientes)
            if cliente is None:
                print("No hay clientes registrados.")
            else:
                disponibles = listar_recompensas_disponibles(cliente, recompensas)

                for recompensa in disponibles:
                    print(f"ID {recompensa['id']}: {recompensa['nombre']} - {recompensa['costo']} puntos")

        elif opcion == "6":
            print("\n--- CANJEAR RECOMPENSA ---")
            cliente = seleccionar_cliente(clientes)
            if cliente is None:
                print("No hay clientes registrados.")
            else:
                disponibles = listar_recompensas_disponibles(cliente, recompensas)

                for recompensa in disponibles:
                    print(f"ID {recompensa['id']}: {recompensa['nombre']} - {recompensa['costo']} puntos")

                id_recompensa = input("Ingrese el ID de la recompensa: ").strip()
                exito, mensaje = canjear_recompensa(cliente, recompensas, id_recompensa)
                print(mensaje)
                print(f"Saldo actual: {cliente['saldo_puntos']} puntos")
            
        elif opcion == "7":
            print("\n--- PLANES DE SUSCRIPCION ---")
            lista_planes = listar_planes(planes)

            for plan in lista_planes:
                print(f"{plan['plan']} | Precio: ${plan['precio']} | Beneficio: {plan['beneficio']} | Multiplicador: x{plan['multiplicador']}")

        elif opcion == "8":
            print("\n--- TOP PREMIUM ---")
            top = obtener_top_premium(ranking)

            for puesto, cliente_top in enumerate(top, start=1):
                print(f"{puesto}. {cliente_top['nombre']} - Total gastado: ${cliente_top['total_gastado']}")

        elif opcion == "9":
            print("\n--- DAR DE ALTA UN NUEVO CLIENTE ---")
            nombre_nuevo = input("Ingrese el nombre del nuevo cliente: ").strip()
            suscripcion_nueva = input("Ingrese la suscripcion del cliente (Basico, Explorer, Premium): ").strip()
            exito, mensaje = dar_alta_cliente(clientes, nombre_nuevo, suscripcion_nueva)
            print(mensaje)

        elif opcion == "10":
            print("\n--- DAR DE BAJA UN CLIENTE ---")
            nombre_baja = input("Ingrese el nombre del cliente a dar de baja: ").strip()
            exito, mensaje = dar_baja_cliente(clientes, nombre_baja)
            print(mensaje)

        elif opcion == "11":
            print("\n--- RECATEGORIZAR UN CLIENTE ---")
            cliente = seleccionar_cliente(clientes)
            if cliente is None:
                print("No hay clientes registrados.")
            else:
                print(f"Suscripcion actual: {cliente['suscripcion']}")
                nueva_suscripcion = input("Ingrese la nueva suscripcion (Basico, Explorer, Premium): ").strip()
                exito, mensaje = recategorizar_suscripcion(cliente, nueva_suscripcion, planes)
                print(mensaje)

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()
