// =====================================================================
// Modelo C4 (Contexto y Contenedores) - Sistema Bebras Bolivia
// Structurizr DSL. Contiene AMBAS vistas (C1 y C2).
// Colores: paleta oficial del modelo C4
//   Person #08427b | Software System #1168bd | Container #438dd5
//
// Render: docker run -it --rm -p 8080:8080 \
//   -v "C:/Users/markv/OneDrive/Escritorio/Proyectos/bebras/bebras-doc/diagramas":/usr/local/structurizr \
//   structurizr/lite   (renombra a workspace.dsl o usa structurizr-cli)
// =====================================================================

workspace "Sistema Bebras Bolivia" "Modelo C4 (contexto y contenedores) del Sistema Bebras Bolivia." {

    model {
        // ---- Actores ----
        admin      = person "Administrador u organizador" "Administra el contenido del sitio y gestiona el concurso."
        maestro    = person "Maestro" "Registra grupos y consulta informacion y resultados."
        estudiante = person "Estudiante" "Consulta informacion y rinde la competencia."

        // ---- Sistema ----
        sistema = softwareSystem "Sistema Bebras Bolivia" "Sistema web del Desafio Bebras en Bolivia. Servido mediante el servidor web Apache." {

            cms = container "CMS (panel de administracion)" "Permite al administrador editar y publicar el contenido del sitio informativo." "Astro + React"

            cmsDb = container "Base de datos del CMS" "Guarda usuarios del CMS, publicaciones y respaldos." "SQLite" {
                tags "Base de datos"
            }

            contentStore = container "Content Store" "Archivos JSON y Markdown del contenido; fuente que consume el build del sitio." "Filesystem (JSON + Markdown)" {
                tags "Almacen"
            }

            sitio = container "Sitio informativo" "Sitio publico estatico (SSG) con la informacion del desafio." "Astro + React"

            frontend = container "Frontend del concurso" "Interfaz del concurso para los usuarios." "Astro + React"

            backend = container "Backend del concurso" "Expone la API y la logica del concurso." "Express + TypeScript"

            contestDb = container "Base de datos del concurso" "Guarda competencias, participantes, examenes y resultados." "MariaDB" {
                tags "Base de datos"
            }
        }

        // ---- Relaciones: contenido / sitio ----
        admin        -> cms          "Administra el contenido"
        cms          -> cmsDb        "Lee y escribe" "SQLite"
        cms          -> contentStore "Escribe el contenido" "JSON/Markdown"
        contentStore -> sitio        "Fuente del build (SSG)"
        maestro      -> sitio        "Consulta informacion" "HTTPS"
        estudiante   -> sitio        "Consulta informacion" "HTTPS"

        // ---- Relaciones: concurso (los tres actores) ----
        admin      -> frontend "Accede al concurso" "HTTPS"
        maestro    -> frontend "Accede al concurso" "HTTPS"
        estudiante -> frontend "Accede al concurso" "HTTPS"
        frontend   -> backend  "Consume la API" "REST/JSON"
        backend    -> contestDb "Lee y escribe" "Prisma"
    }

    views {
        systemContext sistema "C1_Contexto" "Diagrama de contexto del Sistema Bebras Bolivia" {
            include *
            autolayout lr 150 100
        }

        container sistema "C2_Contenedores" "Diagrama de contenedores del Sistema Bebras Bolivia" {
            include *
            autolayout lr 150 100
        }

        // ---- Estilos: paleta oficial del modelo C4 ----
        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
                fontSize 22
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Base de datos" {
                shape Cylinder
            }
            element "Almacen" {
                shape Folder
            }
            relationship "Relationship" {
                dashed true
                thickness 2
                color #707070
            }
        }
    }
}
