# Generated by Django 2.2.9 on 2019-12-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0002_remove_profile_indicators'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='indicators',
            field=models.ManyToManyField(through='datasets.ProfileIndicator', to='datasets.Indicator'),
        ),
    ]
