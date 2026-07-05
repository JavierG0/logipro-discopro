from django.db import migrations


def eliminar_columnas_legacy(apps, schema_editor):
    Motorista = apps.get_model('motoristas', 'Motorista')
    tabla = Motorista._meta.db_table
    columnas = ('vehiculo_placa', 'marca_vehiculo', 'modelo_vehiculo', 'año_vehiculo')
    conexion = schema_editor.connection
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT COLUMN_NAME FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
            """,
            [tabla],
        )
        existentes = {fila[0] for fila in cursor.fetchall()}
        for columna in columnas:
            if columna in existentes:
                cursor.execute(f'ALTER TABLE `{tabla}` DROP COLUMN `{columna}`')


class Migration(migrations.Migration):

    dependencies = [
        ('motoristas', '0006_corregir_regiones'),
    ]

    operations = [
        migrations.RunPython(eliminar_columnas_legacy, migrations.RunPython.noop),
    ]
