from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    add_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    add_category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория поста',
        empty_label='all'
    )
    add_date = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата публикации',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
