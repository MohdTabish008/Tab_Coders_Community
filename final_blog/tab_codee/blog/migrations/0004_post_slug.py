# Generated by Django 3.1.4 on 2020-12-30 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201230_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]
