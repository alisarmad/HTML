# Generated by Django 2.0.3 on 2019-10-23 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0029_teacherfuturemapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='futureteachermapping',
            name='connected_future_student_id',
        ),
        migrations.RemoveField(
            model_name='futureteachermapping',
            name='teacher_id',
        ),
        migrations.RemoveField(
            model_name='futureteachermapping',
            name='teacher_user_id',
        ),
        migrations.RemoveField(
            model_name='teacherfuturemapping',
            name='connected_teacher_id',
        ),
        migrations.RemoveField(
            model_name='teacherfuturemapping',
            name='future_id',
        ),
        migrations.RemoveField(
            model_name='teacherfuturemapping',
            name='future_student_user_id',
        ),
        migrations.DeleteModel(
            name='FutureTeacherMapping',
        ),
        migrations.DeleteModel(
            name='TeacherFutureMapping',
        ),
    ]
