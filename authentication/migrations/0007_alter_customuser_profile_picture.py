# Generated by Django 3.2.20 on 2024-03-27 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_customuser_birthdate_customuser_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='authentication/images/'),
        ),
    ]
