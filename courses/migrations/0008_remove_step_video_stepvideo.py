# Generated by Django 4.0.5 on 2022-08-03 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_step_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='video',
        ),
        migrations.CreateModel(
            name='StepVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to='media/courses/actions/videos/')),
                ('step', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='courses.step')),
            ],
        ),
    ]
