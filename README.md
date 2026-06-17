# Sistema de Gestión de Operaciones Navieras y Recursos Portuarios

Este repositorio contiene una plataforma web monolítica avanzada diseñada para la automatización, control y sincronización de operaciones portuarias y logística marítima. Desarrollado con **Python** y **Django**, el sistema permite coordinar el ciclo de vida de los buques en puerto, administrar las escalas de los navíos y optimizar la asignación de recursos operativos esenciales en los muelles.

La aplicación adopta una arquitectura modular de múltiples aplicaciones integradas, implementando flujos de validación basados en señales de Django, control de perfiles y filtros dinámicos de renderizado del lado del servidor.

---

## 🚀 Características Principales

### 🚢 Aplicación: Gestor de Navíos (`GestorNavios`)
* **Control de Flota:** Módulo CRUD para la creación, edición y catalogación de buques, gestionando variables críticas como bandera, dimensiones y estados operativos (`gestionarNavios.html`).
* **Planificación de Escalas Marítimas:** Control cronológico de arribos, atraques y zarpes de navíos, asociando de forma estricta cada buque a puertos específicos (`listarEscalas.html`).
* **Seguimiento Automatizado:** Clasificación inteligente de itinerarios segmentados operativamente en vistas dedicadas para escalas con y sin recursos asignados.

### 🏗️ Aplicación: Gestor de Recursos (`GestorRecursos`)
* **Catálogo de Recursos Portuarios:** Administración y alta de equipamiento, personal y servicios según tipologías, subtipos y puertos específicos disponibles (`crear-recurso.html`).
* **Asignación Dinámica de Logística:** Interfaz interactiva asistida por JavaScript (`gestionarRecursos.js`) para vincular maquinaria y recursos portuarios directamente a las escalas activas de los navíos.
* **Flujos de Registro y Perfiles:** Sistema completo de registro de usuarios operativos, tableros de control analíticos (`dashboard.html`) y edición de perfiles específicos.

### 🛡️ Componentes Técnicos Avanzados
* **Automatización mediante Signals:** Uso de señales nativas de Django (`signals.py`) para desencadenar acciones en cadena y auditorías cuando ocurren modificaciones en los estados de los navíos o escalas.
* **Filtros Personalizados (Template Tags):** Procesamiento de cadenas, formateo de fechas de arribo y lógica de negocio en la capa de presentación mediante etiquetas personalizadas (`custom_filters.py`).
* **Manejo de Errores Globales:** Vistas personalizadas listas para producción para gestionar fallos comunes de red o navegación (`404.html` y `500.html`).

---

## 🛠️ Stack Tecnológico

* **Core Backend:** Python 3 + Django Web Framework.
* **Arquitectura:** Modelo-Vista-Template (MVT) distribuido en multi-apps.
* **Persistencia:** PostgreSQL / SQLite (Esquema relacional con llaves foráneas encadenadas para Buques ↔ Escalas ↔ Recursos).
* **Frontend Interno:** HTML5, CSS3 estructurado y modularizado por módulos de negocio, JavaScript Vanilla para la manipulación asíncrona del DOM en muelles.

---

## 📂 Estructura del Repositorio

El proyecto organiza su lógica de negocio separando las responsabilidades operativas en dos aplicaciones independientes orquestadas por el núcleo del proyecto:

```text
bdiazzz-sistema-naviero/
├── requirements.txt                 # Dependencias del proyecto
├── .hgignore                        # Archivo de exclusión para control de versiones Mercurial
│
└── NaviApplication/                 # Directorio Raíz del Proyecto Django
    ├── manage.py                    # Ejecutable de comandos de Django
    │
    ├── NaviApplication/             # Configuración Core del Proyecto
    │   ├── settings.py              # Configuraciones globales, apps registradas y static paths
    │   └── urls.py                  # Enrutador de URL global (incluye rutas de apps)
    │
    ├── GestorNavios/                # Aplicación: Control de Buques e Itinerarios
    │   ├── models.py                # Modelos de Navío, Escala, Puerto y Asignación de Recursos
    │   ├── signals.py               # Automatización de estados y disparadores de datos
    │   ├── views.py / urls.py       # Controladores y enrutamiento de flujos de navegación
    │   ├── templates/               # Vistas HTML de control de escalas y navíos
    │   ├── templatetags/            # Filtros personalizados (custom_filters.py)
    │   └── static/                  # Hojas de estilo locales para maquetación naviera
    │
    ├── GestorRecursos/              # Aplicación: Administración de Recursos en Puerto
    │   ├── choices.py               # Enums y opciones estáticas para tipos y subtipos de recursos
    │   ├── models.py / forms.py     # Modelado de recursos portuarios y validaciones de formularios
    │   ├── views.py / templates/    # Lógica de asignación a muelles y Dashboard operativo
    │   └── static/                  # CSS locales (dashboard.css, crear-recurso.css)
    │
    └── staticfiles/                 # Directorio de Producción (Compilado final)
        └── [recursos_estáticos]     # Archivos consolidados tras ejecutar collectstatic (incluye Django Admin)
