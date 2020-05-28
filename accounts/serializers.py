from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from .models import User, Profile

User = get_user_model()

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            type='i',
        )
        profile = Profile.objects.create(user=user) # 기본값으로 프로필 일단 생성 --
        user.set_password(validated_data['password'])

        user.save()
        profile.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


class ProfilePageSerializer(serializers.Serializer):
    # required=True
    username = serializers.CharField(required=True)
    livingArea = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    # 인스턴스에 대한 검증없이 생성자에서 바로 가져오는건가 ? ok
    # update 에 self.instance 그대로 전달하고 create 결과값으로 변경된다 !
    # create 관련 사항은 생성자에 instance=None 하고 save 호출만 안하면 괜찮을듯! oo
    def update(self, instance, validated_data): # 인스턴스가 하나는 아니지만 연관관계로 접근하기! User 기준!
        # 와이어 프레임 대로라면
        # User -- username, email 변경
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.profile.livingArea = validated_data.get('livingArea', instance.profile.livingArea)
        instance.profile.phone = validated_data.get('phone', instance.profile.phone)
        # Profile -- livingArea, phone 변경

        instance.save()
        instance.profile.save()
        return instance

    # def create(self, validated_data):
    #     pass
