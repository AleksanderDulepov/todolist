# Generated by Django 4.0.1 on 2022-12-21 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='due_data',
            new_name='due_date',
        ),
    ]