# Generated by Django 4.0.5 on 2022-08-05 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_action_course_action_process'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='media/courses/actions/photos/static/')),
            ],
        ),
        migrations.CreateModel(
            name='ActionVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to='media/courses/actions/videos/')),
            ],
        ),
        migrations.RemoveField(
            model_name='stepvideo',
            name='step',
        ),
        migrations.RemoveField(
            model_name='step',
            name='main_text',
        ),
        migrations.AddField(
            model_name='action',
            name='main_text',
            field=models.TextField(default='jjj'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='StepPhoto',
        ),
        migrations.DeleteModel(
            name='StepVideo',
        ),
        migrations.AddField(
            model_name='actionvideo',
            name='action',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='courses.action'),
        ),
        migrations.AddField(
            model_name='actionphoto',
            name='action',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='courses.action'),
        ),
    ]
