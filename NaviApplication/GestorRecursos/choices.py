TIPO_SUBTIPO_MAP = {
    "Herramientas y Equipamiento": [
        "Martillos", "Destornilladores", "Taladros",
        "Llaves", "Alicates", "Amoladoras", "Sierras",
        "Multímetros", "Calibradores", "Medidores de presión"
    ],
    "Materiales de Construcción": [
        "Cemento", "Arena", "Grava"
    ],
    "Equipos de Protección": [
        "Guantes", "Cascos", "Botas", "Gafas de seguridad", "Arnés de seguridad", "Overoles"
    ],
    "Lubricantes y Fluidos": [
        "Aceite motor", "Aceite hidráulico", "Grasas industriales",
        "Líquido refrigerante", "Desengrasantes", "Solventes"
    ],
    "Productos de Limpieza y Sanitización": [
        "Detergentes náuticos", "Limpiadores multiuso", "Desinfectantes",
        "Trapos", "Mopas", "Escobas", "Bolsas de basura"
    ],
    "Suministros de Comida y Cocina": [
        "Frutas", "Verduras", "Carnes", "Arroz", "Pasta", "Enlatados",
        "Agua potable", "Jugos", "Leche", "Refrescos", "Utensilios de cocina", "Gas en cilindros"
    ],
    "Artículos de Alojamiento y Bienestar a Bordo": [
        "Sábanas", "Almohadas", "Papel higiénico",
        "Jabones", "Shampoo", "Cepillos de dientes", "Toallas", "Libros", "Entretenimiento"
    ],
    "Seguridad y Salvamento": [
        "Extintores", "Chalecos salvavidas", "Aros salvavidas",
        "Señales de bengala", "Kits de primeros auxilios", "Radios portátiles"
    ],
    "Energía y Baterías": [
        "Baterías para motores", "Paneles solares portátiles",
        "Generadores eléctricos", "Cargadores"
    ],
    "Kits Especializados": [
        "Kit de herramientas básicas", "Kit de primeros auxilios",
        "Kit de reparación eléctrica", "Kit de supervivencia"
    ],
    "Servicios de Mantenimiento y Reparación": [
        "Servicio Reparación de motores",
        "Servicio Reparación eléctrica",
        "Servicio Soldadura",
        "Servicio Reparación de sistemas hidráulicos",
        "Servicio Limpieza de casco o hélice"
    ],
    "Servicios de Recarga y Reposición": [
        "Servicio Recarga de combustible (bunker)",
        "Servicio Recarga de agua potable",
        "Servicio Recarga de gas",
        "Servicio Reposición de víveres"
    ],
    "Servicios de Inspecciones y Certificaciones": [
        "Servicio Inspección de seguridad",
        "Servicio Control de plagas",
        "Servicio Certificación sanitaria",
        "Servicio Pruebas de emisiones"
    ],
    "Servicios de Atención Médica y Salud": [
        "Servicio Atención médica de emergencia",
        "Servicio Revisión de tripulación",
        "Servicio Suministro de medicamentos"
    ],
    "Servicios Administrativos y Aduaneros": [
        "Servicio Gestión de documentos de entrada/salida",
        "Servicio Coordinación aduanera",
        "Servicio Asistencia con inmigración"
    ],
    "Servicios de Logística y Transporte": [
        "Servicio Transporte terrestre para tripulación",
        "Servicio Alquiler de vehículos",
        "Servicio Carga y descarga"
    ],
    "Servicios de Comunicaciones y Electrónica": [
        "Servicio Reparación de equipos de navegación",
        "Servicio Instalación de antenas satelitales",
        "Servicio Acceso a internet temporal"
    ],
    "Servicios de Catering y Servicios a Bordo": [
        "Servicio Catering a bordo (comidas preparadas)",
        "Servicio Lavandería",
        "Servicio Entretenimiento"
    ],
    "Servicios de Limpieza y Gestión de Residuos": [
        "Servicio Recolección de basura",
        "Servicio Limpieza general del barco",
        "Servicio Gestión de residuos peligrosos"
    ],
    "Servicios de Emergencia": [
        "Servicio Rescate marítimo",
        "Servicio Apoyo en averías graves",
        "Servicio Asistencia en encallamientos"
    ],
    "Otros": ["Otros"]
}

TIPO_CHOICES = [(tipo, tipo) for tipo in TIPO_SUBTIPO_MAP.keys()]
SUBTIPO_CHOICES = [(sub, sub) for subs in TIPO_SUBTIPO_MAP.values() for sub in subs]
