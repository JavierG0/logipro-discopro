import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discopro.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute("DESC motorista")
cols = cursor.fetchall()
col_names = [c[0] for c in cols]
print("Columns in motorista:", col_names)
if 'moto_id' in col_names:
    print("- moto_id exists - needs to be removed")
    cursor.execute("ALTER TABLE motorista DROP FOREIGN KEY motorista_moto_id_28577458_fk_moto_id")
    cursor.execute("ALTER TABLE motorista DROP COLUMN moto_id")
    print("  -> moto_id removed")
if 'sucursal_id' in col_names:
    print("- sucursal_id exists - needs to be removed")
    cursor.execute("ALTER TABLE motorista DROP FOREIGN KEY motorista_sucursal_id_7eca1b1c_fk_sucursal_flota_id")
    cursor.execute("ALTER TABLE motorista DROP COLUMN sucursal_id")
    print("  -> sucursal_id removed")
print("Done!")
