# Generated by Django 3.2.10 on 2022-06-15 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_rec', '0004_alter_enroll_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enroll',
            name='Arid_no',
            field=models.CharField(max_length=12),
        ),
    ]
