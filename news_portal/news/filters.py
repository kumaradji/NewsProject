from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    add_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    add_date = DateTimeFilter(
        field_name='created',
        lookup_expr='gt',
        label='Дата создания',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    add_category = ModelChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label='Категория поста',
        empty_label='all'
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'rating': ['gt', 'lt']
        }
