from django.db import migrations, models


def migrar_ciudad_a_comuna(apps, schema_editor):
    Sucursal = apps.get_model('motoristas', 'Sucursal')
    for sucursal in Sucursal.objects.all():
        ciudad = getattr(sucursal, 'ciudad', '') or ''
        if ciudad and not sucursal.comuna:
            sucursal.comuna = ciudad
            sucursal.save(update_fields=['comuna'])


class Migration(migrations.Migration):

    dependencies = [
        ('motoristas', '0003_unify_sucursal_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='region',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='sucursal',
            name='provincia',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='sucursal',
            name='comuna',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.RunPython(migrar_ciudad_a_comuna, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='sucursal',
            name='ciudad',
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='direccion',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.RemoveField(
            model_name='moto',
            name='sucursal',
        ),
        migrations.AddField(
            model_name='motorista',
            name='region',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='motorista',
            name='provincia',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='motorista',
            name='comuna',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='motorista',
            name='direccion',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
