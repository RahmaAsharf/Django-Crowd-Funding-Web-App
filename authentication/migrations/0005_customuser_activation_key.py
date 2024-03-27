# Generated by Django 5.0.3 on 2024-03-26 22:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]