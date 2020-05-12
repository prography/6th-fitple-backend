## Fitple Backend

일단 기본 세팅 같은 경우는 우리의 멘토 백경준님의 django-starter를 활용했습니다.

[django-service-starter](https://github.com/paikend/Django-service-starter)

``` bash
$ git clone https://github.com/paikend/Django-service-starter
$ cd Django-service-starter
## 이걸 수정해서 우리 프로젝트에 활용해야 되니깐 .git 파일 제거(허락 받음)
$ rm -rf .git 

## 가상환경 세팅 
$ python3 -m venv django_py38
$ source django_py38/bin/activate
```

- env 디렉토리에 root에 추가

``` bash
## 써야되는 라이브러리 받아오기 
## (다만 버전 지정이 안되어 있기 때문에 최신버전이 받아와짐 -> 세팅 완료 후 수정 필요)
## 안그러면 추후 고생할 것이 너무나도 뻔히 보임(무섭...)
$ pip install -r env/development.txt
```

해당 프로젝트의 setting app은 config 입니다. 

``` bash
## 어드민 페이지를 위해 임시로 static 디렉토리 생성
$ mkdir config/static
```

**기본 세팅에서 사용하지 않을 내용을 주석 처리 해줍니다.** 

config/setting/development.py

``` python
#with open('env/etc/email.txt') as email:
#    EMAIL_HOST_USER = email.readline().strip()
#    EMAIL_HOST_PASSWORD = email.readline().strip()
```

DB 정보를 해당 문서에 update 해줍니다. 
env/etc/db.txt 

```
fitpletest
root
admin12345
127.0.0.1
5432
```



------------

#### accounts 작업 진행 (user관련)

accounts/models.py의 User 클래스 수정

``` python
# User 클래스를 자신의 프로젝트에 맞춰서 수정
# 필자는 여기서 아래 내용만 추가
username = models.CharField(
        max_length=7,
    )
```

> 해당 customs user model은 email을 username filed로 선언되어 있습니다. 

#### 회원가입 API 작업

serializers.py 와 urls.py 파일을 만들어 줍니다.

``` bash
touch accounts/serializers.py
touch accounts/urls.py
```

serializers.py에 해당 내용을 작성합니다.

``` python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


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
        user.set_password(validated_data['password'])

        user.save()
        return user

```

accounts/views.py를 수정해줍니다. 

``` python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserCreateSerializer
from .models import User


@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return

        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)
```

accounts/urls.py 추가

``` python
from django.urls import path
from . import views

urlpatterns = [
    path('user/create/', views.createUser),
]

```

config/urls.py 추가 

``` python
urlpatterns = [
	path('account/', include('accounts.urls')),  
]
```

**postman 등 api 테스트 도구를 활용하여 테스트 진행**
(됐으면 좋겠다...)

------

#### 로그인 API 작업

해당 프로젝트에서 jwt를 활용할 예정이므로 setting update 필요
config/settings/base.py 아래 내용으로 수정 그 외에 필요한 세팅은 되어 있습니다. 

``` python
# djangorestframework-jwt
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': 'SECRET_KEY',
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}
```

accounts/serializers.py 수정

``` python
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


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
```

accounts/views.py update

``` python
from .serializers import UserCreateSerializer, UserLoginSerializer


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return
        query = User.objects.filter(email=serializer.validated_data['email']).values()[0]
        username = query['username']

        response = {
            'success': 'True',
            'username': username,
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)
```

accounts/urls.py update

``` python
urlpatterns = [
    path('user/login/', views.login),
]
```

이제 로그인 테스트를 진행하면 됩니다...

----------

#### 가입된 이메일 체크

accounts/views.py

``` python
@api_view(['POST'])
def userCheck(request):
    if request.method == 'POST':
        email = request.data['email']

        if User.objects.filter(email=email).first() is None:
            return Response({"message": "register"}, status=status.HTTP_200_OK)
        return Response({"message": "login"}, status=status.HTTP_200_OK)
```

accounts/urls.py

```python
urlpatterns = [
    path('user/check/', views.userCheck)
]
```