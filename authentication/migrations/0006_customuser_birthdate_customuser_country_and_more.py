# Generated by Django 5.0.3 on 2024-03-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_customuser_activation_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='facebook_profile',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profile_pics/'),
        ),
    ]
