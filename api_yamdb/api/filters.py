from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter()
    year = filters.CharFilter()

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year', )
