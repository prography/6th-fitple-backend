# 팀 신청 관련 api

#### 목차

- [신청 create api](##신청 create api)
- [신청 list api](##신청 list api)
- [신청 retrieve api](##신청 retrieve api)
- [신청 update api](##신청 update api)
- [신청 cancel api](##신청 cancel api)
- [신청 승인 api](##신청 승인 api)
- [신청 거절 api](##신청 거절 api)
- [질문 list](#### 질문 list)
- 



Base_Url: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/

---

## 신청 create api

- ##### url

  - ###### POST

  - http://127.0.0.1:8000/teams/board/{team_pk}/applications/

  - ##### 설명

    - 해당 팀에 이미 신청한 회원은 신청할 수 없도록 중복된 이메일 검사합니다.
    - 현재는 직무 선택만 가능합니다. 질문에 대한 대답 작성은 추후 추가하겠습니다.

  - permission : 인증한 회원

- ##### request

  - header -- token

  - ###### body

  - ```cmd
    job  # 직무 ('Developer', 'Planner', 'Designer') 중 택1
    ```

  - ```cmd
    {
        "team": {
        	"job": "Developer"
    	},
        "answers": [
          {
                "question": 7,
                "answer": "...대답1"
        	},
            {
                "question": 8,
                "answer": "...대답2"
        	},
            {
                "question": 9,
                "answer": "...대답3"
            }
        ]
    }
    ```
    
    

- ##### response

  - 해당 팀에 이미 지원했으면

  - ```cmd
    {"message": "Duplicated applicant's email."}
    ```

  - 성공

  - ```cmd
    {"message": "ok"}
    ```

## 신청 list api

- ##### url

  - ###### GET

  - http://127.0.0.1:8000/teams/board/{team_pk}/applications/

  - ##### 설명

    - 이 api 는 팀 리더가 마이페이지에서 본인이 생성한 Team list 를 먼저 보고 하나를 선택해서 해당 팀 내의 신청 list 를 받는 api 입니다.
    - 지원자가 신청 취소한 신청 내역은 가져오지 않습니다.

  - permission : 팀 리더

- ##### request

  - header -- token

- ##### response

  - 신청 내역이 없으면

  - ```cmd
    {"message": "No results."}
    ```

  - 팀 리더가 아니면

  - ```cmd
    {"message": "Request Permission Error."}
    ```

  - 성공

  - ```json
    {
        "team": 2, // 팀id
        "applications": [ // 신청 list
            {
                "id": 11, // 신청 id
                "applicant": { // 지원자 간단 정보
                    "id": 5, // 지원자 id
                    "username": "sisi-apply", // username
                    "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/default_user.png" // image
                },
                "join_status": "Waiting", // 신청 상태
                "job": "Planner", // 신청 직무
                "created_at": "2020-06-02" // 신청일
            }
        ]
    }
    ```

  

## 신청 retrieve api

- ##### url

  - ###### GET

  - http://127.0.0.1:8000/teams/board/{team_pk}/applications/{application_pk}

  - ##### 설명

    - 지원자가 신청 update 위해 화면에 뿌려줄 기존 데이터를 가져옵니다

  - permission : ~~인증한 회원~~  작성한 본인

- ##### request

  - header -- token

- ##### response

  - 본인이 아니면

  - ```json
    {"message": "Request Permission Error."}
    ```

  - 존재하지 않으면

  - ```cmd
    {"message": "Not Found."}
    ```

  - 성공

  - ```json
    {
        "application": {
            "id": 20,
            "applicant": {
                "id": 8,
                "username": "sisi-member",
                "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/default_user.png"
            },
            "join_status": "Waiting",
            "job": "Developer",
            "created_at": "2020-06-20"
        },
      "answer": [
            {
                "answer": "...대답1",
                "question": 7
            },
            {
                "answer": "...대답2",
                "question": 8
            }
        ]
    }
    ```
  
  

## 신청 update api

- ##### url

  - ###### PUT

  - http://127.0.0.1:8000/teams/board/{team_pk}/applications/{application_pk}

  - ##### 설명

    - 신청 정보 수정은 `지원상태`가 `대기중`일 때만 가능합니다.

  - permission :  ~~인증한 회원~~  작성한 본인

- ##### request

  - header -- token

  - ```cmd
    job  # 직무 ('Developer', 'Planner', 'Designer') 중 택1
    ```

  - ```json
    # 예시
    {
        "job": "Planner"
    }
    ```

- ##### response

  - 본인이 아니면

  - ```json
    {"message": "Request Permission Error."}
    ```

  - 존재하지 않으면

  - ```json
    {"message": "Not Found."}
    ```

  - `지원상태` 가 `대기중`일 때만 수정 가능 --  Waiting

    - `대기중`이 아니라면

    - ```json
      {"message": "Bad Request."}
      ```

  - 성공

  - ```json
    {"message": "ok"}
    ```

    

## 신청 cancel api

- ##### url

  - ###### DELETE

  - http://127.0.0.1:8000/teams/board/{team_pk}/applications/{application_pk}

  - ##### 설명

    - 지원자가 신청을 취소하는 api 입니다.

  - permission :  ~~인증한 회원~~  작성한 본인

- ##### request

  - header -- token

- ##### response

  - 본인이 아니면

  - ```json
    {"message": "Request Permission Error."}
    ```

  - 존재하지 않으면

  - ```json
    {"message": "Not Found."}
    ```

  - 성공

  - ```json
    {"message": "ok"}
    ```

    

## ap신청 승인 api

- ##### url

  - ###### GET

  - http://127.0.0.1:8000/applications/{application_pk}/approve/ 

  - ##### 설명

    - 팀 리더가 지원자를 승인하는 api 입니다.

  - permission : 팀 리더

- ##### request

  - header -- token

- ##### response

  - `지원상태:join_status`가 `대기중:Waiting`일 때만 승인 가능하다

    - 대기중이 아니면

    - ```json
      {"message": "Application Status Error."}
      ```

  - 성공

  - ```json
    {"message": "ok"}
    ```

    

## 신청 거절 api

- ##### url

  - ###### GET

  - http://127.0.0.1:8000/applications/{application_pk}/refuse/

  - ##### 설명

    - 팀 리더가 지원자를 거절하는 api 입니다.

  - permission : 팀 리더

- ##### request

  - header -- token

- ##### response
  - `지원상태:join_status`가 `대기중:Waiting`일 때만 거절 가능하다

    - 대기중이 아니면

    - ```json
      {"message": "Application Status Error."}
      ```

  - 성공

  - ```json
    {"message": "ok"}
    ```

    

#### 질문 list

- url

  - GET
  - http://127.0.0.1:8000/teams/board/{team_pk}/questions/
  - response

  ``` json
  [
      {
          "id": 7,
          "question": "시현질문11"
      },
      {
          "id": 8,
          "question": "시현질문22"
      },
      {
          "id": 9,
          "question": "시현질문33"
      }
  ]
  ```

  