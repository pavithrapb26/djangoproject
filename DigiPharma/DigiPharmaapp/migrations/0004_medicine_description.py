# Generated by Django 5.1.2 on 2024-10-29 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DigiPharmaapp', '0003_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
