from django.db import migrations
from django.contrib.auth import get_user_model

def create_default_user(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(email='admin@admin.com').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', '1234')

class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]