# Generated by Django 2.2.9 on 2019-12-20 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0007_auto_20191220_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='geography',
            options={'verbose_name_plural': 'geographies'},
        ),
        migrations.AlterModelOptions(
            name='indicatorcategory',
            options={'verbose_name_plural': 'Indicator Categories'},
        ),
        migrations.AlterModelOptions(
            name='indicatorsubcategory',
            options={'verbose_name_plural': 'Indicator Subcategories'},
        ),
    ]
