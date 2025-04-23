from django.urls import path

from apps.users.views import (
    ChangeRankView,
    GetProfileCertificateView,
    ProfileCreateView,
    ProfileListView,
    ProfileToAdminView,
)

urlpatterns = [
    path('', ProfileListView.as_view(), name='users_get_all'),
    path('/create', ProfileCreateView.as_view(), name='users_create_new_profile'),
    path('/<int:pk>/rank', ChangeRankView.as_view(), name='users_change_name'),
    path('/<int:pk>/certificate', GetProfileCertificateView.as_view(), name='users_get_profile_for_certificate'),
    path('/<int:pk>/to_admin', ProfileToAdminView.as_view(), name='users_profile_to_admin'),
]