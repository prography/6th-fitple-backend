## Team 관련 API 문서

-------

#### API 리스트(해당 위치로 이동 하려면 Ctrl 누른 상태에서 클릭해주세요)

[Team 생성](####Team 생성)

[Team List 조회](####Team List 조회)

[Team Detail 조회](####Team Detail 조회)

[Team Delete](####Team Delete)

[댓글 작성](#### 댓글 작성)

[댓글 view](#### 댓글 view)

--------

#### Team 생성

- 설명: Team create API입니다. 

- 요청 URL

  - Test URL: http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
  - 서비스 URL: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/

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
      "team": {
        "title": "팀리더 팀생성 테스트 final",
        "description": "팀리더 팀생성 테스트",
        "planner": 3,
        "developer": 3,
        "designer": 3,
        "region": "서울",
        "goal": "취직",
        "active_status": "모집진행중"
      },
  	"questions": [
          {"question": "시현질문11"},
          {"question": "시현질문22"},
          {"question": "시현질문33"}
      ]
  }
  ```

- 응답: 응답에 성공하면 결과값을 JSON 형식으로 반환합니다.

| 속성              | 타입   | 설명                 |
| ----------------- | ------ | -------------------- |
| board             | json   | 게시판 json 데이터   |
| board.author      | string | 작성자 email         |
| board.id          | number | Team 신청 PK         |
| board.title       | string | 제목                 |
| board.description | string | 설명                 |
| board.status      | string | 상태                 |
| board.planner     | number | 기획자 인원          |
| board.developer   | number | 개발자 인원          |
| board.designer    | number | 디자이너 인원        |
| board.region      | string | 지역                 |
| board.goal        | string | 목표                 |
| board.kind        | string | 종류 ex) 웹, 앱      |
| board.people      | string | 사용고객             |
| board.image       | string | 프로젝트 이미지(url) |
| board.created_at  | string | 작성시간             |
| board.modified_at | string | 수정시간             |
| author            | string | 작성자 username      |
| application       | json   | 빈 리스트            |

**응답예시**

- 요청 URL 

  ``` 
  http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
  ```

- 요청 Body

  ``` json
  {
      "team": {
  		"title": "팀리더 팀생성 테스트 final",
  		"description": "팀리더 팀생성 테스트",
  		"planner": 3,
  		"developer": 3,
  		"designer": 3,
  		"region": "서울",
  		"goal": "취직",
  		"active_status": "모집진행중"
      },
  	"questions": [
          {"question": "시현질문11"},
          {"question": "시현질문22"},
          {"question": "시현질문33"}
      ]
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
      "board": {
          "author": "ado119",
          "id": 27,
          "title": "팀리더 팀생성 테스트 final",
          "description": "팀리더 팀생성 테스트",
          "planner": 3,
          "developer": 3,
          "designer": 3,
          "region": "서울",
          "goal": "취직",
          "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/public/default_team.jpg",
          "created_at": "2020-06-22T21:46:30.544376+09:00",
          "modified_at": "2020-06-22T21:46:30.544418+09:00",
          "active_status": "모집진행중"
      },
      "author": {
          "id": 13,
          "username": "ado119",
          "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/public/default_user.png"
      },
      "application": false
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

  - Test URL: http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
  - 서비스 URL: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/

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
http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/
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

  - Test URL: http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/:id/
  - 서비스 URL: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/teams/board/:id/

- HTTP 메서드: GET

- 응답: 응답에 성공하면 Team detail 결과 값을 Json 형식으로 반환합니다.

  | 속성              | 타입   | 설명                 |
  | ----------------- | ------ | -------------------- |
  | board             | json   | 게시판 데이터        |
  | board.author      | string | 작성자 email         |
  | board.id          | number | Team 신청 PK         |
  | board.title       | string | 제목                 |
  | board.description | string | 설명                 |
  | board.status      | string | 상태                 |
  | board.planner     | number | 기획자 인원          |
  | board.developer   | number | 개발자 인원          |
  | board.designer    | number | 디자이너 인원        |
  | board.region      | string | 지역                 |
  | board.goal        | string | 목표                 |
  | board.kind        | string | 종류 ex) 웹, 앱      |
  | board.people      | string | 사용고객             |
  | board.image       | string | 프로젝트 이미지(url) |
  | board.created_at  | string | 작성시간             |
  | board.modified_at | string | 수정시간             |
  | author            | string | 게시글 작성자        |
  | application       | json   | 지원자 리스트        |

**응답예시**

- 요청 URL

  ``` 
  http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/18/
  ```

- 응답

  ``` json
  {
      "board": {
          "author": "고기훈",
          "id": 13,
          "title": "장고 스터디 구합니다.",
          "description": "프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명 프로젝트 설명...",
          "status": "delay",
          "planner": 1,
          "developer": 3,
          "designer": 2,
          "region": "0",
          "goal": "목표",
          "kind": "웹",
          "people": "사용고객",
          "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/public/default_team.jpg",
          "created_at": "2020-06-03T01:06:04.865469+09:00",
        "modified_at": "2020-06-03T01:06:04.865493+09:00"
      },
      "author": "고기훈",
      "application": [
          "sisi"
      ]
  }
  ```
  
  

-------

#### Team Delete

- 설명: Team 삭제 api
- 요청 URL
  - Test URL: localhost:8000/team/board/{id}/
  - 서비스 URL: http://api.fit-ple.com/team/board/{id}/
- HTTP 메서드: DELETE
- 요청 Headers

``` json
{
		Authorization: `Bearer ${token}`
}
```

- 응답(성공시)

``` json
{
    "message": "ok"
}
```

- 응답(실패시)

``` json
{
    "message": "Account mismatch"
}
```





#### 댓글 작성

- 설명: 댓글 작성 api 입니다.
- 요청 URL
  - Test URL: http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/comments/
  - 서비스 URL: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/teams/comments/
- HTTP 메서드: POST
- 요청 Headers

``` json
{
		Authorization: `Bearer ${token}`
}
```

- 요청 Body

  - 일반적인 댓글일 경우

  ``` json
  {
  	"team": 24, // team id 값
  	"comment": "test" // 댓글 내용
  }
  ```

  - 대댓글인 경우

  ``` json
  {
  	"team": 24, // team id 값
  	"parent":1, // 댓글 id 값
  	"comment": "test" // 대댓글 내용
  }
  ```

- 응답: 응답에 성공하면 응답 성공 json을 던져줌

| 속성    | 타입   | 설명                                       |
| ------- | ------ | ------------------------------------------ |
| team_id | Number | 해당 팀 id 값                              |
| message | String | 성공 시 ok 실패시 Request Body Error. 반환 |

**응답예시**

- 요청 URL 

  ``` 
  http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/comments/
  ```

- 요청 Body (일반적인 댓글)

  ``` json
  {
  	"team": 3,
  	"comment": "test3"
  }
  ```
  
- 요청 Body (대댓글)

  ``` json
  {
  	"team": 3,
  	"parent": 4, //해당 댓글 id 값은 댓글 view api를 통해 얻을 수 있어요
  	"comment": "test3"
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
      "team_id": 3,
      "message": "ok"
  }
  ```

- 응답 싪패 시 

  ``` json
  {
    "message": "Request Body Error."
  }
  ```

-----



#### 댓글 view

- 설명: 해당 게시글의 댓글 view
- 요청 URL
  - Test URL: http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/comment/${id}/
  - 서비스 URL: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/teams/comment/${id}/
- HTTP 메서드: GET
- 응답: 응답에 성공하면 댓글 data를 json 형태로 반환

| 속성                       | 타입    | 설명                                    |
| -------------------------- | ------- | --------------------------------------- |
| id                         | Number  | 팀 id값                                 |
| parent_comments            | Json    | 댓글 전체 값                            |
| parent_comments.team       | Number  | 팀 id값                                 |
| parent_comments.id         | Number  | 댓글 id 값                              |
| parent_comments.user       | String  | 댓글 작성자                             |
| parent_comments.comment    | String  | 댓글 내용                               |
| parent_comments.created_at | String  | 댓글 작성 시간                          |
| parent_comments.is_deleted | boolean | 댓글 삭제관련(추후 재 정의)             |
| parent_comments.reply      | Json    | 해당 댓글 대댓글(대댓이 없으면 빈 배열) |

**응답예시**

- 요청 URL

``` 
http://fitple-dev.ap-northeast-2.elasticbeanstalk.com/teams/comment/24/
```

- 응답

``` json
{
    "id": 24,
    "parent_comments": [
        {
            "team": 24,
            "id": 1,
            "user": "dobby1",
            "parent": null,
            "comment": "test",
            "created_at": "2020-06-09T11:43:50.273820+09:00",
            "is_deleted": true,
            "reply": [
                {
                    "team": 24,
                    "id": 3,
                    "user": "dobby1",
                    "parent": 1,
                    "comment": "test",
                    "created_at": "2020-06-09T12:07:45.613279+09:00",
                    "is_deleted": true,
                    "reply": []
                }
            ]
        },
        {
            "team": 24,
            "id": 2,
            "user": "dobby1",
            "parent": null,
            "comment": "test",
            "created_at": "2020-06-09T12:06:35.595558+09:00",
            "is_deleted": true,
            "reply": []
        }
    ]
}
```

