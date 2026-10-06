import glob
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
TARJETAS = [4, 16, 20, 33, 50, 66, 70, 74]

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
        rf"\caption{{{caption}}}\label{{{label}}}\\",
        r"\arrayrulecolor{huazul}\specialrule{1.4pt}{0pt}{0pt}",
        r"\rowcolor{hufondo}" + head,
        r"\arrayrulecolor{hulinea}\midrule",
        r"\endfirsthead",
        r"\arrayrulecolor{huazul}\specialrule{1.4pt}{0pt}{0pt}",
        r"\rowcolor{hufondo}" + head,
        r"\arrayrulecolor{hulinea}\midrule",
        r"\endhead",
        *rows,
        r"\arrayrulecolor{hulinea}\midrule",
        rf"\multicolumn{{4}}{{r}}{{\textbf{{Total de puntos}}}} & \textbf{{{total}}}" + fin,
        r"\arrayrulecolor{hulinea}\bottomrule",
        r"\end{longtable}",
        r"\arrayrulecolor{black}",
    ]) + "\n"


for f in glob.glob(T + "tarjeta_*.tex"):
    os.remove(f)
for nombre, hus in grupos:
    archivo, caption, label, version = GRUPOS[nombre]
    io.open(T + archivo + ".tex", "w", encoding="utf-8").write(table(hus, caption, label, version))
    print(f"{nombre}: {hus[0]['id']} a {hus[-1]['id']}, {sum(int(h['esf']) for h in hus)} puntos")
for n in TARJETAS:
    io.open(T + f"tarjeta_hu_{n}.tex", "w", encoding="utf-8").write(card(hus_por_n[n]) + "\n")

TITULO = "ANEXO A. HISTORIAS DE USUARIO"
anexo = [rf"\chapter*{{{TITULO}}}", rf"\addcontentsline{{toc}}{{chapter}}{{{TITULO}}}", "",
         "Tarjetas completas de las historias de usuario de la plataforma, con sus criterios de aceptación. Están numeradas en el orden en que aparecen en el documento.", "",
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
