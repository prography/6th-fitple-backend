## User 관련 API 문서

##### 목차

- [회원가입 API](####회원가입 API)
- [로그인 API](####로그인 API)
- [이메일 중복 확인 API](####이메일 중복 확인 API)
- [프로필 READ/Update API](####프로필 READ/Update API)
- [프로필 read(인증 불필요)](####프로필 read(인증 불필요))
- [프로필 application list](####프로필 application list)



**임시 BaseUrl: http://fitple-deploy-dev.ap-northeast-2.elasticbeanstalk.com/**

---



#### 회원가입 API

- account/user/create/

- ###### POST

- ###### request 

  - ```
    email 
    username 
    password 
    ```

- ###### response

  - 성공하면

  - ```
    {"message": "ok"}
    ```

  - 이메일 중복되면

  - ```
    {"message": "duplicate email"}
    ```



#### 로그인 API

- account/user/login/

- ###### POST

- ###### request

  - ```
    email
    password
    ```

- ###### response

  - 성공하면
  
  - ```json
    {
        'success': 'True',
        'username': "김시현",
        'token': "토큰"
    }
    ```
    
  - 이메일 또는 패스워드 틀렸을 경우
  
  - ``` json
    {
        "message": "fail"
    }
    ```
  
  - request data error
  
  - ```json
    {"message": "Request Body Error."}
    ```



#### 가입 유무 확인 API

- account/user/check/

- ###### POST

- ###### request

  - ```
    email
    ```

- ###### response

  - email 이미 있으면

  - ```json
    {
      "message": "login",
      "email": email
}
    // 다음 순서는 로그인
    ```
  ```
    
  - 없는 email 이면
  
  - ```json
    {
      "message": "register",
    	"email": email
    }
    // 다음 순서는 회원가입
  ```



#### 프로필 READ/Update API

- account/profile/ -- Token 필요한 API

- ###### GET

  - ###### response

  - ```json
    {
        "success": "True",
        "profile": {
            "username": "lemontech",
            "livingArea": null,
            "phone": null,
            "email": "lemontech119@gmail.com",
            "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/public/default_user.png"
        },
        "myTeam": [
            {
                "id": 3,
                "title": "팀리더 팀생성 테스트 final",
                "image": "default_team.jpg"
            }
        ]
    }
    ```
  
- ###### PUT

  - ###### request
  
  - ```
    username
    livingArea
    phone
    email
    ```
  ```
  
  - ###### response
  
  - request data error
  
  - ```json
    {"message": "Request Body Error."}
  ```
  
  - 성공하면
  
  - ```
    {"message": "ok."}
    ```



#### 프로필 application list

- account/profile/application/ -- Token 필요한 API

- GET

  - response

  ``` json
  {
      "myApplication": [
          {
              "id": 29,
              "team_id": 52,
              "title": "팀리더 팀생성 테스트 final2",
              "description": "팀리더 팀생성 테스트",
              "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/default_team.jpg",
              "join_status": "Waiting",
              "job": "Developer"
          }
      ]
  }
  ```

  

#### 프로필 read(인증 불필요)

- account/user/profile/{user_pk}/

- GET

  - response

  ``` json
  {
      "id": 13,
      "user_id": 13,
      "livingArea": null,
      "phone": null,
      "image": "https://fitple-access-s3-test.s3-ap-northeast-2.amazonaws.com/media/default_user.png",
      "username": "ado119"
  }
  ```

  



