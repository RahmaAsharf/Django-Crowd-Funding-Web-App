# Generated by Django 5.0.3 on 2024-03-23 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customuser_birthdate_customuser_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='authentication/images/'),
        ),
    ]
