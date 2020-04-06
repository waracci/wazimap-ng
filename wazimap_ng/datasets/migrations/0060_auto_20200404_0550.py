# Generated by Django 2.2.10 on 2020-04-04 05:50

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import wazimap_ng.datasets.models.upload


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0059_auto_20200402_0808'),
        ('datasets', '0062_auto_20200403_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetfile',
            name='document',
            field=models.FileField(help_text='\n            Uploaded document should be less than 3000.0 MiB in size and \n            file extensions should be one of xls, xlsx, csv.\n        ', upload_to=wazimap_ng.datasets.models.upload.get_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xls', 'xlsx', 'csv']), wazimap_ng.datasets.models.upload.file_size]),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='groups',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), blank=True, default=list, size=None),
        ),
    ]
