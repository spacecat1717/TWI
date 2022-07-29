# Generated by Django 4.0.5 on 2022-07-27 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_action_slug_alter_step_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stepphoto',
            name='action',
        ),
        migrations.AddField(
            model_name='stepphoto',
            name='step',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='courses.step'),
        ),
    ]
