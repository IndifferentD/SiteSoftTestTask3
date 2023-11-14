from django.db import migrations
from django.contrib.auth.models import User


def create_admin(apps, schema_editor):
    # Check if the superuser already exists
    if not User.objects.filter(username='admin').exists():
        # Create a new superuser
        User.objects.create_superuser('1', '', '1')
        print('Superuser "admin" created successfully.')
    else:
        print('Superuser "admin" already exists.')


class Migration(migrations.Migration):
    dependencies = [
        ('parser_configurator', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
