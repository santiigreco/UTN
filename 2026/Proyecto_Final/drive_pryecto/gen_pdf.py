from fpdf import FPDF

class AuditPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Auditoría Factibilidad Comercial - Proyecto Final G8 - UTN FRBA", align="C")
        self.ln(8)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title, r=26, g=35, b=126):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(r, g, b)
        self.ln(4)
        self.cell(0, 9, title)
        self.ln(5)
        self.set_draw_color(r, g, b)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def sub_title(self, title, r=40, g=53, b=147):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(r, g, b)
        self.ln(2)
        self.cell(0, 7, title)
        self.ln(8)

    def body_text(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, txt)
        self.ln(2)

    def bold_text(self, txt):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, txt)
        self.ln(2)

    def alert_box(self, txt, r=255, g=243, b=224, br=255, bg=152, bb=0):
        self.set_fill_color(r, g, b)
        self.set_draw_color(br, bg, bb)
        x = self.get_x()
        y = self.get_y()
        self.set_font("Helvetica", "I", 9.5)
        self.set_text_color(80, 50, 0)
        self.rect(10, y, 190, 1, "F")
        self.set_x(14)
        self.multi_cell(182, 5, txt, fill=True)
        self.ln(3)

    def simple_table(self, headers, data, col_widths=None):
        if col_widths is None:
            w = 190 / len(headers)
            col_widths = [w] * len(headers)
        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(26, 35, 126)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Data
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        for row_idx, row in enumerate(data):
            if row_idx % 2 == 0:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6, cell, border=1, fill=True)
            self.ln()
        self.ln(3)


pdf = AuditPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(26, 35, 126)
pdf.cell(0, 12, "Auditoría - Factibilidad Comercial", align="C")
pdf.ln(10)
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, "Proyecto Final G8 - Planta Sin TACC ('Celi')", align="C")
pdf.ln(7)
pdf.set_font("Helvetica", "I", 10)
pdf.cell(0, 6, "12 de mayo de 2026  |  Referencia: Guía v17, UTN FRBA §3.1", align="C")
pdf.ln(12)

# ============================================================
# CHECKLIST
# ============================================================
pdf.section_title("Checklist de Cobertura vs. Guía v17 §3.1")

headers = ["# Guía", "Requerimiento", "Cubierto", "Observación"]
widths = [18, 72, 18, 82]
data = [
    ["3.1.1", "Análisis de contexto (Macro entorno)", "SI", "Bien desarrollado"],
    ["3.1.2", "Variables Endógenas y Exógenas", "SI", "Listadas correctamente"],
    ["3.1.3", "Micro entorno: Porter", "PARCIAL", "No estructurado como 5 fuerzas"],
    ["3.1.4", "FODA / Diferenciación / BCG / Penetración", "PARCIAL", "Falta BCG y penetración explícita"],
    ["3.1.5", "Investigación de mercado", "PARCIAL", "Falta invest. primaria y ciclo vida"],
    ["3.1.6", "Misión / Visión / Objetivos / Metas", "SI", "Completo"],
    ["3.1.7", "Macrolocalización", "SI", "Verificada aritméticamente OK"],
    ["3.1.8", "Mix de Marketing (4P)", "SI", "Las 4P desarrolladas"],
    ["3.1.9", "Plan de Ventas", "SI", "Unidades y monetario a 10 años"],
]
pdf.simple_table(headers, data, widths)

pdf.bold_text("Entregables requeridos por la guía:")
headers2 = ["Entregable", "Presente", "Observación"]
widths2 = [55, 25, 110]
data2 = [
    ["Market Share", "PARCIAL", "Declarado pero con errores numéricos (ver C2)"],
    ["Estrategia y plan comercial", "SI", "A través de las 4P y diferenciación"],
    ["Proyección de ventas", "SI", "Tablas a 10 años"],
    ["Costos Comerciales", "SI", "Sección 8 detallada"],
]
pdf.simple_table(headers2, data2, widths2)

# ============================================================
# CRITICOS
# ============================================================
pdf.section_title("CRÍTICO - Errores que deben corregirse", 183, 28, 28)

pdf.sub_title("C1. Contradicción: Vegano/Libre de alérgenos vs. Materias primas", 183, 28, 28)
pdf.body_text('La definición inicial establece: "libre de gluten, libre de alérgenos, formulación vegana".')
pdf.body_text("Sin embargo, en Producto (§5.1) se listan como materias primas:")
pdf.body_text("  - Huevo -> alérgeno mayor según ANMAT, NO vegano\n  - Leche -> alérgeno mayor, NO vegano\n  - Lecitina de soja -> alérgeno (soja es uno de los 8 alérgenos principales)")
pdf.alert_box("Esto es una contradicción directa que un jurado detecta inmediatamente. Destruye la credibilidad de la propuesta de valor y la estrategia de diferenciación.")
pdf.bold_text('Solución: Clasificar cada SKU en tabla indicando cuáles son veganos y cuáles contienen alérgenos. Reformular la definición a "incluye opciones veganas y libres de alérgenos".')

pdf.sub_title("C2. Market share año 10: el cálculo está mal", 183, 28, 28)
pdf.body_text("El documento declara alcanzar un 7,77% de market share al año 10. Pero si el mercado crece al 4% anual (como se declara), el denominador también crece:")
headers3 = ["Parámetro", "Valor documento", "Valor recalculado"]
widths3 = [70, 60, 60]
data3 = [
    ["Mercado año 2 (base)", "7.321.640 kg", "7.321.640 kg"],
    ["Mercado año 10 (4% x 8 años)", "No calculado", "~10.020.170 kg"],
    ["Producción año 10", "~3.101k unidades", "~553.610 kg"],
    ["Market share real año 10", "7,77%", "~5,5%"],
]
pdf.simple_table(headers3, data3, widths3)
pdf.body_text("Causa: Se calcula el share sobre el mercado estático del año 2 en vez del mercado que también crece al 4% anual.")

pdf.sub_title("C3. Ahorro logístico: error aritmético", 183, 28, 28)
pdf.body_text('El documento dice "ahorro aproximado del 50%" entre logística propia ($119.960.000) y tercerizada ($66.000.000).')
pdf.body_text("Cálculo real: (119.960.000 - 66.000.000) / 119.960.000 = 44,98% ~= 45%, no 50%. Además, no se presenta desglose de ninguna de las dos cifras.")

# ============================================================
# INCONSISTENCIAS
# ============================================================
pdf.section_title("INCONSISTENCIAS - Lógica que flaquea", 230, 126, 34)

pdf.sub_title("I1. Market share por categoría: desbalance extremo", 200, 100, 0)
headers4 = ["Categoría", "Share año 2 real", "Observación"]
widths4 = [55, 35, 100]
data4 = [
    ["Galletitas dulces", "~22%", "Se aspira a 24,58%. Agresivo para empresa nueva"],
    ["Galletitas saladas", "~0,85%", "Insignificante"],
    ["Panificados", "~3,4%", "Moderado"],
]
pdf.simple_table(headers4, data4, widths4)
pdf.body_text("Declarar que se será el 2do jugador en galletitas dulces sin TACC en el primer año contradice las propias barreras de entrada identificadas.")

pdf.sub_title("I2. Confusión entre market share inicial y final", 200, 100, 0)
headers5 = ["Sección", "Cifra", "Contexto"]
widths5 = [30, 20, 140]
data5 = [
    ["§4.2", "7%", '"abarcar aproximadamente el 7% de market share"'],
    ["§9", "5,27%", '"abarcar un 5,27% del mercado de manera inicial"'],
    ["§6.3", "7%", '"participación de al menos 7% en 10 años" (SMART)'],
    ["§9 final", "7,77%", '"al final del ciclo de vida del proyecto (año 10)"'],
]
pdf.simple_table(headers5, data5, widths5)
pdf.body_text("Hay que unificar y ser preciso sobre cuál es el objetivo y cuál el punto de partida.")

pdf.sub_title("I3. Consumo per cápita ENGHo no aplica al segmento sin TACC", 200, 100, 0)
pdf.body_text("Se usa la ENGHo del INDEC (población general, productos con gluten) para estimar consumo per cápita de celíacos. Un celíaco no consume la misma proporción de panificados: son más caros, menos disponibles y de diferente textura. Esto probablemente sobreestima la demanda de panificados.")

pdf.sub_title("I4. Exportación: promovida en macroentorno, descartada en plaza", 200, 100, 0)
pdf.body_text('En el macroentorno se dedican dos párrafos a exportar a LATAM y EE.UU. Pero en Plaza se dice "Se ha definido una política de No Exportación". Si no van a exportar, el macroentorno no debería promoverla como oportunidad clave.')

pdf.sub_title("I5. Tasas de crecimiento reales difieren de las declaradas", 200, 100, 0)
headers6 = ["Período", "Tasa declarada", "Tasa real en tabla"]
widths6 = [63, 63, 63]
data6 = [
    ["Año 2 -> 3", "4,0%", "4,16%"],
    ["Año 3 -> 4", "4,0%", "4,31%"],
    ["Año 4 -> 5", "4,5%", "4,77%"],
    ["Año 5 -> 6", "4,5%", "4,71%"],
    ["Año 6 -> 7", "4,5%", "4,77%"],
]
pdf.simple_table(headers6, data6, widths6)
pdf.body_text("Las diferencias son menores pero sistemáticas (~0,3pp). Probablemente redondeo, pero debería explicarse.")

pdf.sub_title('I6. Fila "Total" en tabla de precios sin sentido', 200, 100, 0)
pdf.body_text("La fila TOTAL muestra $22.615 en la columna de precio unitario. Es la suma de 11 precios, sin significado económico. Debería ser promedio ponderado o eliminarse.")

pdf.sub_title("I7. Porter no estructurado como 5 Fuerzas", 200, 100, 0)
pdf.body_text("La guía pide 'Micro entorno: Porter'. El documento cubre los contenidos pero no nombra el modelo, no usa los 5 encabezados formales, y falta la conclusión sobre intensidad de la rivalidad.")

# ============================================================
# DATOS Y DETALLES
# ============================================================
pdf.section_title("DATOS Y DETALLES - Faltantes según la guía", 21, 101, 192)

items = [
    ("D1. Falta: Análisis BCG", "La guía pide BCG en §3.1.4. Categorizar los 11 SKUs como Estrellas, Vacas, Interrogantes o Perros."),
    ("D2. Falta: Estrategia de penetración explícita", "La guía pide 'Penetración'. Formalizar precios de penetración, ramp-up por canal, hitos de distribución."),
    ("D3. Falta: Investigación primaria", "La guía lista Encuestas, Focus, Entrevistas. El documento solo usa fuentes secundarias. Una encuesta a celíacos fortalecería la validación."),
    ("D4. Falta: Ciclo de vida del producto", "La guía pide 'Ciclo de vida'. No se analiza si el mercado sin TACC está en crecimiento o madurez."),
    ("D5. Falta: Elasticidad precio-demanda", "La guía pide 'Elasticidad' en Precio. Se menciona cualitativamente pero no se cuantifica."),
    ("D6. Falta: Análisis de portfolio de precios", "No se explica la lógica de pricing entre líneas Gourmet vs. Estándar vs. Free."),
    ("D7. Factor 1,6 sin fuente", "Se usa 1,6 sobre la población celíaca para demanda periférica sin citar fuente. La diferencia entre 1,3 y 2,0 impacta ±25%."),
    ("D8. Datos de Smams sin fuente citada", "Se usan ventas 2025 de Smams como benchmark sin indicar origen. Toda cifra necesita fuente."),
    ("D9. Precio '8 veces' sin fuente precisa", "Probablemente cierto para pan francés pero no para todas las categorías. Citar fuente o moderar."),
    ("D10. Nombre inconsistente", "Portada dice 'Celi', versiones previas 'Naturalis'. Formalizar la marca."),
    ("D11. Falta: Comparativo con productos similares", "La guía pide comparativo en Producto. No hay cuadro Celi vs. Smams vs. Schar vs. Bio."),
    ("D12. Falta: Empaque y etiqueta detallados", "La guía pide 'Empaque y etiqueta'. Solo se define gramaje, falta material, sellado e información obligatoria."),
]

for title, desc in items:
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 6, title)
    pdf.ln(6)
    pdf.body_text(desc)

# ============================================================
# RESUMEN
# ============================================================
pdf.section_title("Resumen y Prioridades")

headers7 = ["Nivel", "Cantidad", "Impacto"]
widths7 = [63, 63, 63]
data7 = [
    ["CRÍTICO", "3", "Errores que invalidan argumentos clave"],
    ["INCONSISTENCIAS", "7", "Debilitan coherencia interna"],
    ["DATOS Y DETALLES", "12", "Variables pedidas por la guía ausentes"],
    ["TOTAL", "22", "-"],
]
pdf.simple_table(headers7, data7, widths7)

pdf.sub_title("Lo que está bien hecho")
buenos = [
    "Macroentorno sólido con datos actualizados (REM, Monitor MinSalud)",
    "Proveedores con nombre propio - valioso y poco común",
    "Costos comerciales detallados con valores referenciales reales",
    "Macrolocalización correcta - verificada aritméticamente sin errores",
    "Plan de ventas a 10 años con desglose por SKU",
    "Estrategia B2B realista con conocimiento del retail",
    "FODA completa - cubre F/D/O/A",
    "Estrategia de diferenciación bien argumentada",
]
for b in buenos:
    pdf.body_text(f"  OK  {b}")

pdf.sub_title("Prioridades de corrección (ordenadas por impacto)")
headers8 = ["#", "Acción", "Esfuerzo", "Impacto"]
widths8 = [10, 120, 30, 30]
data8 = [
    ["1", "Resolver contradicción vegano/alérgenos", "Bajo", "Altísimo"],
    ["2", "Recalcular market share año 10", "Medio", "Alto"],
    ["3", "Unificar cifras market share", "Bajo", "Alto"],
    ["4", "Estructurar Porter como 5 fuerzas", "Medio", "Alto"],
    ["5", "Agregar matriz BCG", "Medio", "Medio"],
    ["6", "Agregar ciclo de vida", "Bajo", "Medio"],
    ["7", "Investigación primaria (encuesta)", "Alto", "Alto"],
    ["8", 'Corregir "50%" -> "45%" logística', "Bajo", "Bajo"],
    ["9", "Cuadro comparativo vs. competencia", "Medio", "Medio"],
    ["10", "Detallar empaque y etiqueta", "Medio", "Medio"],
]
pdf.simple_table(headers8, data8, widths8)

out_path = r"d:\Descargas\UTN\Repo-UTN\2026\Proyecto_Final\drive_pryecto\Auditoria_Comercial_G8.pdf"
pdf.output(out_path)
print(f"PDF generado exitosamente: {out_path}")
