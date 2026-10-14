import io
import os
import re

BASE = "C:/Users/markv/OneDrive/Escritorio/Proyectos/bebras/"
DOC = BASE + "bebras-doc/"
T = DOC + "content/tablas/"

md = io.open(BASE + "_historias.md", encoding="utf-8").read()

# Módulo -> (archivo de la tabla, título de la tabla, etiqueta, columna de versión)
GRUPOS = {
    "Módulo de gestión de contenido": ("hus_cap5", "Historias de usuario del módulo de gestión de contenido", "tab:historias_cms", True),
    "Módulo de gestión de desafíos": ("hus_cap6", "Historias de usuario del módulo de gestión de desafíos", "tab:historias_desafios", False),
    "Módulo de registro y administración de participantes": ("hus_cap7", "Historias de usuario del módulo de registro y administración de participantes", "tab:historias_participantes", False),
    "Módulo de evaluación": ("hus_cap8", "Historias de usuario del módulo de evaluación", "tab:historias_evaluacion", False),
    "Integración entre el CMS y el Desafío": ("hus_integracion", "Historias de usuario de la integración entre el CMS y el Desafío", "tab:historias_integracion", True),
}

grupos = []
for block in re.split(r"^## ", md, flags=re.M)[1:]:
    nombre = block.splitlines()[0].strip()
    if nombre not in GRUPOS:
        continue
    hus = []
    for s in re.split(r"^### ", block, flags=re.M)[1:]:
        head = s.splitlines()[0]
        num, title = re.match(r"HU-(\d+) – (.+)", head).groups()
        meta = re.search(r"Prioridad: (\d) · Esfuerzo: (\d+) · Versión: (\d)", s)
        como = re.search(r"Como ([^,\n]+),\s*\nquiero (.+?),\s*\npara (.+?)\.\s*\n", s, re.S)
        hus.append(dict(n=int(num), id=f"HU-{num}", title=title.strip(), prio=meta[1], esf=meta[2], ver=meta[3],
                        role=como[1].strip(), quiero=como[2].strip().replace("\n", " "),
                        para=como[3].strip().replace("\n", " "), crits=re.findall(r"^\* (.+)$", s, re.M)))
    grupos.append((nombre, hus))

todas = [h for _, hus in grupos for h in hus]
assert [h["n"] for h in todas] == list(range(1, len(todas) + 1)), "la numeración debe ir de 1 a n sin saltos"
assert all(h["crits"] for h in todas)
primera_persona = re.compile(r"\b(puedo|subo|escribo|elijo|veo|marco|indico|agrego|selecciono|descargo|busco|edito|pego|creo|genero|ordeno|entro|me|mi|mis)\b", re.I)
for h in todas:
    for c in h["crits"]:
        assert not primera_persona.search(re.sub(r"«[^»]*»", "", c)), (h["id"], c)
hus_por_n = {h["n"]: h for h in todas}


def tex(t):
    t = t.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")
    return t.replace("\u2212", "$-$").replace("→", r"$\rightarrow$")


def user(role):
    return role.split()[0].capitalize()


def card(h):
    desc = rf"\textbf{{Como}} {tex(h['role'])}, \textbf{{quiero}} {tex(h['quiero'])}, \textbf{{para}} {tex(h['para'])}."
    out = [rf"\begin{{historia}}[{h['ver']}]{{{h['id']}}}{{{tex(h['title'])}}}{{{user(h['role'])}}}{{{h['prio']}}}{{{h['esf']}}}{{{desc}}}"]
    out += [rf"\hucriterio{{{tex(c)}}}" for c in h["crits"]]
    out.append(r"\end{historia}")
    return "\n".join(out)


def table(hus, caption, label, version):
    if version:
        cols = r"l >{\raggedright\arraybackslash}p{6.4cm} >{\raggedright\arraybackslash}p{2.3cm} c c c"
        head = r"\textbf{ID} & \textbf{Historia} & \textbf{Usuario} & \textbf{Prior.} & \textbf{Esf.} & \textbf{Versión} \\"
        rows = [rf"{h['id']} & {tex(h['title'])} & {user(h['role'])} & {h['prio']} & {h['esf']} & {h['ver']} \\" for h in hus]
        fin = " & \\\\"
    else:
        cols = r"l >{\raggedright\arraybackslash}p{6.9cm} >{\raggedright\arraybackslash}p{2.4cm} c c"
        head = r"\textbf{ID} & \textbf{Historia} & \textbf{Usuario} & \textbf{Prioridad} & \textbf{Esfuerzo} \\"
        rows = [rf"{h['id']} & {tex(h['title'])} & {user(h['role'])} & {h['prio']} & {h['esf']} \\" for h in hus]
        fin = " \\\\"
    total = sum(int(h["esf"]) for h in hus)
    return "\n".join([
        rf"\begin{{longtable}}{{{cols}}}",
        r"\arrayrulecolor{huazul}\specialrule{1.4pt}{0pt}{0pt}",
        r"\rowcolor{hufondo}" + head,
        r"\arrayrulecolor{hulinea}\midrule",
        r"\endhead",
        *rows,
        r"\arrayrulecolor{hulinea}\midrule",
        rf"\multicolumn{{4}}{{r}}{{\textbf{{Total de puntos}}}} & \textbf{{{total}}}" + fin,
        r"\arrayrulecolor{hulinea}\bottomrule",
        rf"\rowcolor{{white}}\caption{{{caption}}}\label{{{label}}}\\",
        r"\end{longtable}",
        r"\arrayrulecolor{black}",
    ]) + "\n"


ITERACIONES = {1: (1, 6), 2: (7, 17), 3: (18, 30), 4: (31, 45), 5: (46, 59), 6: (60, 66), 7: (67, 73), 8: (74, 81)}
MODULO_DE = {1: "Gestión de contenido", 2: "Gestión de contenido", 3: "Gestión de desafíos", 4: "Gestión de desafíos",
             5: "Participantes", 6: "Participantes", 7: "Evaluación", 8: "Evaluación"}
ULTIMA = ITERACIONES[8][1]
assert ITERACIONES[1][0] == 1 and all(ITERACIONES[k][1] + 1 == ITERACIONES[k + 1][0] for k in range(1, 8))
assert ULTIMA < len(todas)


def tabla_iteracion(n, hus):
    total = sum(int(h["esf"]) for h in hus)
    rows = [rf"{h['id']} & {tex(h['title'])} & {user(h['role'])} & {h['prio']} & {h['esf']} \\" for h in hus]
    return "\n".join([
        r"\begin{table}[H]",
        r"\estilotabla",
        r"\begin{tabularx}{\linewidth}{l >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}p{2.8cm} c c}",
        r"\arrayrulecolor{huazul}\specialrule{1.4pt}{0pt}{0pt}",
        r"\rowcolor{hufondo}\textbf{ID} & \textbf{Historia} & \textbf{Usuario} & \textbf{Prioridad} & \textbf{Esfuerzo} \\",
        r"\arrayrulecolor{hulinea}\midrule",
        *rows,
        r"\arrayrulecolor{hulinea}\midrule",
        rf"\rowcolor{{white}}\multicolumn{{4}}{{r}}{{\textbf{{Total de puntos}}}} & \textbf{{{total}}} \\",
        r"\arrayrulecolor{hulinea}\bottomrule",
        r"\end{tabularx}",
        r"\arrayrulecolor{black}",
        rf"\caption[Historias de la Iteración {n}]{{Historias de la Iteración {n}}}",
        rf"\label{{tab:hus_iteracion_{n}}}",
        r"\end{table}",
    ]) + "\n"


def resumen(hus):
    return len(hus), sum(int(h["esf"]) for h in hus), sum(h["prio"] == "1" for h in hus), sum(h["prio"] == "2" for h in hus)


def tabla_distribucion():
    filas, total = [], [0, 0, 0, 0]
    entradas = [(f"Iteración {k}", MODULO_DE[k], [hus_por_n[i] for i in range(a, b + 1)]) for k, (a, b) in ITERACIONES.items()]
    entradas.append(("Integración", "Papel y CMS--Desafío", [hus_por_n[i] for i in range(ULTIMA + 1, len(todas) + 1)]))
    for nombre, modulo, hus in entradas:
        valores = resumen(hus)
        total = [t + v for t, v in zip(total, valores)]
        filas.append(rf"{nombre} & {modulo} & " + " & ".join(str(v) for v in valores) + r" \\")
    return "\n".join([
        r"\begin{table}[H]",
        r"\estilotabla",
        r"\begin{tabularx}{\linewidth}{l >{\raggedright\arraybackslash}X c c c c}",
        r"\arrayrulecolor{huazul}\specialrule{1.4pt}{0pt}{0pt}",
        r"\rowcolor{hufondo}\textbf{Iteración} & \textbf{Módulo} & \textbf{Historias} & \textbf{Puntos} & \textbf{Prioridad 1} & \textbf{Prioridad 2} \\",
        r"\arrayrulecolor{hulinea}\midrule",
        *filas,
        r"\arrayrulecolor{hulinea}\midrule",
        r"\rowcolor{white}\textbf{Total} & & " + " & ".join(rf"\textbf{{{v}}}" for v in total) + r" \\",
        r"\arrayrulecolor{hulinea}\bottomrule",
        r"\end{tabularx}",
        r"\arrayrulecolor{black}",
        r"\caption[Resumen de historias por iteración]{Resumen de historias, puntos y prioridades por iteración}",
        r"\label{tab:backlog_iteraciones}",
        r"\end{table}",
    ]) + "\n", total


for nombre, hus in grupos:
    archivo, caption, label, version = GRUPOS[nombre]
    io.open(T + archivo + ".tex", "w", encoding="utf-8").write(table(hus, caption, label, version))
    print(f"{nombre}: {hus[0]['id']} a {hus[-1]['id']}, {sum(int(h['esf']) for h in hus)} puntos")
for k, (a, b) in ITERACIONES.items():
    hus = [hus_por_n[i] for i in range(a, b + 1)]
    io.open(T + f"hus_iter_{k}.tex", "w", encoding="utf-8").write(tabla_iteracion(k, hus))
    print(f"Iteración {k}: HU-{a} a HU-{b}, {len(hus)} historias, {sum(int(h['esf']) for h in hus)} puntos")
distribucion, total = tabla_distribucion()
io.open(T + "backlog_iteraciones.tex", "w", encoding="utf-8").write(distribucion)
print("Distribución: historias, puntos, prioridad 1, prioridad 2 =", total)

TITULO = "ANEXO A. HISTORIAS DE USUARIO"
anexo = [rf"\chapter*{{{TITULO}}}", rf"\addcontentsline{{toc}}{{chapter}}{{{TITULO}}}", "",
         io.open(DOC + "scripts/anexo_a_intro.tex", encoding="utf-8").read(),
         r"\tcbset{hucolocacion/.style={nofloat, before skip=10pt, after skip=10pt}}", ""]
for nombre, hus in grupos:
    anexo += [rf"\section*{{{nombre}}}", rf"\addcontentsline{{toc}}{{section}}{{{nombre}}}", ""]
    for h in hus:
        anexo += [card(h), ""]
for out in ["content/", "anexos/"]:  # anexos/ es la carpeta que se compila sola
    io.open(DOC + out + "anexo_a_historias.tex", "w", encoding="utf-8").write("\n".join(anexo))
    viejo = DOC + out + "anexo_b_historias_cms.tex"
    if os.path.exists(viejo):
        os.remove(viejo)
print(len(todas), "historias")
