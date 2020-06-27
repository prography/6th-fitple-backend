## Mac 기준 redis celery local test



- redis 설치

``` bash
$ brew update
$ brew install redis
## redis start
$ brew services start redis

## redis stop
$ brew services stop redis

## redis background service 
$ redis-server /usr/local/etc/redis.conf

## redis server test
$ redis-cli ping
```



- main project에 celery.py 파일 추가

``` python
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

if('DJANGO_SETTINGS_MODULE' in os.environ) and (os.environ["DJANGO_SETTINGS_MODULE"] == "config.settings.production"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery('config',backend='redis://', broker='redis://localhost:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
```



- __ init __.py 에 해당 내용 추가 (init _ 붙어있느넉ㅂ니다....)

``` python 
from __future__ import absolute_import
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ('celery_app',)
```



이제 각 프로젝트에서 celery로 비동기로 진행을 하려면 각 프로젝트에 task.py 파일을 만들고 아래 예시처럼 만들어주면 됩니다. (당연히 돌리고 싶은 코드는 각자 스타일에 맞춰서 작업하면 됩니다. 여기서는 email 전송 함수를 호출해줍니다.)

``` python
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from config.email import send_test_email


@shared_task
def def_email():
    send_test_email()
    return True
```

> 위의 코드처럼 작업을하는데 여기서 중요한건 비동기로 작업하고 싶은 함수 위에 @shared_task를 넣어줘야 합니다. 
>
> 추가적으로 이 함수를 비동기적으로 돌릴려면 def_email.delay() 이런식으로 호출해줘야 합니다. 



-------

- 작업 순서
  - Redis server를 가동합니다.
    -  redis-server /usr/local/etc/redis.conf
  - 터미널을 하나 더 켜서 celery worker를 작동시킵니다.
    - celery -A config worker -l info
  - python 서버를 작동하여 테스트를 합니다. (잘됐으면...)

