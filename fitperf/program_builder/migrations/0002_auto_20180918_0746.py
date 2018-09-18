# Generated by Django 2.1.1 on 2018-09-18 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program_builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('challenge', models.BooleanField(default=False)),
                ('done', models.BooleanField(default=False)),
                ('performance', models.DecimalField(decimal_places=1, max_digits=5, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='exercise',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the execise's creator"),
        ),
        migrations.AlterField(
            model_name='movement',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the movement's creator"),
        ),
        migrations.AlterField(
            model_name='program',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the program's creator"),
        ),
        migrations.AlterField(
            model_name='training',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile', verbose_name="the training's creator"),
        ),
        migrations.AddField(
            model_name='session',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Exercise'),
        ),
        migrations.AddField(
            model_name='session',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Program'),
        ),
        migrations.AddField(
            model_name='session',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Training'),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program_builder.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='exercises',
            field=models.ManyToManyField(through='program_builder.Session', to='program_builder.Exercise', verbose_name='list of exercises per user'),
        ),
        migrations.AddField(
            model_name='profile',
            name='programs',
            field=models.ManyToManyField(related_name='profiles', through='program_builder.Session', to='program_builder.Program', verbose_name='list of programs per user'),
        ),
        migrations.AddField(
            model_name='profile',
            name='trainings',
            field=models.ManyToManyField(related_name='profiles', through='program_builder.Session', to='program_builder.Training', verbose_name='list of trainings per user'),
        ),
        migrations.AddField(
            model_name='program',
            name='exercises',
            field=models.ManyToManyField(related_name='programs', through='program_builder.Session', to='program_builder.Exercise', verbose_name='list of exercises per program'),
        ),
        migrations.AddField(
            model_name='program',
            name='trainings',
            field=models.ManyToManyField(related_name='programs', through='program_builder.Session', to='program_builder.Training', verbose_name='list of trainings per program'),
        ),
        migrations.AddField(
            model_name='training',
            name='exercises',
            field=models.ManyToManyField(related_name='trainings', through='program_builder.Session', to='program_builder.Exercise', verbose_name='list of exercises per training'),
        ),
    ]
