from rest_framework import serializers

from ..models import Category
from ..utils import create_from_breadcrumbs


class CategoryField(serializers.RelatedField):
    def __init__(self, **kwargs):
        kwargs["queryset"] = Category.objects
        super(CategoryField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return create_from_breadcrumbs(data)

    def to_representation(self, value):
        return value.full_name
