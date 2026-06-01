# CLAUDE.md

Proyecto de documento académico (perfil de tesis) en LaTeX sobre la plataforma web del Desafío Bebras en Bolivia.

## Reglas de trabajo

- **No incluir código en el documento.** Al describir la programación o implementación, explicar con texto, tablas o diagramas; nunca pegar fragmentos de código fuente en los `.tex`.
- **No usar emojis.** Ni en el documento ni en las respuestas del chat.
- **Idioma: español.** Todo el contenido del documento va en español.

## Compilación

- Para compilar o recompilar, ejecutar el script `compilar.ps1` desde la raíz:
  ```powershell
  .\compilar.ps1
  ```
- El script usa `latexmk` (pdflatex + biber) y deja **solo** el PDF `Perfil-Bebras.pdf` en la raíz.
- Los archivos auxiliares (`.aux`, `.log`, `.bbl`, etc.) van a la carpeta `build/`.
- No invocar `pdflatex`/`latexmk` manualmente; usar siempre `compilar.ps1`.

## Estructura del documento

- Archivo principal: `main.tex` (clase `report`, `biblatex` estilo APA con backend `biber`).
- Bibliografía: `referencias.bib`.
- Capítulos en `content/`:
  - `01_introduccion.tex` — Introducción (antecedentes, descripción del problema, objetivos)
  - `02_marco_conceptual.tex` — Marco conceptual
  - `03_metologia.tex` — Metodología y marco tecnológico
  - `04_modulo_cms.tex` — Módulo de gestión de contenido (CMS)
  - `05_modulo_competencias.tex` — Módulo de competencias y tareas
  - `06_modulo_participantes.tex` — Módulo de participantes
  - `07_modulo_evaluacion.tex` — Módulo de evaluación
  - `08_integracion_despliegue.tex` — Integración, despliegue y pruebas
  - `09_conclusiones.tex` — Conclusiones y recomendaciones
- La carpeta `ultimo-avance/` contiene una versión/propuesta anterior del documento (referencia, no es la versión final).

## Notas del proyecto

- Es el **documento final de grado** (adscripción para Licenciatura en Ing. Informática, UMSS), no un perfil. Equipo de **dos personas**.
- Metodología XP con **iteraciones fijas de 2 semanas**; cada módulo ocupa 2 iteraciones (8 en total).
- Cuatro módulos: CMS, competencias y tareas, participantes, evaluación digital e imprimible. El desarrollo se documenta por módulo, con las fases de XP dentro de cada uno.
- Pila: Astro, Bun, Express, Prisma, MariaDB, Docker.
- `ultimo-avance/` tiene secciones (justificación, alcances y límites) que podrían reincorporarse al documento actual.
