# Generated by Django 4.0.1 on 2023-01-05 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_chat_id', models.CharField(max_length=255)),
                ('t_user_id', models.CharField(max_length=255)),
                ('fk_user_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]