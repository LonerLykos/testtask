from django_filters import rest_framework as filters

class ProfileFilter(filters.FilterSet):
    profile_id_in = filters.BaseInFilter(field_name='id')
    profile_id_lt = filters.NumberFilter(field_name='id', lookup_expr='lt')
    profile_id_gt = filters.NumberFilter(field_name='id', lookup_expr='gt')
    profile_id_lte = filters.NumberFilter(field_name='id', lookup_expr='lte')
    profile_id_gte = filters.NumberFilter(field_name='id', lookup_expr='gte')
    profile_is_staff = filters.BooleanFilter()
    profile_is_active = filters.BooleanFilter()
    name_endswith = filters.CharFilter(field_name='user__name', lookup_expr='iendswith')
    name_startswith = filters.CharFilter(field_name='user__name', lookup_expr='istartswith')
    name_contains = filters.CharFilter(field_name='user__name', lookup_expr='icontains')
    surname_endswith = filters.CharFilter(field_name='user__surname', lookup_expr='iendswith')
    surname_startswith = filters.CharFilter(field_name='user__surname', lookup_expr='istartswith')
    surname_contains = filters.CharFilter(field_name='user__surname', lookup_expr='icontains')
    rank_id_in = filters.BaseInFilter(field_name='user__rank__id')
    rank_id_lt = filters.NumberFilter(field_name='user__rank__id', lookup_expr='lt')
    rank_id_gt = filters.NumberFilter(field_name='user__rank__id', lookup_expr='gt')
    rank_id_lte = filters.NumberFilter(field_name='user__rank__id', lookup_expr='lte')
    rank_id_gte = filters.NumberFilter(field_name='user__rank__id', lookup_expr='gte')
    rank_name_endswith = filters.CharFilter(field_name='user_rank__rank_name', lookup_expr='iendswith')
    rank_name_startswith = filters.CharFilter(field_name='user_rank__rank_name', lookup_expr='istartswith')
    rank_name_contains = filters.CharFilter(field_name='user_rank__rank_name', lookup_expr='icontains')

    order = filters.OrderingFilter(
        fields=[
            'id',
            'email',
            'is_active',
            'is_staff',
            'user__name',
            'user__surname',
            'user__rank__rank_name',
            'user__rank__id',
        ]
    )