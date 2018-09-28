# Generated by Django 2.1.1 on 2018-09-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program_builder', '0012_auto_20180926_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='exercise_type',
            field=models.CharField(choices=[('RUNNING', 'RUNNING'), ('FORTIME', 'FORTIME'), ('AMRAP', 'AMRAP'), ('ECHAUFFEMENT', 'ECHAUFFEMENT'), ('FORCE', 'FORCE'), ('EMOM', 'EMOM'), ('CONDITIONNEMENY', 'CONDITIONNEMENT'), ('MAXIMUM DE REPETITIONS', 'MAXIMUM DE REPETITIONS')], max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='performance_type',
            field=models.CharField(choices=[('Temps', 'Temps'), ('Nombre de tours', 'Nombre de tours'), ('Nombre de répétitions', 'Nombre de répétitions'), ('Distance', 'Distance')], max_length=20, null=True),
        ),
    ]