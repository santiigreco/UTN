from pathlib import Path
from math import ceil

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image as RLImage,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE = Path(__file__).resolve().parent
OUT = BASE / "TP2_Edificios_Industriales_Grupo5_CORREGIDO_EJ5_COMPLETO.pdf"
ASSET_DIR = BASE / "_tp2_corregido_assets"
ASSET_DIR.mkdir(exist_ok=True)


def font(size=18):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def draw_grid(draw, x0, y0, cols, rows, dx, dy):
    for c in range(cols):
        x = x0 + c * dx
        draw.line((x, y0, x, y0 + (rows - 1) * dy), fill=(120, 120, 120), width=2)
    for r in range(rows):
        y = y0 + r * dy
        draw.line((x0, y, x0 + (cols - 1) * dx, y), fill=(120, 120, 120), width=2)
    for c in range(cols):
        for r in range(rows):
            x = x0 + c * dx
            y = y0 + r * dy
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(30, 30, 30))


def draw_beam(draw, x1, y1, x2, y2, color, label="", width=12):
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        draw.text((mx - 35, my - 26), label, fill=color, font=font(16))


def draw_arrow_down(draw, x, y, label="Q"):
    draw.line((x, y - 45, x, y + 20), fill=(210, 30, 30), width=7)
    draw.polygon([(x - 16, y + 20), (x + 16, y + 20), (x, y + 48)], fill=(210, 30, 30))
    draw.text((x + 18, y - 12), label, fill=(210, 30, 30), font=font(20))


def add_legend(draw, x, y):
    items = [
        ((35, 130, 210), "Ultimo nivel"),
        ((45, 155, 90), "Nivel intermedio"),
        ((240, 170, 35), "Nivel intermedio"),
        ((210, 65, 65), "Primer nivel / nodos"),
    ]
    for i, (color, text) in enumerate(items):
        yy = y + i * 28
        draw.line((x, yy, x + 38, yy), fill=color, width=8)
        draw.text((x + 48, yy - 10), text, fill=(40, 40, 40), font=font(14))


def scheme_ex1(path):
    im = Image.new("RGB", (900, 520), "white")
    d = ImageDraw.Draw(im)
    d.text((30, 25), "P.1.1 - Reparto simetrico en 16 nodos", fill=(20, 20, 20), font=font(24))
    x0, y0, dx, dy = 110, 100, 155, 80
    draw_grid(d, x0, y0, 5, 5, dx, dy)
    draw_arrow_down(d, x0 + 2.5 * dx, y0 + 2 * dy, "Q=3900")
    draw_beam(d, x0 + 1 * dx, y0 + 2 * dy, x0 + 4 * dx, y0 + 2 * dy, (35, 130, 210), "N4")
    draw_beam(d, x0 + 1 * dx, y0 + 1 * dy, x0 + 1 * dx, y0 + 3 * dy, (45, 155, 90), "N3")
    draw_beam(d, x0 + 4 * dx, y0 + 1 * dy, x0 + 4 * dx, y0 + 3 * dy, (45, 155, 90), "N3")
    for c in [1, 2, 3, 4]:
        draw_beam(d, x0 + c * dx - 55, y0 + dy, x0 + c * dx + 55, y0 + dy, (240, 170, 35), "")
        draw_beam(d, x0 + c * dx - 55, y0 + 3 * dy, x0 + c * dx + 55, y0 + 3 * dy, (240, 170, 35), "")
    for r in [0, 1, 3, 4]:
        draw_beam(d, x0 + 1 * dx, y0 + r * dy, x0 + 4 * dx, y0 + r * dy, (210, 65, 65), "")
    d.text((80, 455), "Maximo nodo: 243.75 kg < 400 kg", fill=(35, 110, 55), font=font(18))
    add_legend(d, 610, 365)
    im.save(path)


def scheme_ex2(path):
    im = Image.new("RGB", (900, 560), "white")
    d = ImageDraw.Draw(im)
    d.text((30, 25), "P.1.2 - Reparto en 16 nodos con carga excentrica", fill=(20, 20, 20), font=font(24))
    x0, y0, dx, dy = 110, 105, 155, 78
    draw_grid(d, x0, y0, 5, 6, dx, dy)
    draw_arrow_down(d, x0 + 2.8 * dx, y0 + 2.4 * dy, "Q=3800")
    draw_beam(d, x0 + 2 * dx, y0 + 2.4 * dy, x0 + 4 * dx, y0 + 2.4 * dy, (35, 130, 210), "N4")
    for c in [2, 4]:
        draw_beam(d, x0 + c * dx, y0 + 1 * dy, x0 + c * dx, y0 + 4 * dy, (45, 155, 90), "N3")
    for r in [1, 2, 3, 4]:
        draw_beam(d, x0 + 1 * dx, y0 + r * dy, x0 + 2 * dx, y0 + r * dy, (240, 170, 35), "")
        draw_beam(d, x0 + 3 * dx, y0 + r * dy, x0 + 4 * dx, y0 + r * dy, (240, 170, 35), "")
    for r in [1, 2, 3, 4]:
        draw_beam(d, x0 + 1 * dx - 45, y0 + r * dy, x0 + 1 * dx + 45, y0 + r * dy, (210, 65, 65), "")
        draw_beam(d, x0 + 4 * dx - 45, y0 + r * dy, x0 + 4 * dx + 45, y0 + r * dy, (210, 65, 65), "")
    d.text((80, 500), "Maximo nodo: 350.31 kg < 360 kg. Cumple.", fill=(35, 110, 55), font=font(18))
    add_legend(d, 610, 385)
    im.save(path)


def scheme_ex3(path):
    im = Image.new("RGB", (900, 590), "white")
    d = ImageDraw.Draw(im)
    d.text((30, 25), "P.1.3 - Reparto no uniforme para compensar excentricidad", fill=(20, 20, 20), font=font(23))
    x0, y0, dx, dy = 105, 105, 155, 82
    draw_grid(d, x0, y0, 5, 5, dx, dy)
    draw_arrow_down(d, x0 + 1.45 * dx, y0 + 0.8 * dy, "Q=2660")
    draw_beam(d, x0 + 1 * dx, y0 + 0.8 * dy, x0 + 2 * dx, y0 + 0.8 * dy, (35, 130, 210), "N4")
    draw_beam(d, x0 + 1 * dx, y0 + 0 * dy, x0 + 1 * dx, y0 + 2 * dy, (45, 155, 90), "A")
    draw_beam(d, x0 + 2 * dx, y0 + 0 * dy, x0 + 2 * dx, y0 + 2 * dy, (45, 155, 90), "B")
    draw_beam(d, x0 + 0 * dx, y0 + 0 * dy, x0 + 3 * dx, y0 + 0 * dy, (240, 170, 35), "8 nodos")
    draw_beam(d, x0 + 1 * dx, y0 + 2 * dy, x0 + 2 * dx, y0 + 2 * dy, (240, 170, 35), "2 nodos")
    draw_beam(d, x0 + 2 * dx, y0 + 0 * dy, x0 + 4 * dx, y0 + 0 * dy, (210, 65, 65), "4 nodos")
    draw_beam(d, x0 + 2 * dx, y0 + 2 * dy, x0 + 3 * dx, y0 + 2 * dy, (210, 65, 65), "2 nodos")
    d.text((55, 450), "Ramal A superior: 1191.68 kg / 8 = 148.96 kg/nodo", fill=(40, 40, 40), font=font(17))
    d.text((55, 477), "Ramal B superior: 936.32 kg / 4 = 234.08 kg/nodo", fill=(40, 40, 40), font=font(17))
    d.text((55, 504), "Maximo nodo: 234.08 kg < 286.67 kg. Cumple.", fill=(35, 110, 55), font=font(18))
    add_legend(d, 610, 420)
    im.save(path)


def scheme_ex4(path):
    im = Image.new("RGB", (900, 570), "white")
    d = ImageDraw.Draw(im)
    d.text((30, 25), "P.1.4 - Sistema unico para Q1 y Q2", fill=(20, 20, 20), font=font(24))
    x0, y0, dx, dy = 100, 105, 155, 78
    draw_grid(d, x0, y0, 5, 6, dx, dy)
    draw_arrow_down(d, x0 + 1.2 * dx, y0 + 1.8 * dy, "Q1=1200")
    draw_arrow_down(d, x0 + 3.3 * dx, y0 + 1.8 * dy, "Q2=1800")
    draw_beam(d, x0 + 0.8 * dx, y0 + 1.8 * dy, x0 + 4.0 * dx, y0 + 1.8 * dy, (35, 130, 210), "N4")
    for c in [1, 4]:
        draw_beam(d, x0 + c * dx, y0 + 1 * dy, x0 + c * dx, y0 + 4 * dy, (45, 155, 90), "N3")
    for r in [1, 2, 3, 4]:
        draw_beam(d, x0 + 0.5 * dx, y0 + r * dy, x0 + 1.5 * dx, y0 + r * dy, (240, 170, 35), "")
        draw_beam(d, x0 + 3.5 * dx, y0 + r * dy, x0 + 4.5 * dx, y0 + r * dy, (240, 170, 35), "")
    for r in [1, 2, 3, 4]:
        draw_beam(d, x0 + 0.5 * dx, y0 + r * dy, x0 + 1.5 * dx, y0 + r * dy, (210, 65, 65), "")
        draw_beam(d, x0 + 3.5 * dx, y0 + r * dy, x0 + 4.5 * dx, y0 + r * dy, (210, 65, 65), "")
    d.text((80, 505), "Maximo nodo: 218.75 kg < 286.67 kg. Cumple.", fill=(35, 110, 55), font=font(18))
    add_legend(d, 610, 395)
    im.save(path)


def scheme_ex5(path):
    im = Image.new("RGB", (900, 560), "white")
    d = ImageDraw.Draw(im)
    d.text((30, 25), "P.1.5 - Verificacion de imposibilidad sin refuerzo", fill=(20, 20, 20), font=font(24))
    x0, y0, dx, dy = 110, 100, 135, 68
    draw_grid(d, x0, y0, 5, 6, dx, dy)
    draw_arrow_down(d, x0 + 1.35 * dx, y0 + 0 * dy, "Q=2400")
    forbidden = [(0, 0), (1, 0), (2, 0), (2, 4), (3, 4), (4, 4), (0, 5), (2, 5)]
    for c, r in forbidden:
        x = x0 + c * dx
        y = y0 + r * dy
        d.line((x - 18, y - 18, x + 18, y + 18), fill=(200, 0, 0), width=6)
        d.line((x - 18, y + 18, x + 18, y - 18), fill=(200, 0, 0), width=6)
    d.rectangle((545, 150, 835, 315), outline=(210, 65, 65), width=4)
    d.text((568, 175), "NO VIABLE", fill=(190, 40, 40), font=font(30))
    d.text((568, 220), "22 nodos disponibles", fill=(40, 40, 40), font=font(17))
    d.text((568, 250), "Capacidad total: 880 kg", fill=(40, 40, 40), font=font(17))
    d.text((568, 280), "Q requerida: 2400 kg", fill=(40, 40, 40), font=font(17))
    d.text((75, 500), "Debe resolverse con refuerzo de cabreadas, mayor capacidad nodal o estructura auxiliar.", fill=(40, 40, 40), font=font(17))
    im.save(path)


def make_assets():
    paths = {}
    for name, fn in [
        ("ex1", scheme_ex1),
        ("ex2", scheme_ex2),
        ("ex3", scheme_ex3),
        ("ex4", scheme_ex4),
        ("ex5", scheme_ex5),
    ]:
        p = ASSET_DIR / f"{name}.png"
        fn(p)
        paths[name] = p
    return paths


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=8) for item in items],
        bulletType="bullet",
        leftIndent=16,
    )


def table(data, col_widths=None, font_size=8.5):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12355B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B9C2CC")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5C6670"))
    canvas.drawString(1.5 * cm, 1.0 * cm, "TP2 Edificios Industriales - Grupo 5 - Version corregida")
    canvas.drawRightString(A4[0] - 1.5 * cm, 1.0 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build_pdf():
    assets = make_assets()
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#12355B"),
            spaceAfter=16,
        )
    )
    styles.add(
        ParagraphStyle(
            "H1x",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#12355B"),
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "H2x",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=15,
            textColor=colors.HexColor("#1F2933"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "BodyX",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=12.5,
            spaceAfter=5,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            "SmallX",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "BoxX",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.3,
            leading=12,
            textColor=colors.HexColor("#0B6B3A"),
            backColor=colors.HexColor("#EAF7EF"),
            borderColor=colors.HexColor("#98D6B0"),
            borderWidth=0.7,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=1.4 * cm,
        leftMargin=1.4 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.6 * cm,
    )

    story = []

    # Cover
    story += [
        Spacer(1, 1.2 * cm),
        p("UNIVERSIDAD TECNOLOGICA NACIONAL", styles["CoverTitle"]),
        p("FACULTAD REGIONAL BUENOS AIRES", styles["CoverTitle"]),
        Spacer(1, 0.8 * cm),
        p("Manejo de Materiales y Distribucion de Plantas", styles["H1x"]),
        p("Trabajo Practico Nro. 2", styles["H1x"]),
        p("Estructuras de Plantas - Cabreadas", styles["H1x"]),
        Spacer(1, 0.6 * cm),
        table(
            [
                ["Integrante", "Legajo"],
                ["Greco, Santiago", "1779801"],
                ["De Conto, Franco", "2094277"],
                ["Echague, Ricardo Martin", "2093870"],
                ["Diaz, Maria Belen", "1636571"],
            ],
            [10 * cm, 4 * cm],
            9,
        ),
        Spacer(1, 0.5 * cm),
        table(
            [
                ["Curso", "Anio", "Grupo", "Ciclo lectivo"],
                ["I5054", "5to", "5", "2026"],
                ["Profesor", "Ing. Gustavo Grimolizzi", "Ayudante T.P.", "Ing. Pablo Lassave"],
            ],
            [3.6 * cm, 4.0 * cm, 3.6 * cm, 4.0 * cm],
            9,
        ),
        Spacer(1, 1.0 * cm),
        p("Version corregida para entrega", styles["BoxX"]),
        PageBreak(),
    ]

    # Intro
    story += [
        p("1. Introduccion y criterio de resolucion", styles["H1x"]),
        p(
            "Se resuelven los casos P.1.1 a P.1.5 para el grupo 5. "
            "No se considera el peso propio de las vigas ni accesorios de anclaje, "
            "segun la consigna. La verificacion principal consiste en comprobar que "
            "la reaccion final sobre cada nodo no supere la capacidad admisible de trabajo.",
            styles["BodyX"],
        ),
        p(
            "Para nodos se adopta: Ctrab = Cmax / coeficiente cuando el coeficiente es mayor que 1. "
            "En P.1.5 el coeficiente informado es 0.10; por ser menor que 1 se interpreta como "
            "disponibilidad residual del nodo, por lo que Ctrab = Cmax x 0.10.",
            styles["BodyX"],
        ),
        p(
            "Para la viga sosten de la carga se calcula Wnec = Mmax x coef_viga / sigma_adm. "
            "Cuando no se informa coeficiente para vigas se toma coef_viga = 1.",
            styles["BodyX"],
        ),
        Spacer(1, 0.2 * cm),
        p("Datos de grupo 5", styles["H2x"]),
        table(
            [
                ["Caso", "Q", "Nodo max", "sigma adm", "Coef nodos", "Coef vigas"],
                ["P.1.1", "3900 kg", "400 kg", "1000 kg/cm2", "-", "-"],
                ["P.1.2", "3800 kg", "450 kg", "1000 kg/cm2", "1.25", "-"],
                ["P.1.3", "2660 kg", "430 kg", "1000 kg/cm2", "1.50", "1.80"],
                ["P.1.4", "Q1=1200 kg; Q2=1800 kg", "430 kg", "1000 kg/cm2", "1.50", "1.50"],
                ["P.1.5", "2400 kg", "400 kg", "1000 kg/cm2", "0.10", "-"],
            ],
            [2.0 * cm, 4.0 * cm, 2.4 * cm, 2.8 * cm, 2.5 * cm, 2.3 * cm],
            8.2,
        ),
        Spacer(1, 0.25 * cm),
        p("Extracto de perfiles usados", styles["H2x"]),
        table(
            [
                ["Perfil", "Wx [cm3]", "Peso [kg/m]", "Uso"],
                ["IPN 180", "161.1", "21.9", "Referencia P.1.5 si se refuerza"],
                ["IPN 240", "354.2", "36.1", "P.1.3"],
                ["IPN 320", "781.9", "60.9", "P.1.1 y P.1.2"],
                ["IPN 340", "923.5", "67.9", "P.1.4"],
            ],
            [3.0 * cm, 3.0 * cm, 3.0 * cm, 6.8 * cm],
            8.5,
        ),
        PageBreak(),
    ]

    # Exercise 1
    story += [
        p("2. Ejercicio 1 - P.1.1", styles["H1x"]),
        RLImage(str(assets["ex1"]), width=16 * cm, height=9.25 * cm),
        p("Datos: Q=3900 kg; nodo maximo=400 kg; sigma admisible=1000 kg/cm2.", styles["BodyX"]),
        table(
            [
                ["Concepto", "Calculo", "Resultado"],
                ["Nodos minimos", "3900 / 400", "9.75 -> se adoptan 16 nodos"],
                ["Nivel 4", "Viga 8 m, carga centrada", "RA=RB=1950 kg"],
                ["Nivel 3", "1950 / 2", "975 kg por apoyo"],
                ["Nivel 2", "975 / 2", "487.50 kg por apoyo"],
                ["Nivel 1", "487.50 / 2", "243.75 kg por nodo"],
                ["Verificacion nodal", "243.75 < 400", "Cumple"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
        ),
        p("Seleccion de perfil de la viga sosten:", styles["H2x"]),
        table(
            [
                ["Magnitud", "Calculo", "Resultado"],
                ["Mmax", "3900 x 800 / 4", "780000 kgcm"],
                ["Wnec", "780000 / 1000", "780 cm3"],
                ["Perfil seleccionado", "Primer Wx >= 780 cm3", "IPN 320 (Wx=781.9 cm3)"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
        ),
        p("Conclusion: el sistema cumple en nodos y el perfil minimo normalizado es IPN 320.", styles["BoxX"]),
        PageBreak(),
    ]

    # Exercise 2
    story += [
        p("3. Ejercicio 2 - P.1.2", styles["H1x"]),
        RLImage(str(assets["ex2"]), width=16 * cm, height=9.95 * cm),
        p(
            "Datos: Q=3800 kg; nodo maximo=450 kg; coeficiente de nodos=1.25; "
            "sigma admisible=1000 kg/cm2.",
            styles["BodyX"],
        ),
        table(
            [
                ["Concepto", "Calculo", "Resultado"],
                ["Capacidad de trabajo", "450 / 1.25", "360 kg/nodo"],
                ["Nodos minimos", "3800 / 360", "10.56 -> se adoptan 16 nodos"],
                ["Nivel 4", "L=8 m; a=5 m; b=3 m", "RA=1425 kg; RB=2375 kg"],
                ["Nivel 3 - ramal A", "1425 x 2.95 / 5", "840.75 kg y 584.25 kg"],
                ["Nivel 3 - ramal B", "2375 x 2.95 / 5", "1401.25 kg y 973.75 kg"],
                ["Nivel 2", "Cada reaccion / 2", "292.125; 420.375; 486.875; 700.625 kg"],
                ["Nivel 1", "Cada reaccion / 2", "Maximo nodo=350.3125 kg"],
                ["Verificacion nodal", "350.3125 < 360", "Cumple"],
            ],
            [4.3 * cm, 6.7 * cm, 5.2 * cm],
            8.0,
        ),
        p("Seleccion de perfil:", styles["H2x"]),
        table(
            [
                ["Magnitud", "Calculo", "Resultado"],
                ["Mmax", "3800 x 5 x 3 / 8", "7125 kgm = 712500 kgcm"],
                ["Wnec", "712500 / 1000", "712.5 cm3"],
                ["Perfil seleccionado", "Primer Wx >= 712.5 cm3", "IPN 320 (Wx=781.9 cm3)"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
        ),
        p("Conclusion: con el coeficiente correcto de grupo 5, P.1.2 cumple. No se requiere un quinto nivel.", styles["BoxX"]),
        PageBreak(),
    ]

    # Exercise 3
    story += [
        p("4. Ejercicio 3 - P.1.3", styles["H1x"]),
        RLImage(str(assets["ex3"]), width=12.0 * cm, height=7.87 * cm),
        p(
            "Datos: Q=2660 kg; nodo maximo=430 kg; coeficiente de nodos=1.50; "
            "coeficiente de vigas=1.80; sigma admisible=1000 kg/cm2.",
            styles["BodyX"],
        ),
        p(
            "La distribucion uniforme de 8 nodos no cumple. Se adopta una distribucion no uniforme "
            "para compensar la excentricidad del punto de carga: el ramal mas cargado se abre en mas nodos.",
            styles["BodyX"],
        ),
        table(
            [
                ["Concepto", "Calculo", "Resultado"],
                ["Capacidad de trabajo", "430 / 1.50", "286.67 kg/nodo"],
                ["Nodos minimos por carga media", "2660 / 286.67", "9.28 nodos"],
                ["Nivel 4", "L=2.5 m; a=1.1 m; b=1.4 m", "RA=1489.6 kg; RB=1170.4 kg"],
                ["Ramal A superior", "1489.6 x 3.2 / 4", "1191.68 kg"],
                ["Ramal A inferior", "1489.6 x 0.8 / 4", "297.92 kg"],
                ["Ramal B superior", "1170.4 x 3.2 / 4", "936.32 kg"],
                ["Ramal B inferior", "1170.4 x 0.8 / 4", "234.08 kg"],
            ],
            [4.2 * cm, 6.6 * cm, 5.4 * cm],
            8.0,
        ),
        Spacer(1, 0.2 * cm),
        table(
            [
                ["Ramal", "Carga de ramal", "Nodos adoptados", "Carga por nodo"],
                ["A superior", "1191.68 kg", "8", "148.96 kg"],
                ["A inferior", "297.92 kg", "2", "148.96 kg"],
                ["B superior", "936.32 kg", "4", "234.08 kg"],
                ["B inferior", "234.08 kg", "2", "117.04 kg"],
                ["Total", "2660 kg", "16", "Maximo=234.08 kg < 286.67 kg"],
            ],
            [3.4 * cm, 3.7 * cm, 3.7 * cm, 5.4 * cm],
            8.4,
        ),
        p("Seleccion de perfil de la viga sosten:", styles["H2x"]),
        table(
            [
                ["Magnitud", "Calculo", "Resultado"],
                ["Mmax", "1489.6 x 1.1 m", "1638.56 kgm = 163856 kgcm"],
                ["Wnec", "163856 x 1.80 / 1000", "294.94 cm3"],
                ["Perfil seleccionado", "Primer Wx >= 294.94 cm3", "IPN 240 (Wx=354.2 cm3)"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
        ),
        p("Conclusion: el redisenio cumple en nodos y la viga sosten se resuelve con IPN 240.", styles["BoxX"]),
        PageBreak(),
    ]

    # Exercise 4
    story += [
        p("5. Ejercicio 4 - P.1.4", styles["H1x"]),
        RLImage(str(assets["ex4"]), width=16 * cm, height=10.1 * cm),
        p(
            "Datos: Q1=1200 kg; Q2=1800 kg; nodo maximo=430 kg; coeficiente de nodos=1.50; "
            "coeficiente de vigas=1.50; sigma admisible=1000 kg/cm2.",
            styles["BodyX"],
        ),
        table(
            [
                ["Concepto", "Calculo", "Resultado"],
                ["Capacidad de trabajo", "430 / 1.50", "286.67 kg/nodo"],
                ["Nodos minimos", "3000 / 286.67", "10.47 -> se adoptan 16 nodos"],
                ["Nivel 4", "L=12 m; Q1 a 4 m; Q2 a 9 m", "RA=1250 kg; RB=1750 kg"],
                ["Nivel 3", "1250/2 y 1750/2", "625 kg; 875 kg"],
                ["Nivel 2", "625/2 y 875/2", "312.5 kg; 437.5 kg"],
                ["Nivel 1", "312.5/2 y 437.5/2", "156.25 kg; 218.75 kg"],
                ["Verificacion nodal", "218.75 < 286.67", "Cumple"],
            ],
            [4.2 * cm, 6.8 * cm, 5.2 * cm],
            8.2,
        ),
        p("Seleccion de perfil:", styles["H2x"]),
        table(
            [
                ["Magnitud", "Calculo", "Resultado"],
                ["Momento en Q1", "1250 x 400", "500000 kgcm"],
                ["Momento en Q2", "1250 x 900 - 1200 x 500", "525000 kgcm"],
                ["Wnec", "525000 x 1.50 / 1000", "787.5 cm3"],
                ["Perfil seleccionado", "IPN 320 no alcanza; IPN 340 si", "IPN 340 (Wx=923.5 cm3)"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
        ),
        p("Conclusion estructural: el sistema cumple y se selecciona IPN 340.", styles["BoxX"]),
        PageBreak(),
    ]

    story += [
        p("5.1 Evaluacion economica y de desperdicio - P.1.4", styles["H1x"]),
        p(
            "Se adopta IPN 340 en barras comerciales de 12 m. Las longitudes de plano se incrementan 5% "
            "por soldadura, fijacion y preparacion en obra. Precio de referencia adoptado para presupuesto "
            "academico: 2.00 USD/kg. Tipo de cambio adoptado: 1420 ARS/USD.",
            styles["BodyX"],
        ),
        table(
            [
                ["Nivel", "Cantidad", "Longitud plano [m]", "Longitud con 5% [m]", "Subtotal [m]"],
                ["4", "1", "12.00", "12.60", "12.60"],
                ["3", "2", "5.00", "5.25", "10.50"],
                ["2", "4", "4.00", "4.20", "16.80"],
                ["1", "8", "2.50", "2.625", "21.00"],
                ["Total", "-", "58.00", "-", "60.90"],
            ],
            [2.5 * cm, 2.5 * cm, 3.6 * cm, 4.1 * cm, 3.0 * cm],
        ),
        Spacer(1, 0.2 * cm),
        p("Plan de corte propuesto", styles["H2x"]),
        table(
            [
                ["Barra", "Cortes propuestos [m]", "Uso [m]", "Remanente [m]"],
                ["1", "12.00 (tramo N4 principal)", "12.000", "0.000"],
                ["2", "0.60 (complemento N4) + 5.25 + 5.25", "11.100", "0.900"],
                ["3", "4.20 + 4.20 + 2.625", "11.025", "0.975"],
                ["4", "4.20 + 4.20 + 2.625", "11.025", "0.975"],
                ["5", "2.625 + 2.625 + 2.625 + 2.625", "10.500", "1.500"],
                ["6", "2.625 + 2.625", "5.250", "6.750"],
                ["Total", "-", "60.900", "11.100"],
            ],
            [2.2 * cm, 8.5 * cm, 2.7 * cm, 2.8 * cm],
            8.0,
        ),
        p(
            "El tramo de 12.60 m se resuelve con una unica union soldada (12.00 m + 0.60 m), "
            "cumpliendo la restriccion de no mas de una union por tramo.",
            styles["BodyX"],
        ),
        Spacer(1, 0.2 * cm),
        table(
            [
                ["Item", "Calculo", "Resultado"],
                ["Material instalado", "60.90 m x 67.9 kg/m", "4135.11 kg"],
                ["Material comprado", "72.00 m x 67.9 kg/m", "4888.80 kg"],
                ["Desperdicio", "11.10 m x 67.9 kg/m", "753.69 kg"],
                ["Desperdicio porcentual", "11.10 / 72.00", "15.42%"],
                ["Costo material comprado", "4888.80 kg x 2.00 USD/kg", "9777.60 USD"],
                ["Costo desperdicio", "753.69 kg x 2.00 USD/kg", "1507.38 USD"],
                ["Mano de obra", "70 h x 35 USD/h", "2450.00 USD"],
                ["Costo total", "9777.60 + 2450.00", "12227.60 USD"],
                ["Costo total en ARS", "12227.60 x 1420", "17363192 ARS"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
            8.2,
        ),
        p("Conclusion economica: presupuesto estimado del sistema P.1.4 = 12227.60 USD, equivalente a 17363192 ARS.", styles["BoxX"]),
        PageBreak(),
    ]

    # Exercise 5
    story += [
        p("6. Ejercicio 5 - P.1.5", styles["H1x"]),
        RLImage(str(assets["ex5"]), width=11.2 * cm, height=6.97 * cm),
        p(
            "Datos: Q=2400 kg; nodo maximo=400 kg; coeficiente de nodos=0.10; "
            "sigma admisible=1000 kg/cm2. Nodos no utilizables: N1 a N3, N23 a N25, N26 y N28.",
            styles["BodyX"],
        ),
        table(
            [
                ["Concepto", "Calculo", "Resultado"],
                ["Capacidad residual por nodo", "400 x 0.10", "40 kg/nodo"],
                ["Nodos teoricos necesarios", "2400 / 40", "60 nodos"],
                ["Nodos del plano", "5 columnas x 6 filas", "30 nodos"],
                ["Nodos prohibidos", "N1, N2, N3, N23, N24, N25, N26, N28", "8 nodos"],
                ["Nodos disponibles", "30 - 8", "22 nodos"],
                ["Capacidad total disponible", "22 x 40", "880 kg"],
                ["Verificacion", "880 < 2400", "No cumple"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
            8.2,
        ),
        p(
            "Resultado: no es admisible colgar la carga Q=2400 kg con los nodos disponibles y sin modificar "
            "la capacidad resistente de la estructura. La solucion tecnica es reforzar cabreadas/nodos, "
            "incorporar una estructura auxiliar independiente o relocalizar el anclaje hacia una zona con "
            "capacidad residual suficiente.",
            styles["BodyX"],
        ),
        p("Resolucion adoptada para el caso", styles["H2x"]),
        table(
            [
                ["Paso", "Criterio tecnico", "Decision"],
                [
                    "1",
                    "Nodos agotados y Ctrab=40 kg.",
                    "No usar anclaje directo.",
                ],
                [
                    "2",
                    "880 kg disponibles < 2400 kg requeridos.",
                    "La VRC no alcanza.",
                ],
                [
                    "3",
                    "No se modifican coeficientes.",
                    "Refuerzo o estructura auxiliar.",
                ],
                [
                    "4",
                    "Luego del refuerzo.",
                    "Recalcular e instalar.",
                ],
            ],
            [1.6 * cm, 7.5 * cm, 7.1 * cm],
            7.8,
        ),
        p("Perfil de referencia para la viga sosten, condicionado al refuerzo", styles["H2x"]),
        table(
            [
                ["Magnitud", "Calculo", "Resultado"],
                ["Mmax", "2400 x 1.0 x 1.5 / 2.5", "1440 kgm = 144000 kgcm"],
                ["Wnec", "144000 / 1000", "144 cm3"],
                ["Perfil minimo", "Primer Wx >= 144 cm3", "IPN 180 (Wx=161.1 cm3)"],
            ],
            [4.2 * cm, 7.0 * cm, 5.0 * cm],
        ),
        p(
            "El IPN 180 solo corresponde a la viga sosten si previamente se resuelve el refuerzo estructural. "
            "No habilita por si mismo el uso de los nodos existentes. Por lo tanto, P.1.5 queda resuelto como "
            "caso no factible con la estructura disponible y requiere refuerzo previo.",
            styles["BoxX"],
        ),
        PageBreak(),
    ]

    # Summary
    story += [
        p("7. Resumen final de verificacion", styles["H1x"]),
        table(
            [
                ["Ejercicio", "Nodos / criterio", "Max nodo", "Capacidad admisible", "Perfil", "Estado"],
                ["P.1.1", "16 nodos", "243.75 kg", "400 kg", "IPN 320", "Cumple"],
                ["P.1.2", "16 nodos", "350.31 kg", "360 kg", "IPN 320", "Cumple"],
                ["P.1.3", "16 nodos no uniformes", "234.08 kg", "286.67 kg", "IPN 240", "Cumple"],
                ["P.1.4", "16 nodos", "218.75 kg", "286.67 kg", "IPN 340", "Cumple"],
                ["P.1.5", "22 disponibles < 60 requeridos", "No aplica", "40 kg", "IPN 180 ref.", "No viable sin refuerzo"],
            ],
            [2.1 * cm, 4.1 * cm, 2.5 * cm, 3.2 * cm, 2.3 * cm, 3.1 * cm],
            7.8,
        ),
        Spacer(1, 0.4 * cm),
        p(
            "Se concluye que los ejercicios P.1.1 a P.1.4 pueden resolverse con los perfiles indicados y "
            "cumpliendo la capacidad nodal. El caso P.1.5, por los nodos anulados y la baja capacidad residual, "
            "requiere una intervencion estructural previa; no debe ejecutarse solamente con vigas de reparticion.",
            styles["BoxX"],
        ),
    ]

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    return OUT


if __name__ == "__main__":
    print(build_pdf())
