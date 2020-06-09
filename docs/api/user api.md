## User 관련 API 문서

##### 목차

- [회원가입 API](####회원가입 API)
- [로그인 API](####로그인 API)
- [이메일 중복 확인 API](####이메일 중복 확인 API)
- [프로필 READ/Update API](####프로필 READ/Update API)



**임시 BaseUrl: http://fitple-dev.ap-northeast-2.elasticbeanstalk.com**

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
        'success': 'True',
        'username': '이름',
        'livingArea': '거주지',
        'phone': '폰번호',
        'email': '이메일'
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