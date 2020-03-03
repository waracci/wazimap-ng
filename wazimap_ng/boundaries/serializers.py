from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometrySerializerMethodField 
from rest_framework import serializers
from . import models
from ..datasets.models import Geography
from ..points.models import Location

from django.core.serializers import serialize
from itertools import groupby
from django.db.models import Count


class GeographySerializer(GeoFeatureModelSerializer):
    geom = GeometrySerializerMethodField()
    parent = serializers.SerializerMethodField()

    # TODO might want simplification to come from settings.py
    def __init__(self, *args, simplification=0.005, parentCode=None, **kwargs):
        super(GeographySerializer, self).__init__(*args, **kwargs)
        self.simplification = simplification
        self.parentCode = parentCode


    def get_geom(self, obj):
        return obj.geom_cache

    def get_parent(self, obj):
        if self.parentCode is not None:
            return self.parentCode

        code = obj.code
        # TODO how to handle no results
        # TODO this might get inefficient with many children
        geo = obj.geography
        parent = geo.get_parent()
        if parent is not None:
            return parent.code
        return None


class GeographyBoundarySerializer(GeographySerializer):
    level = serializers.SerializerMethodField()
    themes = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, simplification=0.005, **kwargs)

    def get_level(self, obj):
        return obj.geography.level

    def get_themes(self, obj):
        themes = []
        if obj.geom:
            fields = ["category__name", "category__theme", "category__theme__name", "category__theme__icon"]

            for theme_id, data in groupby(
                Location.objects.filter(
                    coordinates__intersects=obj.geom
                ).values(*fields).annotate(count=Count("name")),
                lambda x: x["category__theme"]
            ):
                data=list(data)
                theme_count = 0
                categories = []

                for category in data:
                    categories.append({
                        "name": category["category__name"],
                        "count": category["count"]
                    })
                    theme_count = theme_count + category["count"]

                icon = data[0]["category__theme__icon"]
                name = data[0]["category__theme__name"]
                if not icon:
                    icon = "icon--%s" % name.lower()

                themes.append({
                    "name": name,
                    "count": theme_count,
                    "icon": icon,
                    "id": theme_id,
                    "categories": categories,
                })

        return themes

    class Meta:
        model = models.GeographyBoundary
        geo_field = "geom_cache"

        fields = ("code", "name", "area", "parent", "level", "themes")
