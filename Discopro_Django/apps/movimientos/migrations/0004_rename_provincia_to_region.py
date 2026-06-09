from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0003_movimiento_destinatario_comuna_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movimiento',
            old_name='destinatario_provincia',
            new_name='destinatario_region',
        ),
    ]
