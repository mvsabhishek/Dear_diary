# Generated by Django 2.0.5 on 2018-06-11 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drdiary', '0005_auto_20180611_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
