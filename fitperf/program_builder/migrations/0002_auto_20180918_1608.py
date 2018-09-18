# Generated by Django 2.1.1 on 2018-09-18 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program_builder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="the movement's creator"),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="the execise's creator"),
        ),
        migrations.AlterField(
            model_name='movement',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="the movement's creator"),
        ),
        migrations.AlterField(
            model_name='movementsettings',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="the movement setting's creator"),
        ),
        migrations.AlterField(
            model_name='program',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="the program's creator"),
        ),
        migrations.AlterField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user who does the session'),
        ),
        migrations.AlterField(
            model_name='training',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="the training's creator"),
        ),
    ]
