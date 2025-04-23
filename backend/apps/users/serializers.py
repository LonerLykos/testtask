from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from rest_framework import serializers

from apps.users.models import RankModel, UserModel

ProfileModel = get_user_model()

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankModel
        fields = (
            'id',
            'rank_name',
            'image'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'id',
            'name',
            'surname',
            'rank',
            'avatar'
        )
        read_only_fields = ('rank',)

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'user',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'created_at', 'updated_at')


    @atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('rank', None)

        user = UserModel.objects.create(**user_data)

        password = validated_data.pop('password')
        profile = ProfileModel(**validated_data)
        profile.set_password(password)
        profile.user = user
        profile.save()

        return profile

class ChangeRankSerializer(serializers.Serializer):
    rank_id = serializers.IntegerField()

    def validate_rank_id(self, value):
        if not RankModel.objects.filter(id=value).exists():
            raise serializers.ValidationError('Such a rank does not exist')
        return value