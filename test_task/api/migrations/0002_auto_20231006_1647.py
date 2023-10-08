# Generated by Django 3.2.22 on 2023-10-06 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='link',
            new_name='links',
        ),
        migrations.AlterField(
            model_name='link',
            name='employee',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='сотрудник'),
        ),
    ]