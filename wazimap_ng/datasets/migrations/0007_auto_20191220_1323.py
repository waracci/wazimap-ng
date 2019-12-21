# Generated by Django 2.2.9 on 2019-12-20 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0006_auto_20191220_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorSubcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.IndicatorCategory')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Indicator')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Profile')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.IndicatorSubcategory')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='indicators',
            field=models.ManyToManyField(through='datasets.ProfileIndicator', to='datasets.Indicator'),
        ),
    ]
