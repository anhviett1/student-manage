# Generated by Django 4.2.20 on 2025-06-02 07:52

import api.app_score.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_subject', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_student', '0001_initial'),
        ('app_score', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='student',
            field=models.ForeignKey(default=api.app_score.models.get_default_student, on_delete=django.db.models.deletion.CASCADE, related_name='student_scores', to='app_student.student', verbose_name='Sinh viên'),
        ),
        migrations.AddField(
            model_name='score',
            name='subject',
            field=models.ForeignKey(default=api.app_score.models.get_default_subject, on_delete=django.db.models.deletion.CASCADE, related_name='subject_scores', to='app_subject.subject', verbose_name='Môn học'),
        ),
        migrations.AddField(
            model_name='score',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_scores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('student', 'subject', 'semester')},
        ),
    ]
