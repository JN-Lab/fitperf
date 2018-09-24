# Generated by Django 2.1.1 on 2018-09-18 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('exercise_type', models.CharField(choices=[('RUN', 'RUNNING'), ('FORTIME', 'FORTIME'), ('AMRAP', 'AMRAP'), ('WARMUP', 'ECHAUFFEMENT'), ('STRENGTH', 'FORCE'), ('EMOM', 'EMOM'), ('CONDITIONNING', 'CONDITIONNEMENT'), ('MAX_REP', 'MAXIMUM DE REPETITION')], max_length=20)),
                ('performance_type', models.CharField(choices=[('TIME', 'Temps'), ('NB_ROUNDS', 'Nombre de tours'), ('NB_REP', 'Nombre de repetitions')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExercisesPerSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.BooleanField(default=False)),
                ('performance', models.DecimalField(decimal_places=1, max_digits=5, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Equipment', verbose_name="the movement's equipment")),
            ],
        ),
        migrations.CreateModel(
            name='MovementSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('REP', 'Repetitions'), ('WEIGTH', 'Poids'), ('DISTANCE', 'Distance')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovementsPerExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_value', models.DecimalField(decimal_places=1, max_digits=5)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Exercise')),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Movement')),
                ('movement_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.MovementSettings')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the program's creator")),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('done', models.BooleanField(default=False)),
                ('exercises', models.ManyToManyField(related_name='sessions', through='program_builder.ExercisesPerSession', to='program_builder.Exercise', verbose_name='list of exercises per session')),
                ('program', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='program_builder.Program', verbose_name='program linked to the session if exists')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('exercises', models.ManyToManyField(related_name='trainings', to='program_builder.Exercise', verbose_name='list of exercises per training')),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the training's creator")),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Training', verbose_name='training associated to the session'),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name='user who does the session'),
        ),
        migrations.AddField(
            model_name='program',
            name='trainings',
            field=models.ManyToManyField(related_name='programs', to='program_builder.Training', verbose_name='list of trainings per program'),
        ),
        migrations.AddField(
            model_name='movementsettings',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the movement setting's creator"),
        ),
        migrations.AddField(
            model_name='movement',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the movement's creator"),
        ),
        migrations.AddField(
            model_name='movement',
            name='settings',
            field=models.ManyToManyField(related_name='movements', to='program_builder.MovementSettings', verbose_name='list of settings'),
        ),
        migrations.AddField(
            model_name='exercisespersession',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Session'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the execise's creator"),
        ),
        migrations.AddField(
            model_name='exercise',
            name='movements',
            field=models.ManyToManyField(related_name='exercises', through='program_builder.MovementsPerExercise', to='program_builder.Movement', verbose_name='list of movements per exercise'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the movement's creator"),
        ),
    ]