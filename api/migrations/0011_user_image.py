# Generated by Django 3.2.25 on 2024-11-28 05:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_user_work_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'], message='Faqat png yoki jpg rasm yuklashingiz mumkin')]),
        ),
    ]
