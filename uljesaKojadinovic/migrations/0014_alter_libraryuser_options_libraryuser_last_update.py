# Generated by Django 4.0.7 on 2022-08-16 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uljesaKojadinovic', '0013_alter_libraryuser_start_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='libraryuser',
            options={'get_latest_by': ['last_update']},
        ),
        migrations.AddField(
            model_name='libraryuser',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
    ]
