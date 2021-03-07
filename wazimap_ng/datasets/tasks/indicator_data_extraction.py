import json
import logging

from django.db import transaction
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from django.contrib.postgres.fields.jsonb import KeyTextTransform

from .. import models
from itertools import groupby

logger = logging.getLogger(__name__)

from .data_accumulator import DataAccumulator


class Sorter:
    def __init__(self, primary_group=None):
        self.accumulators = {}
        self.primary_group = primary_group

    def get_accumulator(self, geography_id):
        if geography_id not in self.accumulators:
            self.accumulators[geography_id] = DataAccumulator(geography_id, self.primary_group)

        accumulator = self.accumulators[geography_id]
        return accumulator

    def add_groups_data(self, group, subindicator, data_blob):
        for datum in data_blob:
            geography_id = datum["geography_id"]
            accumulator = self.get_accumulator(geography_id)

            accumulator.add_groups_data(group, subindicator, datum)

    def add_subindicator_data(self, data_blob):
        for datum in data_blob:
            geography_id = datum["geography_id"]
            accumulator = self.get_accumulator(geography_id)
            accumulator.add_subindicator_data(datum["data"])


@transaction.atomic
def indicator_data_extraction(indicator, **kwargs):
    sorter = Sorter(primary_group=indicator.primary_group)

    models.IndicatorData.objects.filter(indicator=indicator).delete()
    for group in indicator.dataset.group_set.all():
        logger.debug(f"Extracting subindicators for: {group.name}")
        qs = models.DatasetData.objects.filter(dataset=indicator.dataset, data__has_keys=[group.name])
        if group.name != indicator.primary_group:
            subindicators = qs.get_unique_subindicators(group.name)

            for subindicator in subindicators:
                logger.debug(f"Extracting subindicators for: {group.name} -> {subindicator}")
                qs_subindicator = qs.filter(**{f"data__{group.name}": subindicator})

                counts = extract_counts(indicator, qs_subindicator, indicator.primary_group)
                sorter.add_groups_data(group.name, subindicator, counts)
        else:
            counts = extract_counts(indicator, qs, indicator.primary_group)
            sorter.add_subindicator_data(counts)


    datarows = []
    for geography_id, accumulator in sorter.accumulators.items():
        datarows.append(models.IndicatorData(
            indicator=indicator, geography_id=geography_id, data=accumulator.data
        )
    )

    models.IndicatorData.objects.bulk_create(datarows, 1000)

    return {
        "model": "indicator",
        "name": indicator.name,
        "id": indicator.id,
    }           

def extract_counts(indicator, qs, primary_group):

    ds_groups = indicator.dataset.group_set.all()
    nonagg_groups = ds_groups.filter(can_aggregate=False)
    nonagg_groups_names = [g.name for g in nonagg_groups]
    in_groups = list(set([primary_group] + nonagg_groups_names))
    
    if indicator.universe is not None:
        qs = qs.filter_by_universe(indicator.universe)

    groups = ["data__" + i for i in in_groups]
    c = Cast(KeyTextTransform("count", "data"), FloatField())

    qs = qs.exclude(data__count="")
    qs = qs.order_by("geography_id")
    data = groupby(qs.grouped_totals_by_geography(groups), lambda x: x["geography_id"])

    datarows = []
    for geography_id, group in data:
        data_dump = json.dumps(list(group))
        grouped = json.loads(data_dump.replace("data__", ""))

        for item in grouped:
            item.pop("geography_id")

        datarows.append({"geography_id": geography_id, "data": grouped})
    return datarows
