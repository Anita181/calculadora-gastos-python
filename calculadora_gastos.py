from tabulate import tabulate
import csv
import os
import matplotlib.pyplot as plt
from fpdf import FPDF
CONTRASENA = "1234"  

intentos = 3
while intentos > 0:
    ingreso = input("🔒 Ingresa la contraseña para acceder a la calculadora: ")
    if ingreso == CONTRASENA:
        print("✅ Acceso concedido. Bienvenida, Any.")
        break
    else:
        intentos -= 1
        print(f"❌ Contraseña incorrecta. Te quedan {intentos} intento(s).")
        if intentos == 0:
            print("🚫 Acceso denegado. Programa finalizado.")
            exit()

print("💰 Bienvenida a tu Calculadora de Gastos Personales 💸")
gastos = []
if os.path.exists("gastos.csv"):
    with open("gastos.csv", mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            gastos.append({
                "cantidad": int(fila["Cantidad"]),
                "fecha": fila["Fecha"],
                "descripcion": fila["Descripción"],
                "categoria": fila["Categoría"],
                "etiquetas": fila.get("Etiquetas", "")  
            })
    print("✅ Gastos cargados correctamente desde gastos.csv")
else:
    print("📂 No se encontraron gastos guardados, empezando desde cero.")
presupuesto = input("💵 Ingresa tu presupuesto máximo (o deja vacío si no quieres límite): ")
if presupuesto.isdigit():
    presupuesto = int(presupuesto)
else:
    presupuesto = None
meta_ahorro = None
def buscar_gasto():
    palabra_clave = input("🔍 Ingresa una palabra para buscar en los gastos (descripción o categoría): ").lower()
    encontrados = []

    for gasto in gastos:
        descripcion = gasto["descripcion"].lower()
        categoria = gasto["categoria"].lower()

        if palabra_clave in descripcion or palabra_clave in categoria:
            encontrados.append(gasto)

    if encontrados:
        print("\n📌 Gastos encontrados:")
        for i, gasto in enumerate(encontrados, start=1):
            print(f"{i}. {gasto['fecha']} | {gasto['descripcion']} ({gasto['categoria']}) - {gasto['cantidad']} 💸")
    else:
        print("⚠️ No se encontraron gastos con esa palabra.")
limites_por_categoria = {}
ingresos = 0
while True:
    print("""
📌 MENÚ PRINCIPAL
1. Agregar gasto
2. Ver todos los gastos
3. Ver resumen por categoría
4. Eliminar un gasto
5. Salir
6. Ver gráfico de gastos por categoría
7. Ver gráfico circular (pastel)
8. Filtrar gastos por categoría o etiquet
9. Ver estadísticas rápidas
10. Exportar gastos a PDF
11. Editar un gasto registrado
12. Buscar gasto por nombre o categoría
13. Mostrar presupuesto restante
14. Establecer límite por categoría
15. Definir meta de ahorro mensual
16. Exportar resumen por categoría a CSV
17. Ver predicción de gastos para el mes
18. Registrar ingresos
""")
    opcion = input("Elige una opción (1-18): ")
    if opcion == "1":
        while True:
            cantidad_input = input("¿Cuánto gastaste? 💸: ")
            if cantidad_input.isdigit():
                cantidad = int(cantidad_input)
                break
            else:
                print("❌ Por favor ingresa un número válido.")

        while True:
            fecha = input("¿Fecha del gasto? 📅 (ej: 2025-08-13): ")
            if fecha.strip() != "":
                break
            else:
                print("❌ La fecha no puede estar vacía.")

        while True:
            descripcion = input("¿Descripción? 📝: ")
            if descripcion.strip() != "":
                break
            else:
                print("❌ La descripción no puede estar vacía.")

        while True:
            categoria = input("¿Categoría? 🗂️: ")
            if categoria.strip() != "":
                break
            else:
                print("❌ La categoría no puede estar vacía.")

        etiquetas = input("🏷️ Escribe etiquetas (separadas por comas, o deja vacío si no hay): ")

        gasto = {
            "cantidad": cantidad,
            "fecha": fecha,
            "descripcion": descripcion,
            "categoria": categoria,
            "etiquetas": etiquetas
        }
        gastos.append(gasto)
        print(f"✅ Gasto agregado: {fecha} | {descripcion} ({categoria}) - {cantidad} 💸")

        
        if categoria in limites_por_categoria:
            total_categoria = sum(
                g["cantidad"] for g in gastos
                if g["categoria"].lower() == categoria.lower()
            )
            limite = limites_por_categoria[categoria]
            if total_categoria > limite:
                print(f"⚠️ Has superado el límite de {limite} 💸 para '{categoria}'. Total: {total_categoria} 💸")
            elif total_categoria >= limite * 0.8:
                print(f"🔔 Atención: 80% del límite de '{categoria}' alcanzado ({total_categoria}/{limite} 💸)")

        
        total_gastado = sum(g["cantidad"] for g in gastos)
        if presupuesto is not None:
            if total_gastado >= presupuesto:
                print(f"⚠️ Has superado tu presupuesto de {presupuesto} 💸. Total: {total_gastado} 💸")
            elif total_gastado >= presupuesto * 0.8:
                print(f"🔔 Ya has gastado el 80% de tu presupuesto ({total_gastado}/{presupuesto} 💸)")

          
            if meta_ahorro is not None:
                posible_ahorro = presupuesto - total_gastado
                if posible_ahorro < meta_ahorro:
                    print(f"⚠️ Con este ritmo no podrás ahorrar tu meta de {meta_ahorro} 💸.")

    
        if ingresos:
            ahorro_actual = ingresos - total_gastado
            print(f"💡 Ahorro actual (ingresos - gastos): {ahorro_actual} 💸")
    
    elif opcion == "2":
        if gastos:
            total_gastado = sum(g["cantidad"] for g in gastos)
            tabla = []
            for i, gasto in enumerate(gastos, start=1):
                porcentaje = (gasto["cantidad"] / total_gastado) * 100 if total_gastado > 0 else 0
                tabla.append([
                    i,
                    gasto["cantidad"],
                    gasto["fecha"],
                    gasto["descripcion"],
                    gasto["categoria"],
                    gasto["etiquetas"],
                    f"{porcentaje:.2f}%"
                ])

            print("\n📊 Tabla de gastos con porcentaje de participación:\n")
            print(tabulate(
                tabla,
                headers=["N°", "Cantidad 💸", "Fecha 📅", "Descripción 📝", "Categoría 🗂️", "Etiquetas 🏷️", "Participación %"],
                tablefmt="grid"
                ))
            print(f"\n💵 Total gastado: {total_gastado} 💸\n")
        else:
            print("📂 No hay gastos registrados.")
    elif opcion == "3":
        if gastos:
            resumen_categorias = {}
            for gasto in gastos:
                categoria = gasto["categoria"]
                if categoria in resumen_categorias:
                    resumen_categorias[categoria] += gasto["cantidad"]
                else:
                    resumen_categorias[categoria] = gasto["cantidad"]

            print("\n📂 Resumen por categoría:")
            for categoria, total in resumen_categorias.items():
                print(f"- {categoria}: {total} 💸")
        else:
            print("📂 No hay gastos registrados para mostrar resumen.")
    elif opcion == "4":
        if gastos:
            try:
                numero = int(input("❌ ¿Qué número de gasto quieres eliminar? (escribe el número): "))
                if 1 <= numero <= len(gastos):
                    del gastos[numero - 1]
                    print("✅ Gasto eliminado correctamente.")
                else:
                    print("❌ Número no válido.")
            except ValueError:
                print("❌ Debes escribir un número.")
        else:
            print("📂 No hay gastos registrados para eliminar.")
    elif opcion == "5":
        print("👋 ¡Gracias por usar la calculadora! Todos los cambios se han guardado.")
        break
    elif opcion == "6":
        if gastos:
            resumen_categorias = {}
            for gasto in gastos:
                categoria = gasto["categoria"]
                if categoria in resumen_categorias:
                    resumen_categorias[categoria] += gasto["cantidad"]
                else:
                    resumen_categorias[categoria] = gasto["cantidad"]

            # Crear gráfico
            categorias = list(resumen_categorias.keys())
            cantidades = list(resumen_categorias.values())

            plt.figure(figsize=(7, 5))
            plt.bar(categorias, cantidades)
            plt.title("Gastos por categoría")
            plt.xlabel("Categorías")
            plt.ylabel("Cantidad gastada 💸")
            plt.show()
        else:
            print("📂 No hay gastos registrados para mostrar gráfico.")

    elif opcion == "7":
        if gastos:
            resumen_categorias = {}
            for gasto in gastos:
                categoria = gasto["categoria"]
                if categoria in resumen_categorias:
                    resumen_categorias[categoria] += gasto["cantidad"]
                else:
                    resumen_categorias[categoria] = gasto["cantidad"]

            # Crear gráfico circular
            categorias = list(resumen_categorias.keys())
            cantidades = list(resumen_categorias.values())

            plt.figure(figsize=(7, 7))
            plt.pie(cantidades, labels=categorias, autopct="%1.1f%%", startangle=90)
            plt.title("Distribución de gastos por categoría")
            plt.show()
        else:
            print("📂 No hay gastos registrados para mostrar gráfico circular.")
    elif opcion == "8":
        if gastos:
            filtro = input("🔍 Escribe la categoría o etiqueta que quieres buscar: ").strip().lower()
            gastos_filtrados = []

            for i, gasto in enumerate(gastos, start=1):
                if filtro in gasto["categoria"].lower() or filtro in gasto["etiquetas"].lower():
                    gastos_filtrados.append([
                        i,
                        gasto["cantidad"],
                        gasto["fecha"],
                        gasto["descripcion"],
                        gasto["categoria"],
                        gasto["etiquetas"]
                    ])

            if gastos_filtrados:
                print("\n📊 Gastos filtrados:\n")
                print(tabulate(
                    gastos_filtrados,
                    headers=["N°", "Cantidad 💸", "Fecha 📅", "Descripción 📝", "Categoría 🗂️", "Etiquetas 🏷️"],
                    tablefmt="grid"))
            else:
                print(f"📂 No se encontraron gastos con '{filtro}'.")
        else:
            print("📂 No hay gastos registrados para filtrar.")

    elif opcion == "9":
        if gastos:
            total_gastado = sum(g["cantidad"] for g in gastos)
            ahorro_actual = ingresos - total_gastado
            print(f"✅ Ahorro actual (ingresos - gastos): {ahorro_actual} 💸")
            numero_gastos = len(gastos)
            promedio_gasto = total_gastado / numero_gastos if numero_gastos > 0 else 0
            gasto_mas_alto = max(gastos, key=lambda g: g["cantidad"])

            print("\n📊 ESTADÍSTICAS RÁPIDAS 📊")
            print(f"✅ Total gastado: {total_gastado} 💸")
            print(f"✅ Número de gastos: {numero_gastos}")
            print(f"✅ Promedio por gasto: {promedio_gasto:.2f} 💸")
            print(f"✅ Gasto más alto: {gasto_mas_alto['cantidad']} 💸 - "
                  f"{gasto_mas_alto['descripcion']} ({gasto_mas_alto['categoria']})")
        else:
            print("📂 No hay gastos registrados para mostrar estadísticas.")

    elif opcion == "10":
        if gastos:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Reporte de Gastos", ln=True, align="C")

            pdf.set_font("Arial", "", 10)
            pdf.ln(10)

            for i, gasto in enumerate(gastos, start=1):
                linea = f"{i}. {gasto['fecha']} - {gasto['descripcion']} - {gasto['categoria']} - {gasto['cantidad']} Bs"
                if gasto["etiquetas"]:
                    linea += f" ({gasto['etiquetas']})"
                pdf.multi_cell(0, 8, linea)

            try:
                pdf.output("reporte_gastos.pdf")
                print("✅ Gastos exportados correctamente en 'reporte_gastos.pdf'")
            except Exception as e:
                print(f"❌ Error al guardar el PDF: {e}")
        else:
            print("📂 No hay gastos registrados para exportar.")

    elif opcion == "11":
        if gastos:
            try:
                numero = int(input("✏️ ¿Qué número de gasto deseas editar? (escribe el número): "))
                if 1 <= numero <= len(gastos):
                    gasto = gastos[numero - 1]
                    print(f"\nEditando gasto {numero}:")
                    print(f"Actual: {gasto['fecha']} - {gasto['descripcion']} - {gasto['categoria']} - {gasto['cantidad']} 💸 ({gasto['etiquetas']})")

                    nueva_fecha = input(f"📅 Nueva fecha (enter para mantener '{gasto['fecha']}'): ") or gasto["fecha"]
                    nueva_descripcion = input(f"📝 Nueva descripción (enter para mantener '{gasto['descripcion']}'): ") or gasto["descripcion"]
                    nueva_categoria = input(f"🗂️ Nueva categoría (enter para mantener '{gasto['categoria']}'): ") or gasto["categoria"]
                    nueva_etiquetas = input(f"🏷️ Nuevas etiquetas (enter para mantener '{gasto['etiquetas']}'): ") or gasto["etiquetas"]

                    while True:
                        nueva_cantidad = input(f"💸 Nueva cantidad (enter para mantener '{gasto['cantidad']}'): ")
                        if nueva_cantidad == "":
                            nueva_cantidad = gasto["cantidad"]
                            break
                        elif nueva_cantidad.isdigit():
                            nueva_cantidad = int(nueva_cantidad)
                            break
                        else:
                            print("❌ Ingresa un número válido o presiona Enter para no modificar.")

                    gastos[numero - 1] = {
                        "fecha": nueva_fecha,
                        "descripcion": nueva_descripcion,
                        "categoria": nueva_categoria,
                        "etiquetas": nueva_etiquetas,
                        "cantidad": nueva_cantidad
                    }
                    print("✅ Gasto actualizado correctamente.")
                else:
                    print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes escribir un número.")
        else:
            print("📂 No hay gastos registrados para editar.")
    elif opcion == "12":
        buscar_gasto()

    elif opcion == "13":
        if presupuesto is not None:
            total_gastado = sum(g["cantidad"] for g in gastos)
            restante = presupuesto - total_gastado
            print(f"\n💡 Presupuesto máximo: {presupuesto} 💸")
            print(f"💸 Total gastado: {total_gastado} 💸")
            print(f"🟢 Presupuesto restante: {restante} 💸")

            if restante <= 0:
                print("⚠️ Has alcanzado o superado tu presupuesto.")
            elif restante <= presupuesto * 0.2:
                print("🔔 ¡Cuidado! Solo te queda el 20% del presupuesto.")
        else:
            print("⚠️ No has definido un presupuesto máximo")

    elif opcion == "14":
        categoria = input("🗂️ ¿A qué categoría deseas ponerle un límite? ").strip()
        if categoria == "":
            print("❌ La categoría no puede estar vacía.")
        else:
            limite = input(f"💰 Ingresa el límite de gasto para '{categoria}': ")
            if limite.isdigit():
                limites_por_categoria[categoria] = int(limite)
                print(f"✅ Límite de {limite} 💸 establecido para la categoría '{categoria}'.")
            else:
                print("❌ El límite debe ser un número válido.")

    elif opcion == "15":
        entrada_meta = input("🎯 Ingresa tu meta de ahorro mensual (en Bs): ")
        if entrada_meta.isdigit():
            meta_ahorro = int(entrada_meta)
            print(f"✅ Meta de ahorro mensual establecida en {meta_ahorro} 💸")
        else:
            print("❌ La meta de ahorro debe ser un número válido.")

    elif opcion == "16":
        if gastos:
            resumen_categorias = {}
            for gasto in gastos:
                categoria = gasto["categoria"]
                if categoria in resumen_categorias:
                    resumen_categorias[categoria] += gasto["cantidad"]
                else:
                    resumen_categorias[categoria] = gasto["cantidad"]

            nombre_archivo = "resumen_por_categoria.csv"
            try:
                with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
                    escritor = csv.writer(archivo_csv)
                    escritor.writerow(["Categoría", "Total gastado 💸"])

                    for categoria, total in resumen_categorias.items():
                        escritor.writerow([categoria, total])

                print(f"✅ Resumen exportado exitosamente en '{nombre_archivo}'")
            except Exception as e:
                print(f"❌ Error al exportar el archivo: {e}")
        else:
            print("📂 No hay gastos registrados para exportar.")

    elif opcion == "17":
        from datetime import datetime

        if gastos:
            try:
                hoy = datetime.today()
                dia_actual = hoy.day

                total_gastado = sum(g["cantidad"] for g in gastos)
                promedio_diario = total_gastado / dia_actual
                prediccion = promedio_diario * 30  # Estimación para un mes de 30 días

                print(f"\n📊 Has gastado {total_gastado} 💸 en {dia_actual} días.")
                print(f"📈 Promedio diario: {promedio_diario:.2f} 💸")
                print(f"🔮 Si sigues así, gastarás aproximadamente {prediccion:.2f} 💸 este mes.")

               
                if presupuesto:
                    if prediccion > presupuesto:
                        print(f"⚠️ Esta predicción supera tu presupuesto de {presupuesto} 💸.")
                    else:
                        print(f"✅ Estás dentro de tu presupuesto de {presupuesto} 💸.")

                    gasto_diario_ideal = presupuesto / 30
                    print(f"💡 Para cumplir tu presupuesto, deberías gastar como máximo {gasto_diario_ideal:.2f} 💸 por día.")

                
                if presupuesto and meta_ahorro:
                    max_gasto_para_ahorrar = presupuesto - meta_ahorro

                    if prediccion > max_gasto_para_ahorrar:
                        print(f"⚠️ Con esta predicción, no lograrás tu meta de ahorro de {meta_ahorro} 💸.")
                    else:
                        print(f"✅ Vas bien para alcanzar tu meta de ahorro de {meta_ahorro} 💸.")

                    gasto_diario_para_ahorrar = max_gasto_para_ahorrar / 30
                    print(f"💡 Para ahorrar {meta_ahorro} 💸, deberías gastar como máximo {gasto_diario_para_ahorrar:.2f} 💸 por día.")

            except Exception as e:
                print(f"❌ Error al calcular la predicción: {e}")
        else:
            print("📂 No hay gastos registrados para hacer una predicción.")

    elif opcion == "18":
        entrada_ingreso = input("💰 Ingresa el monto de ingresos: ")
        if entrada_ingreso.isdigit():
            ingresos += int(entrada_ingreso)
            print(f"✅ Ingreso registrado. Total de ingresos acumulados: {ingresos} 💸")
            ahorro = ingresos - sum(g["cantidad"] for g in gastos)
            print(f"💡 Ahorro actual: {ahorro} 💸")
        else:
            print("❌ El ingreso debe ser un número válido.")

with open("gastos.csv", mode="w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Cantidad", "Fecha", "Descripción", "Categoría", "Etiquetas"])  # Encabezados

    for gasto in gastos:
        escritor.writerow([gasto["cantidad"], gasto["fecha"], gasto["descripcion"], gasto["categoria"], gasto["etiquetas"]])

    print("💾 Gastos guardados en 'gastos.csv'")

    




    # opcion = input("¿Quieres agregar un gasto? (sí / salir): ")
    # if opcion.lower() == "salir":
    #     break  # esto rompe el bucle
    # while True:
    #     cantidad_input = input("¿Cuánto gastaste? 💸: ")
    #     if cantidad_input.isdigit():
    #         cantidad = int(cantidad_input)
    #         break
    #     else:
    #         print("❌ Por favor ingresa un número válido.")
    # while True:
    #     fecha = input("¿Fecha del gasto? 📅: ")
    #     if fecha.strip() != "":
    #         break
    #     else:
    #         print("❌ La fecha no puede estar vacía.")
    # while True:
    #     descripcion = input("¿Descripción? 📝: ")
    #     if descripcion.strip() != "":
    #         break
    #     else:
    #         print("❌ La descripcion no puede estar vacía.")
    # while True:
    #     categoria = input("¿Categoría? 🗂️: ")
    #     if categoria.strip() != "":
    #         break
    #     else:
    #         print("❌ La categoria no puede estar vacía.")
#     gasto = {
#         "cantidad": cantidad,
#         "fecha": fecha,
#         "descripcion": descripcion,
#         "categoria": categoria
#     }
#     gastos.append(gasto)

# print("\n🧾 Todos tus gastos registrados:\n")

# for i, gasto in enumerate(gastos, start=1):
#     print(f"Gasto {i}:")
#     print(f"  💸 Cantidad: {gasto['cantidad']}")
#     print(f"  📅 Fecha: {gasto['fecha']}")
#     print(f"  📝 Descripción: {gasto['descripcion']}")
#     print(f"  🗂️ Categoría: {gasto['categoria']}")
#     print("-" * 30)
# ver_categoria = input("🔍 ¿Quieres ver los gastos de una categoría específica? (sí / no): ")
# if ver_categoria.lower() in ["sí", "si"]:
#     categoria_filtrada = input("🗂️ Escribe la categoría que quieres ver: ")
#     print(f"\n📂 Gastos en la categoría: {categoria_filtrada}\n")
#     for gasto in gastos:
#         if gasto["categoria"].lower() == categoria_filtrada.lower():
#             print(f"  💸 Cantidad: {gasto['cantidad']}")
#             print(f"  📅 Fecha: {gasto['fecha']}")
#             print(f"  📝 Descripción: {gasto['descripcion']}")
#             print("-" * 30)
# else:
#     print("👋 ¡Gracias por usar la calculadora!")
# total = 0
# for gasto in gastos:
#     total += gasto["cantidad"]
# print(f"\n🧮 Total gastado: {total}")
# valor_mas_alto = 0
# gasto_mas_alto = None
# for gasto in gastos:
#     if gasto["cantidad"] > valor_mas_alto:
#         valor_mas_alto = gasto["cantidad"]
#         gasto_mas_alto = gasto
# if gasto_mas_alto:
#     print(f"\n🏆 El gasto más alto fue de {gasto_mas_alto['cantidad']} 💸")
#     print(f"   📅 Fecha: {gasto_mas_alto['fecha']}")
#     print(f"   📝 Descripción: {gasto_mas_alto['descripcion']}")
#     print(f"   🗂️ Categoría: {gasto_mas_alto['categoria']}")

# eliminar = input("❌ ¿Quieres eliminar un gasto? (sí / no): ")
# if eliminar.lower() in ["sí", "si"]:
#     numero = int(input("¿Qué número de gasto quieres eliminar? (escribe el número): "))
#     if 1 <= numero <= len(gastos):
#         del gastos[numero - 1]
#         print("✅ Gasto eliminado correctamente.")
#     else:
#         print("❌ Número no válido.")
# print("\n🧾 Lista actualizada de gastos:\n")
# if gastos:
#     tabla = []
#     for i, gasto in enumerate(gastos, start=1):
#         tabla.append([i, gasto["cantidad"], gasto["fecha"], gasto["descripcion"], gasto["categoria"]])

#     print("\n📊 Tabla de gastos:\n")
#     print(tabulate(tabla, headers=["N°", "Cantidad 💸", "Fecha 📅", "Descripción 📝", "Categoría 🗂️"], tablefmt="grid"))
# else:
#     print("No hay gastos registrados.")

# resumen_categorias = {}
# for gasto in gastos:
#     categoria = gasto["categoria"]
#     if categoria in resumen_categorias:
#         resumen_categorias[categoria] += gasto["cantidad"]
#     else:
#         resumen_categorias[categoria] = gasto["cantidad"]
# print("\n📂 Resumen por categoría:")
# for categoria, total in resumen_categorias.items():
#     print(f"- {categoria}: {total} 💸")
# with open("gastos.csv", mode="w", newline="", encoding="utf-8") as archivo:
#     escritor = csv.writer(archivo)
#     escritor.writerow(["Cantidad", "Fecha", "Descripción", "Categoría"])  # Encabezados

#     for gasto in gastos:
#         escritor.writerow([gasto["cantidad"], gasto["fecha"], gasto["descripcion"], gasto["categoria"]])

# print("💾 Gastos guardados en 'gastos.csv'")


