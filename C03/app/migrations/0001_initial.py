# Generated by Django 3.1.2 on 2020-11-16 07:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=32, null=True)),
                ('price', models.IntegerField()),
                ('openState', models.BooleanField()),
                ('floor', models.IntegerField(null=True)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('startTime', models.CharField(max_length=10)),
                ('endTime', models.CharField(max_length=10)),
                ('openState', models.BooleanField()),
                ('accessible', models.BooleanField()),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.court')),
            ],
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('information', models.CharField(max_length=300)),
                ('openingHours', models.CharField(max_length=50, verbose_name='scheduleForCourt')),
                ('openTime', models.CharField(max_length=32)),
                ('closeTime', models.CharField(max_length=32)),
                ('contact', models.CharField(max_length=32, null=True)),
                ('openState', models.BooleanField()),
                ('foreDays', models.IntegerField()),
                ('durations', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('userId', models.IntegerField(verbose_name='studentId')),
                ('email', models.EmailField(max_length=254)),
                ('loginToken', models.CharField(max_length=100, null=True)),
                ('phone', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReserveEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('S', 'success'), ('F', 'fail'), ('W', 'waiting')], default='W', max_length=2)),
                ('startTime', models.CharField(max_length=50)),
                ('endTime', models.CharField(max_length=50)),
                ('payment', models.BooleanField(null=True, verbose_name='Whether user has payed')),
                ('cancel', models.BooleanField(null=True, verbose_name='Whether this event has been canceled')),
                ('checked', models.BooleanField(null=True, verbose_name='Whether user has used court')),
                ('leave', models.BooleanField(null=True, verbose_name='Whether user has left court')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.court')),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.duration')),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('userId', models.IntegerField(verbose_name='managerId')),
                ('email', models.EmailField(max_length=254)),
                ('loginToken', models.CharField(max_length=100, null=True)),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium')),
            ],
        ),
        migrations.AddField(
            model_name='duration',
            name='stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium'),
        ),
        migrations.AddField(
            model_name='duration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AddField(
            model_name='court',
            name='stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.court')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openingHours', models.CharField(max_length=300)),
                ('date', models.CharField(max_length=32)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.IntegerField(default=1)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.manager')),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium')),
            ],
        ),
        migrations.CreateModel(
            name='AddEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.CharField(max_length=32)),
                ('endTime', models.CharField(max_length=32)),
                ('date', models.CharField(max_length=32)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.IntegerField(default=2)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.court')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.manager')),
            ],
        ),
    ]
