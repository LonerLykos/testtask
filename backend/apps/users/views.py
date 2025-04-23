from datetime import date

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.users.filter import ProfileFilter
from apps.users.models import RankModel
from apps.users.serializers import ChangeRankSerializer, ProfileSerializer
from core.pagination import PagePagination
from django_filters.rest_framework import DjangoFilterBackend

ProfileModel = get_user_model()


class ProfileCreateView(CreateAPIView):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


class ProfileListView(ListAPIView):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = ProfileFilter
    pagination_class = PagePagination


class ChangeRankView(GenericAPIView):
    serializer_class = ChangeRankSerializer
    queryset = ProfileModel.objects.all()
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            rank_id = serializer.validated_data['rank_id']

            try:
                rank = RankModel.objects.get(id=rank_id)
            except Exception:
                return Response({'detail': 'Such a rank does not exist'}, status=status.HTTP_404_NOT_FOUND)

            profile.user.rank = rank
            profile.user.save()

            return Response({"status": "rank updated"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProfileCertificateView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        profile_id = request.data.get('profile')

        if not profile_id:
            return Response({'error': 'profile is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_profile = ProfileModel.objects.get(id=profile_id)
        except ProfileModel.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        certificate_image_url = '/api/media/certificate/certificate.jpg'

        template = get_template('certificate.html')
        context = {
            'admin': request.user,
            'profile': selected_profile,
            'certificate_data': {
                'title': 'Certificate',
                'date': date.today().strftime('%d.%m.%Y'),
                'certificate_image_url': certificate_image_url,
            }
        }
        rendered_html = template.render(context, request)
        return HttpResponse(rendered_html, content_type='text/html')


class ProfileToAdminView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProfileModel.objects.all().exclude(id=self.request.profile.id)

    def patch(self, *args, **kwargs):
        profile = self.get_object()
        if not profile.is_staff:
            profile.is_staff = True
            profile.save()

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status.HTTP_200_OK)

class RetrieveProfileView(GenericAPIView):
    serializer_class = ChangeRankSerializer
    queryset = ProfileModel.objects.all()
    permission_classes = [IsAdminUser]