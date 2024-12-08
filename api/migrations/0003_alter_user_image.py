# Generated by Django 3.2.25 on 2024-11-24 07:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'], message='Faqat png yoki jpg rasm yuklashingiz mumkin')]),
        ),
    ]