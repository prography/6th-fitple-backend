## Team 관련 API 문서

-------

#### API 리스트(해당 위치로 이동 하려면 Ctrl 누른 상태에서 클릭해주세요)

[Team 생성](####Team 생성)

[Team List 조회](####Team List 조회)

[Team Detail 조회](####Team Detail 조회)



--------

#### Team 생성

- 설명: Team create API입니다. 

- 요청 URL

  - Test URL: http://fitple-last-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
  - 서비스 URL: 추후 추가 

- HTTP 메서드: POST

- 요청 Headers

  ``` json
  {
  		Authorization: `Bearer ${token}`
  }
  ```

- 요청 Body

  ``` json
  {
      "title": "",
      "description": "",
      "status": "",
      "planner": ${number},
      "developer": ${number},
      "designer": ${number},
      "region": "",
      "goal": "",
      "kind": "",
      "people": "",
      "image": 이미지(default 가능),
  }
  ```

- 응답: 응답에 성공하면 결과값을 JSON 형식으로 반환합니다.

| 속성        | 타입   | 설명                 |
| ----------- | ------ | -------------------- |
| author      | string | 작성자 email         |
| id          | number | Team 신청 PK         |
| title       | string | 제목                 |
| description | string | 설명                 |
| status      | string | 상태                 |
| planner     | number | 기획자 인원          |
| developer   | number | 개발자 인원          |
| designer    | number | 디자이너 인원        |
| region      | string | 지역                 |
| goal        | string | 목표                 |
| kind        | string | 종류 ex) 웹, 앱      |
| people      | string | 사용고객             |
| image       | string | 프로젝트 이미지(url) |
| created_at  | string | 작성시간             |
| modified_at | string | 수정시간             |

**응답예시**

- 요청 URL 

  ``` 
  http://fitple-last-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
  ```

- 요청 Body

  ``` json
  {
      "title": "test1",
      "description": "testtest",
      "status": "delay",
      "planner": 1,
      "developer": 1,
      "designer": 1,
      "region": "서",
      "goal": "test",
      "kind": "웹",
      "people": "test",
  }
  ```

- 요청 Headers

  ``` json
  {
    Authorization: `Bearer ${token}`
  }
  ```

- 응답 성공

  ``` json
  {
      "author": "dobby1@naver.com",
      "id": 17,
      "title": "test1",
      "description": "testtest",
      "status": "delay",
      "planner": 1,
      "developer": 1,
      "designer": 1,
      "region": "서",
      "goal": "test",
      "kind": "웹",
      "people": "test",
      "image": "http://localhost:8000/media/default.jpg",
      "created_at": "2020-05-22T13:44:18.477133+09:00",
      "modified_at": "2020-05-22T13:44:18.477168+09:00"
  }
  ```

- 응답 실패시

  ``` json
  {
      "message": "Request Body Error."
  }
  ```

  

-----------



#### Team list 조회

- 설명: Team list 조회 입니다. (일단 임의로 pagenation은 10개씩 진행했습니다.)

- 요청 URL

  - Test URL: http://fitple-last-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
  - 서비스 URL: 추후 추가

- HTTP 메서드: GET

- 응답: 응답에 성공하면 Team list를 Json 형태로 반환

  | 속성               | 타입           | 설명                       |
  | ------------------ | -------------- | -------------------------- |
  | count              | number         | 전체 글 수                 |
  | next               | string or null | 다음 페이지 없을 경우 null |
  | previous           | string or null | 전 페이지 없을 경우 null   |
  | result             | json           | team 정보들                |
  | result.author      | string         | 작성자 email               |
  | result.id          | number         | 작성 글 PK                 |
  | result.title       | string         | 제목                       |
  | result.description | string         | 설명                       |
  | result.image       | string         | 이미지 URL                 |

**응답예시**

-  요청 URL

```
http://fitple-last-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
```

- 응답

``` json
{
    "count": 18,
    "next": "http://localhost:8000/teams/?page=2",
    "previous": null,
    "results": [
        {
            "author": "dobby1@naver.com",
            "id": 18,
            "title": "test1",
            "description": "testtest",
            "image": "http://localhost:8000/media/default.jpg"
        },
        {
            "author": "dobby1@naver.com",
            "id": 17,
            "title": "test1",
            "description": "testtest",
            "image": "http://localhost:8000/media/default.jpg"
        },
        {
            "author": "dobby1@naver.com",
            "id": 16,
            "title": "test1",
            "description": "testtest",
            "image": "http://localhost:8000/media/default.jpg"
        },
        {
            "author": "dobby1@naver.com",
            "id": 15,
            "title": "test1",
            "description": "testtest",
            "image": "http://localhost:8000/media/team/image/2020/05/05/21/20/saemi1.jpeg"
        }
        ...
    ]
}
```



------



#### Team Detail 조회

- 설명: Team detail 조회입니다. (comment는 추후 추가)

- 요청 URL

  - Test URL: http://fitple-last-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/:id/
  - 서비스 URL: 추후 추가

- HTTP 메서드: GET

- 응답: 응답에 성공하면 Team detail 결과 값을 Json 형식으로 반환합니다.

  | 속성        | 타입   | 설명                 |
  | ----------- | ------ | -------------------- |
  | author      | string | 작성자 email         |
  | id          | number | Team 신청 PK         |
  | title       | string | 제목                 |
  | description | string | 설명                 |
  | status      | string | 상태                 |
  | planner     | number | 기획자 인원          |
  | developer   | number | 개발자 인원          |
  | designer    | number | 디자이너 인원        |
  | region      | string | 지역                 |
  | goal        | string | 목표                 |
  | kind        | string | 종류 ex) 웹, 앱      |
  | people      | string | 사용고객             |
  | image       | string | 프로젝트 이미지(url) |
  | created_at  | string | 작성시간             |
  | modified_at | string | 수정시간             |

**응답예시**

- 요청 URL

  ``` 
  http://fitple-last-dev.ap-northeast-2.elasticbeanstalk.com/teams/18/
  ```

- 응답

  ``` json
  {
      "author": "dobby1",
      "id": 1,
      "title": "Fitple 프로젝트 완성",
      "description": "Fitple test",
      "status": "delay",
      "planner": 1,
      "developer": 1,
      "designer": 1,
      "region": "서울",
      "goal": "test",
      "kind": "웹",
      "people": "test",
      "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/public/default_team.jpg",
      "created_at": "2020-05-31T19:34:50.519963+09:00",
      "modified_at": "2020-05-31T19:34:50.519990+09:00"
}
  ```
  
  

-------

