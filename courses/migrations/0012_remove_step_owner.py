# Generated by Django 4.0.5 on 2022-08-05 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_actionphoto_actionvideo_remove_stepvideo_step_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='owner',
        ),
    ]
