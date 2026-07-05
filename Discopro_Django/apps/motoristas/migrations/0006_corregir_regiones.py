from django.db import migrations


def corregir_regiones_compuestas(apps, schema_editor):
    Sucursal = apps.get_model('motoristas', 'Sucursal')
    Motorista = apps.get_model('motoristas', 'Motorista')

    for sucursal in Sucursal.objects.filter(region='Arica y Parinacota'):
        if sucursal.provincia == 'Parinacota':
            sucursal.region = 'Parinacota'
        else:
            sucursal.region = 'Arica'
        sucursal.save(update_fields=['region'])

    for motorista in Motorista.objects.filter(region='Arica y Parinacota'):
        if motorista.provincia == 'Parinacota':
            motorista.region = 'Parinacota'
        else:
            motorista.region = 'Arica'
        motorista.save(update_fields=['region'])


class Migration(migrations.Migration):

    dependencies = [
        ('motoristas', '0005_arquitectura_logistica'),
    ]

    operations = [
        migrations.RunPython(corregir_regiones_compuestas, migrations.RunPython.noop),
    ]
