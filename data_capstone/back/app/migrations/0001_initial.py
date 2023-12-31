# Generated by Django 3.2.19 on 2023-06-11 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happy', models.IntegerField(default=0)),
                ('sad', models.IntegerField(default=0)),
                ('neutral', models.IntegerField(default=0)),
                ('detectionError', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
