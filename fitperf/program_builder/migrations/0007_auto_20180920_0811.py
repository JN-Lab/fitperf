# Generated by Django 2.1.1 on 2018-09-20 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program_builder', '0006_auto_20180920_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementsperexercise',
            name='movement_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]