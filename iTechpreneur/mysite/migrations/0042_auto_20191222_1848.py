# Generated by Django 2.0.7 on 2019-12-22 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0041_employeeee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='future_student_post',
            name='future_student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Graduate'),
        ),
    ]
