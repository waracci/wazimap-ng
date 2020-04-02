from django.contrib import admin
from django.contrib.postgres import fields

from .. import models
from .. import widgets
from .utils import customTitledFilter, description

@admin.register(models.ProfileIndicator)
class ProfileIndicatorAdmin(admin.ModelAdmin):
    list_filter = (
        ('profile__name', customTitledFilter('Profile')),
        ('indicator__name', customTitledFilter('Indicator')),
        ('subcategory__category__name', customTitledFilter('Category')),
        "subcategory",
    )

    list_display = (
        "profile",
        "label", 
        description("Indicator", lambda x: x.indicator.name), 
        description("Category", lambda x: x.subcategory.category.name),
        "subcategory",
        "key_metric",
    )

    fieldsets = (
        ("Database fields (can't change after being created)", {
            'fields': ('profile', 'indicator')
        }),
        ("Profile fields", {
          'fields': ('label', 'subcategory', 'key_metric', 'description', 'choropleth_method')
        }),
        ("Subindicators", {
          'fields': ('subindicators',)
        })
    )

    formfield_overrides = {
        fields.ArrayField: {"widget": widgets.SortableWidget},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ("profile",) + self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.subindicators = obj.indicator.subindicators
        super().save_model(request, obj, form, change)