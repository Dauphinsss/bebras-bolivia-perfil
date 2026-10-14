# CLAUDE.md: bebras-doc

Guía para Claude Code en `bebras-doc/`. Concatena el `AGENTS.md` de esta carpeta (abajo); las reglas generales están en `../CLAUDE.md`.

> Edita siempre en `AGENTS.md` y vuelve a concatenar.

---

# AGENTS.md: bebras-doc

Documento final de grado (adscripción, Licenciatura en Ingeniería Informática, UMSS) e informes de avance. Las reglas generales están en `../AGENTS.md`; aquí va lo propio del documento.

## Datos del trabajo

- Título: **Sistema web para la administración del Desafío Bebras en Bolivia**. Autor único: Velasquez Vela Marcos (el equipo de dos personas terminó con la carta de cambio leve de sept. 2026).
- Tutora: MSc. Blanco Coca Maria Leticia. Supervisor: MSc. Costas Jauregui Vladimir Abel. Docente de la materia: Dra. Romero Rodríguez Patricia Elizabeth.
- **Alineado con los papeles oficiales** (`adscripcion/finales/`: formulario de tema, carta de cambio leve, términos de referencia, convenio): 4 objetivos específicos (A contenido, B desafíos, C participantes, D evaluación) y alcances copiados casi literal de los términos de referencia. **No cambiarlos sin hablar con el usuario.**
- Fechas de referencia: primera edición prevista 13/11/2026 (el sitio dice 16 a 20 de noviembre); validación final 23/10; «sistema desplegado y probado antes de diciembre de 2026»; el trabajo no demanda financiamiento.
- Pila real: Astro, React, Bun, Express, Prisma, SQLite (CMS) y D1 en Cloudflare (concurso). MariaDB y Docker fueron un diseño inicial descartado.

## Reglas de redacción

- Español, **sin código fuente**, sin emojis, tono académico, **menos es más** (frases cortas). Explicar con texto, tablas o diagramas.
- Compilar **siempre** con `.\compilar.ps1` (latexmk + biber; deja solo `Perfil-Bebras.pdf` en la raíz y los auxiliares en `build/`). No llamar a `pdflatex`/`latexmk` a mano.
- **Un solo estilo de tabla** (2026-10-08): `table` con `\estilotabla` (definido en `main.tex`) y `tabularx{\linewidth}` con regla azul, encabezado `hufondo`, filas alternadas, sin líneas verticales ni `\hline`, y el pie (`\caption` y `\label`) **abajo**. Las de HU (generadas) son `longtable` dentro de `{\estilotabla … \input{…}}` con el pie como última fila; no usar `\captionof` (cuenta doble y salta la numeración). No volver a la cuadrícula ni a una línea entre filas.

## Estructura

- Principal: `main.tex` (clase `report`, `biblatex` APA con `biber`, bibliografía `referencias.bib`).
- Capítulos en `content/`: 01 introducción (con `01.1` a `01.4`), 02 marco conceptual, 03 metodología, 04 arquitectura, 05 CMS, 06 competencias, 07 participantes, 08 evaluación, 09 integración y despliegue, 10 conclusiones. Un solo Anexo A con las 91 HU (también en `anexos/` como PDF aparte).
- **Estado del arte (pedido de la tutora, 2026-10-07):** el análisis de las plataformas Bebras de otros países (Francia, Bélgica, Perú, EE. UU., síntesis y su tabla) y «Sistemas de gestión de concursos en línea» van en el cap. 2, sección «Estado del arte». El cap. 3 queda solo con la metodología (XP) y el marco tecnológico: no devolverlos ahí.
- **Generados, no editar a mano:** `content/tablas/*` y `content/anexo_a_historias.tex` (script `scripts/generar_historias.py` desde `../_historias.md`; escribe también en `anexos/`).
- `ultimo-avance/` es una versión anterior (solo referencia). `cronograma-da/` es el cronograma de actividades (aún con los dos autores). `adscripcion/` tiene los trámites.
- **`informe-avance/`**: informe de avance con el formato de la carrera (cabecera con título, postulante, tutor, docente, firmas y fecha; «Descripción de lo avanzado» en **una sola plana**). Se compila con su propio `compilar.ps1` y deja `Informe-Avance.pdf`. Es el **informe Nro. 1** (`\nroinforme`), con entrega el 13/10/2026 (`\fechaentrega`). Para el Nro. 2, contar solo lo avanzado desde el 13/10.

## Historias de usuario (revisión de la tutora, 2026-10-05)

- Una sola lista HU-1 a HU-91 en el orden del documento (sin «3.1» ni «CMS-01»).
- Descripción que baste para entender la historia; criterios **impersonales** («Se registra…», «Es posible…», «El sistema…»), nunca en primera persona (el script lo comprueba); cada criterio del actor de su historia.
- Una HU por tipo de pregunta; la impresión en dos (cuadernillo y hojas de respuestas, HU-82 y HU-83). Títulos en neutro («Crear una cuenta de maestro», no «Crear mi cuenta»). Cada HU grande se parte en vez de agrupar. Fuentes viejas en `../_archivo/historias_v1/`.
- **Tamaño** (pedido de la tutora, 2026-10-08): ni muy genéricas ni muy específicas. Una HU es una necesidad de un solo usuario que se entrega y se prueba sola; si junta dos (calcular y publicar, ver y verificar) se parte. No es «una HU por caso de uso» (registrar una tarea son seis HU, una por tipo). Ese día el cálculo de HU-76 pasó a HU-75 y HU-90 se partió en HU-90 y HU-91.
- Cada iteración lista sus HU en una tabla (`hus_iter_N`, en su subsección de planificación o de historias) y el cap. 3 tiene el resumen por iteración (`backlog_iteraciones`); todas se generan con `generar_historias.py`. El mapa iteración→HU es `ITERACIONES` en el script y **debe coincidir** con las tablas «Plan de entregas» de los caps. 5 a 8 (HU-82 a HU-91 son posteriores y van como «Integración»). La metodología es XP: el cap. 3 aclara que la lista de historias hace de *product backlog* y la de cada iteración de *sprint backlog*; no renombrar con términos de Scrum.
- Tarjetas de HU: entorno `historia` de `main.tex`; viven **solo en el Anexo A** (no flotan). En los caps. 5 a 9 las HU solo se nombran (tabla con ID, título, usuario, prioridad, esfuerzo y versión), sin tarjetas de ejemplo.
- Cómo se elaboran las HU (seis pasos, prioridad, esfuerzo, versión) va en el **cap. 3, subsección «Historias de usuario»**, no en el anexo (pedido de la tutora, 2026-10-08). La entrada del anexo sale de `scripts/anexo_a_intro.tex`, que lee `generar_historias.py`.

## Figuras y diagramas

- Cap. 4: cinco secciones (Descripción general, Contexto, Contenedores, Decisiones, Modelo de datos). **No volver** a agregar «Estructura funcional», «Interacción general» ni «Flujo operativo».
- Diagramas en **PlantUML** (`diagramas/*.puml`, C4-PlantUML + ER en español, blanco y negro). Regenerar: `java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -charset UTF-8 -tpng diagramas/*.puml` con `GRAPHVIZ_DOT` a un `dot.exe` (en 2026-10-08 había uno en `%TEMP%\_graphviz\`; sin `dot`, `!pragma layout smetana` da otro trazado). El usuario rechazó TikZ a mano («usa un verdadero lenguaje»). C2 con `linetype ortho`.
- Los cuatro almacenes de datos van **juntos en el cap. 4, sección «Modelo de datos»** (subsecciones: base del Desafío, archivos R2, base del CMS, Content Store), cada uno con su diagrama y nunca mezclados: `modelo-datos` (D1), `archivos-r2` (documentos de los maestros; el R2 es un solo bucket `UPLOADS`, claves `uuid.ext`, 5 MB, PDF/JPG/PNG, privados), `modelo-datos-cms` (SQLite) y `content-store` (árbol de carpetas en `@startwbs`). El cap. 5 solo remite a ellos, y su tabla de la Iteración 2 no menciona lo posterior (certificados, listado de colegios). El modelo del CMS se contrastó con `cms/src/db/index.ts` y con la base real; el del Desafío, con `schema.prisma`.
- **Sin leyendas ni notas en los diagramas** (pedido del usuario, 2026-10-08): ni «PK: clave primaria…» en los pies de figura ni notas «Único». Las marcas PK/FK/UQ dentro de las cajas se quedan y se definen **una vez en el texto** del cap. 4 (sección 4.5). Los pies de figura son solo el título; lo que explicaban va en el párrafo que presenta la figura, que además la cita con `\ref`.
- **Content Store** = toda la carpeta `cms/content` (JSON, Markdown, imágenes, respaldos y versiones publicadas), igual en el C2 (`c2-contenedores.puml`), el cap. 4 y el cap. 5; las imágenes no son un almacén aparte. Si cambia, cambiarlo en los tres.
- Figuras 2.1 y 3.1: imágenes de Codex en `assets/ia/*-r.png`, **sin texto dentro** (rótulos en LaTeX) y sin mencionar la IA en el pie. No volver a las imágenes viejas con texto inventado.
- Capturas: Playwright 1440×900 contra servidores locales, JPEG 1600 px (`assets/ui/desafio`, `assets/ui/cms`). Ocultar `astro-dev-toolbar`. La vista previa del CMS deja `src/content/blog/cms-preview.md` en `bebras-bolivia`: borrarlo.

## Citas verificadas (no deshacer)

- `porto2024`, `meza2024` (autores corregidos con Crossref); cifras de `bebrasstats2024` (3 936 642 participantes, 70 países; 4 sistemas en papel, respalda los imprimibles); **no usar cifras por país** del PDF (tabla desalineada).
- Grover y Pea no fijan «cuatro componentes»: el trabajo los **adopta**.
- Antes de aplicar una crítica de Codex, verificarla (Crossref, `pdftotext`, API de GitHub).

## Pendiente

1. Revisar con Codex (solo lectura) los caps. 4 a 10 y el Anexo A.
2. Formatos imprimibles: hechos (2026-10-05): HU-82 a HU-84 en el cap. 8 (las de integración pasaron a HU-85 a HU-91), tabla de adaptación al papel con sus 4 pruebas e2e, capturas `papel-*.jpg` y columna `forma_rendicion` del intento en el ER.
3. Despliegue: hecho el 2026-10-06; falta la validación con el supervisor y las pruebas de usabilidad.
4. Cap. 9 y `../bebras-bolivia/_informe_pruebas_cms_sitio.md` dicen accesibilidad 100: con los colores originales restaurados hay que volver a medir.
5. Menores: entradas `bebras`, `bebrascms`, `bebrastaskworkshops`, `bebrasstructure` apuntan a la portada de bebras.org; `\clearpage` del cap. 1; pruebas de usabilidad con usuarios reales.
6. Difusión en redes: pasar `../marketing/REGISTRO.md` al documento cuando el usuario lo pida (no está entre los alcances oficiales: preguntar dónde va).
