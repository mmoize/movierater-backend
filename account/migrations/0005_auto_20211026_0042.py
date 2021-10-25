# Generated by Django 3.1.3 on 2021-10-25 14:42

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20211023_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default-3.png', upload_to=account.models.get_image_path),
        ),
    ]
