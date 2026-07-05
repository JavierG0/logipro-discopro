from django.db import migrations, models


def migrar_direccion_destino(apps, schema_editor):
    Movimiento = apps.get_model('movimientos', 'Movimiento')
    for movimiento in Movimiento.objects.all():
        direccion = getattr(movimiento, 'destinatario_direccion', '') or ''
        Movimiento.objects.filter(pk=movimiento.pk).update(direccion_destino=direccion)


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0004_rename_provincia_to_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='direccion_destino',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.RunPython(migrar_direccion_destino, migrations.RunPython.noop),
        migrations.RemoveIndex(
            model_name='movimiento',
            name='movimiento_motoris_cb5817_idx',
        ),
        migrations.RemoveIndex(
            model_name='movimiento',
            name='movimiento_fecha_p_b3873d_idx',
        ),
        migrations.RemoveField(model_name='movimiento', name='calificacion'),
        migrations.RemoveField(model_name='movimiento', name='comentarios'),
        migrations.RemoveField(model_name='movimiento', name='descripcion'),
        migrations.RemoveField(model_name='movimiento', name='destinatario_comuna'),
        migrations.RemoveField(model_name='movimiento', name='destinatario_direccion'),
        migrations.RemoveField(model_name='movimiento', name='destinatario_nombre'),
        migrations.RemoveField(model_name='movimiento', name='destinatario_region'),
        migrations.RemoveField(model_name='movimiento', name='destinatario_rut'),
        migrations.RemoveField(model_name='movimiento', name='destinatario_telefono'),
        migrations.RemoveField(model_name='movimiento', name='distancia_km'),
        migrations.RemoveField(model_name='movimiento', name='duracion_minutos'),
        migrations.RemoveField(model_name='movimiento', name='estado'),
        migrations.RemoveField(model_name='movimiento', name='fecha_cierre'),
        migrations.RemoveField(model_name='movimiento', name='fecha_inicio'),
        migrations.RemoveField(model_name='movimiento', name='fecha_programada'),
        migrations.RemoveField(model_name='movimiento', name='firma_confirmacion'),
        migrations.RemoveField(model_name='movimiento', name='hora_estimada_entrega'),
        migrations.RemoveField(model_name='movimiento', name='motorista'),
        migrations.RemoveField(model_name='movimiento', name='observaciones'),
        migrations.RemoveField(model_name='movimiento', name='sucursal'),
        migrations.RemoveField(model_name='movimiento', name='tipo_movimiento'),
        migrations.AlterModelOptions(
            name='movimiento',
            options={
                'ordering': ['-creado_en'],
                'verbose_name': 'Movimiento',
                'verbose_name_plural': 'Movimientos',
            },
        ),
    ]
