<<<<<<< HEAD
# Generated by Django 3.1.2 on 2020-11-04 12:42
=======
# Generated by Django 3.1.1 on 2020-11-03 15:07
>>>>>>> 7cefe6294fcf73231678ad718931b26d94d0724d

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='floor',
            field=models.IntegerField(null=True),
        ),
    ]
