from django.db import migrations

def crear_puertos_por_defecto(apps, schema_editor):
    Puerto = apps.get_model('GestorNavios', 'Puerto')
    puertos_defecto = [
    "Puerto Acajutla",         # El Salvador
    "Puerto de La Unión",      # El Salvador
    "Puerto El Triunfo",       # El Salvador
    "Puerto de Balboa",        # Panamá
    "Puerto de Colón",         # Panamá
    "Puerto de Veracruz",      # México
    "Puerto de Manzanillo",    # México
    "Puerto de Santos",        # Brasil
    "Puerto de Buenos Aires",  # Argentina
    "Puerto de Valparaíso",    # Chile
    "Puerto de Cartagena",     # Colombia
    "Puerto de Callao",        # Perú
    "Puerto de Miami",         # Estados Unidos
    "Puerto de Los Ángeles",   # Estados Unidos
    "Puerto de Rotterdam",     # Países Bajos
    "Puerto de Hamburgo",      # Alemania
    "Puerto de Singapur",      # Singapur
    "Puerto de Shanghai",      # China
    "Puerto de Dubai",         # Emiratos Árabes Unidos
    ]

    for nombre in puertos_defecto:
        Puerto.objects.get_or_create(nombre=nombre)

class Migration(migrations.Migration):

    dependencies = [
    ('GestorNavios', '0007_remove_asignacionrecursos_escala_and_more'),
    ]

    operations = [
        migrations.RunPython(crear_puertos_por_defecto),
    ]
