# Generated by Django 3.2.18 on 2023-05-04 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20230504_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='init_time',
            field=models.DateTimeField(null=True),
        ),
    ]
