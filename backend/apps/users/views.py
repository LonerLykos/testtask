import io
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import FileResponse

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.users.filter import ProfileFilter
from apps.users.models import RankModel
from apps.users.serializers import ChangeRankSerializer, ProfileSerializer
from cairosvg import svg2png
from core.pagination import PagePagination
from django_filters.rest_framework import DjangoFilterBackend
from PIL import Image, ImageDraw, ImageFont, ImageOps

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


class GetProfileCertificateView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def create_rounded_avatar(self, image, size):
        mask = Image.new('L', size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + size, fill=255)

        avatar = image.resize(size, Image.Resampling.LANCZOS)
        output = Image.new('RGBA', size, (0, 0, 0, 0))
        output.paste(avatar, (0, 0), mask)
        return output

    def svg_to_png(self, svg_path):
        output_path = svg_path.replace('.svg', '.png')
        svg2png(url=svg_path, write_to=output_path)
        img = Image.open(output_path).convert('RGBA')
        os.remove(output_path)
        return img

    def get(self, request, pk, *args, **kwargs):
        try:
            CERTIFICATE_SIZE = (960, 540)
            AVATAR_SIZE = (241, 241)
            RANK_SIZE = (233, 232)
            BACKGROUD_PATH = os.path.join(settings.BASE_DIR, 'storage', 'background', 'background.png')
            FONT_PATH = os.path.join(settings.BASE_DIR, 'storage', 'font', 'inter_24pt-Regular.ttf')

            try:
                profile = ProfileModel.objects.get(id=pk)
                user = profile.user
            except ProfileModel.DoesNotExist:
                return Response({'error': 'Profile not found'}, status.HTTP_404_NOT_FOUND)

            if not os.path.exists(BACKGROUD_PATH):
                return Response({'error': 'Background image not found'}, status.HTTP_404_NOT_FOUND)
            background = Image.open(BACKGROUD_PATH).convert('RGBA')
            background = background.resize(CERTIFICATE_SIZE, Image.Resampling.LANCZOS)

            avatar_path = os.path.join(settings.BASE_DIR, 'storage', user.avatar.path)
            if not os.path.exists(avatar_path):
                return Response({'error': 'Avatar image not found'}, status.HTTP_404_NOT_FOUND)
            avatar = Image.open(avatar_path).convert('RGBA')

            rank_path = os.path.join(settings.BASE_DIR, 'storage', user.rank.image.path)
            if not os.path.exists(rank_path):
                return Response({'error': 'Rank image not found'}, status.HTTP_404_NOT_FOUND)

            if rank_path.endswith('.svg'):
                rank = self.svg_to_png(rank_path)
            else:
                rank = Image.open(rank_path).convert('RGBA')

            rounded_avatar = self.create_rounded_avatar(avatar, AVATAR_SIZE)

            rank = rank.resize(RANK_SIZE, Image.Resampling.LANCZOS)

            certificate = Image.new('RGBA', CERTIFICATE_SIZE, (0,0,0,0))
            certificate.paste(background, (0, 0))

            avatar_pos = (168, 113)
            certificate.paste(rounded_avatar, avatar_pos, rounded_avatar)

            rank_pos = (563,134)
            certificate.paste(rank, rank_pos, rank)

            draw = ImageDraw.Draw(certificate)

            try:
                font = ImageFont.truetype(FONT_PATH, 22)
            except Exception as e:
                return Response({'error': f'Font loading failed: {str(e)}'}, status.HTTP_404_NOT_FOUND)

            user_text = f'{user.name} {user.surname}'
            user_bbox = draw.textbbox((0, 0), user_text, font=font)
            user_text_width = user_bbox[2] - user_bbox[0]
            user_pos = ((avatar_pos[0]+(AVATAR_SIZE[0] - user_text_width) // 2), avatar_pos[1] + AVATAR_SIZE[1] + 70)
            draw.text(user_pos, user_text, fill='#FFF', font=font)

            rank_name = user.rank.rank_name
            result = rank_name.replace('_', '.') if '_' in rank_name else rank_name
            rank_text = f'RANK STAR {result}'
            rank_bbox = draw.textbbox((0, 0), rank_text, font=font)
            rank_text_width = rank_bbox[2] - rank_bbox[0]
            rank_pos = ((rank_pos[0] + (RANK_SIZE[0] - rank_text_width) // 2), rank_pos[1] + RANK_SIZE[1] + 14)
            draw.text(rank_pos, rank_text, fill='#FFDF65', font=font)

            buffer = io.BytesIO()
            certificate.save(buffer, format='PNG')
            buffer.seek(0)

            return FileResponse(buffer, as_attachment=True, filename=f'certificate_{pk}.png', content_type='image/png')
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
