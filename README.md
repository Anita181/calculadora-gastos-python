# calculadora-gastos-python
Calculadora de gastos personales en Python. Permite registrar, analizar y exportar gastos.
💸 Calculadora de Gastos Personales en Python
Una aplicación de consola interactiva que permite gestionar tus finanzas personales: registrar gastos, controlar presupuesto, generar reportes en PDF/CSV y visualizar estadísticas con gráficos.
🚀 Funcionalidades principales
Seguridad con contraseña 🔒 (protege el acceso a la calculadora).
Registro de gastos con fecha, descripción, categoría y etiquetas.
Presupuesto máximo y alertas al superar el 80% o 100%.
Meta de ahorro mensual 🎯 con avisos si no se está cumpliendo.
Límites por categoría 🗂️ con advertencias al superarlos.
Ingreso de dinero y cálculo automático de ahorro (ingresos - gastos).
Estadísticas rápidas: total, promedio, gasto más alto.
Búsqueda y filtros de gastos por palabra, categoría o etiquetas.
Edición y eliminación de gastos ya registrados.
Gráficos con Matplotlib:
Barras: gastos por categoría.
Circular (pastel): distribución porcentual.
Exportación de reportes:
PDF (reporte_gastos.pdf) con todos los gastos.
CSV (gastos.csv y resumen_por_categoria.csv).
Predicción de gastos 🔮 con base en el promedio diario del mes.
Guardado automático en CSV (persistencia de datos).
📂 Archivos incluidos
calculadora_gastos.py → Código principal en Python.
gastos.csv → Archivo donde se almacenan los gastos registrados.
resumen_por_categoria.csv → Exportación de resumen de gastos por categoría.
reporte_gastos.pdf → Reporte detallado en PDF generado automáticamente.

▶️ Cómo ejecutar

1. Clonar el repositorio: 
git clone https://github.com/anita181/calculadora-gastos-python.git
cd calculadora-gastos-python
2. Instalar dependencias necesarias:
pip install tabulate matplotlib fpdf
3. Ejecutar la aplicación:
python calculadora_gastos.py
4. Ingresa la contraseña 1234 para acceder.

🛠️ Tecnologías utilizadas

Python 3

CSV (persistencia de datos)
Matplotlib (visualización de gráficos)
FPDF (generación de reportes en PDF)
Tabulate (formato de tablas en consola)

📜 Licencia

Este proyecto está bajo la licencia MIT.
¡Siéntete libre de usarlo y mejorarlo! ✨
