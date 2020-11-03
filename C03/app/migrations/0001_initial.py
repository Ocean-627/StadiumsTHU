# Generated by Django 3.1.2 on 2020-11-03 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stadiumId', models.IntegerField()),
                ('openingHours', models.CharField(max_length=300)),
                ('date', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=32, null=True)),
                ('price', models.IntegerField()),
                ('openingHours', models.CharField(max_length=50)),
                ('openState', models.BooleanField()),
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
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('userId', models.IntegerField(verbose_name='managerId')),
                ('email', models.EmailField(max_length=254)),
                ('workPlace', models.CharField(max_length=32, null=True)),
                ('workPlaceId', models.IntegerField(null=True)),
                ('loginToken', models.CharField(max_length=100)),
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
                ('schedule', models.CharField(max_length=32, null=True)),
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
                ('stadiumName', models.CharField(max_length=32)),
                ('courtName', models.CharField(max_length=32, null=True)),
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
        migrations.AddField(
            model_name='duration',
            name='stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium'),
        ),
        migrations.AddField(
            model_name='court',
            name='stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stadium'),
        ),
    ]
