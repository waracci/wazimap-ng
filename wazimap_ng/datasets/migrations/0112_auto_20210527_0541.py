# Generated by Django 2.2.13 on 2021-05-27 05:41

from django.db import migrations
from django.db.models import Count


def remove_duplicate_groups(apps, schema_editor):
    Dataset = apps.get_model("datasets", "Dataset")
    DatasetData = apps.get_model("datasets", "DatasetData")

    # loop over all datasets
    for dataset in Dataset.objects.all():

        # Get groups for a dataset
        groups = dataset.group_set.all()

        # loop over groups and check if group with same name exists more
        # one time
        for group in groups.values("name").annotate(gc=Count("name")):

            # Filter group by name and order by updated
            # So we can get latest updated group
            filtered_group = groups.filter(name=group["name"]).order_by("-updated")
            last_updated_group = filtered_group.first()

            # if count of groups in greater than one 
            # Delete all groups of dataset with same name except last updated group
            if group["gc"] > 1:
                filtered_group.exclude(id=last_updated_group.id).delete()

            # Fetch list of subindicator from dataset data
            subindicators = list(
                DatasetData.objects.filter(dataset=dataset)
                .order_by()
                .values_list(F"data__{group['name']}", flat=True)
                .distinct()
            )

            # Sort subindicators acording to last updated groups subindicator

            sub_groups = last_updated_group.subindicators
            sorted_list = sorted(
                subindicators, key=lambda x: sub_groups.index(x) if x in sub_groups else len(subindicators)
            )

            last_updated_group.subindicators = sorted_list
            last_updated_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0111_auto_20210322_0740'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_groups),
    ]
