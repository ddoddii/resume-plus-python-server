# Chat Your Interview 회고

[GDSC](https://gdsc-ys.github.io/) ML 파트원, 프런트 [@수빈](https://github.com/suekim3028), 백엔드 [@인엽](https://github.com/inshining) 함께 CV 기반 개인 질문을 생성해주고, 챗봇 형태로 대화할 수 있는 `Chat Your Interview` 프로젝트를 진행했다. 

프로젝트를 통해 Github-actions, docker, AWS EC2 를 찐하게 다루어볼 수 있었다. 우선 이 포스팅에서는 어떤 기술을 선택했는지, DB 스키마 설계, API 설계에 대해 다루어보고자 한다. 

프로젝트 스택은 다음과 같다. 

- Backend Framework : FastAPI
- Frontend Framework : React
- Server : AWS EC2 
- Database : SQlite

**[FastAPI 선택 이유]**

CV 기반 개인 질문을 생성할 때, OpenAI API 를 사용했다. ML 파트원들이 우선 이 코드를 짜고 나에게 넘겨주었다. 이 코드가 우선 python 으로 되어 있어서, ML 파트원도 혹시 백엔드 로직을 수정할 때 번거롭지 않게끔 python 백엔드 프레임워크 를 선택했다.

그 중에서도 **FastAPI** 는 작은 프로젝트에 적합하고, Django 의 강력한 Authentication 기능은 over-engineering 이라고 생각했다. 백과 프런트를 처음 만든 시점(11/17) 2주 후가 데모데이(12/4) 였기 때문에, 2주 안에 적당한 성능을 가진 완성본을 뽑아낼 수 있는 프레임워크로는 FastAPI 가 적합하다고 생각했다. 

또, FastAPI 는 OpenAPI standard 에 따른 문서를 자동으로 생성해주기 때문에, 프런트와 협업하기도 수월했다. 


**[SQLite 선택 이유]**

SQLite 는 정말 가벼운 데이터베이스이다. MySQL 은 클라이언트-서버 기반 관계형 DB 인데 비해서, SQLite 는 serverless rdb 이다. SQLite 자체 포함형(embedded)인데, 외부 서버가 필요 없다. 서버와 연결할 필요 없이, 파일 하나로 관리 가능하다. 

SQLite 는 경량 어플리케이션, 개발 및 테스트 목적에 적합하다. 적은 사용자가 있는 서비스에 적합하다. 따로 설치할 필요가 없으며, 파일 기반의 데이터베이스이므로 어플리케이션과 함께 배포될 수 있다. 이것은 AWS EC2 를 사용해서 배포했을 때 DB 복사가 간편하다는 장점으로 다가왔다. 

그렇지만 SQLite 는 단점도 많다. 내장 보안 기능이 제한적이고, 대용량 데이터와 높은 사용자 부하를 견디기 어렵다.  따라서 실 사용자가 많아지면 MySQL 로 마이그레이션을 진행할 생각을 가지고 있다. 

## 사용자 Flow

사용자의 flow 를 우선 정리했다. API 의 실행 속도는 우리가 제어할 수 없는 외부 변수이므로, 사용자가 API 응답 시간을 느끼지 못하게끔 어플리케이션의 흐름을 짰다. 

<img width="556" alt="image" src="https://github.com/ddoddii/resume-ai-chat/assets/95014836/b985ed50-0a9d-4d03-bb92-82ce9e8afbe4">

처음 사용자가 들어오면, (username, name, password, email) 을 입력하고 회원가입을 한다. 그 후 사용자의 CV(Curriculum Vitae) 를 pdf 형태로 업로드 한다. pdf 형태에서 text 를 추출하는 것은 프런트에서 react 내장 라이브러리로 해결했다. 

그 후 본인이 지원하는 포지션 (AI/BE/FE/Mobile) 를 선택한다. ML 파트에서 각 포지션에 맞는 질문들과 예시 답안을 파트별로 거의 900개 씩 총 3600개의 질문들을 준비해주었다. 각 파트별 예시 질문으로는 아래가 있다. 따라서 사용자가 기술 질문에 대한 답변을 할 때도, 예시 답변을 바탕으로 사용자가 입력한 대답을 평가해준다. 

```csv
position,question,topic,example_answer
be,Compare Relational DB (SQL) vs NoSQL. It's also really nice to know about newSQL (a kind of auto sharding DB which support SQL stuff but scale like NoSQL),database,"Relational DB is organized by schema, table. All records in a table must be in the same structure, follow some constraints. Relational DB guarantees ACID characteristics so it is safe and stable.NoSQL is something that is not relational DB. Currently, it contains 4 main kinds:- The first kind is Document. In this kind, each piece of data is a JSON document.- The second is Key-Value DB. Simply, it is like a hash map that maps one key to one value.- The third is Wide Column DB. Records in a table can have a different number of columns.- The last one is Graph which is suitable for some graph-like data, for example, connections of people on a social network."
fe,Explain how a browser determines what elements match a CSS selector.,CSS,"This part is related to the above about [writing efficient CSS](#what-are-some-of-the-gotchas-for-writing-efficient-css). Browsers match selectors from rightmost (key selector) to left. Browsers filter out elements in the DOM according to the key selector and traverse up its parent elements to determine matches. The shorter the length of the selector chain, the faster the browser can determine if that element matches the selector.  
 For example with this selector `p span`, browsers firstly find all the `<span>` elements and traverse up its parent all the way up to the root to find the `<p>` element. For a particular `<span>`, as soon as it finds a `<p>`, it knows that the `<span>` matches and can stop its matching.  
 "
 ai,Why is naive Bayes so ‘naive’ ?,Naive Bayes,"naive Bayes is so ‘naive’ because it assumes that all of the features in a data set are equally important and independent. As we know, these assumption are rarely true in real world scenario."
 mobile,What is Flutter?,Flutter,"Flutter is an open-source UI toolkit from Google for crafting beautiful, natively compiled applications for desktop, web, and mobile from a single codebase. Flutter apps are built using the Dart programming language."
```
 
인성 면접을 위한 질문들도 준비했다.  Behav-Q 라고 이름 지었는데, 총 30문제 정도 준비했다. 

```csv
Recall a time when you were assigned a task outside of your job description. How did you handle the situation? What was the outcome?,adaptability
```


## Database 설계

<img width="700" alt="image" src="https://github.com/ddoddii/resume-ai-chat/assets/95014836/6321c4b5-edfe-4020-9cee-0cad9bcb42ed">

DB 설계는 위와 같이 했다. OpenAI API 를 사용하므로 과도하게 사용하지 않도록 사용자 당 세션 5회로 제한했다.  하나의 세션은 (기술 질문 답변 -  인성 질문 답변 - CV 기반 개인 질문 답변 - 평가 보기) 로 이루어진다. 

세션(session) 테이블에는 기반이 되는 CV id, 사용자 id, 상호작용 id를 FK 로 저장하고, 사용자의 답변에 대한 평가도 저장했다. 상호작용(interaction) 테이블에는 그 세션에서 물어본 질문 id (기술질문, 인성질문, 개인질문) 와 사용자의 답변을 저장했다. 


## API 설계

### 로그인



```python
class Token(BaseModel):  
    access_token: str  
    token_type: str

@router.post("/login", response_model=Token)  
async def login_for_access_token(  
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency  
) -> dict:  
    user = await authenticate_user(form_data.username, form_data.password, db)  
    if not user:  
        raise HTTPException(  
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"  
        )  
    token = create_access_token(user.username, user.id, timedelta(minutes=60))  
  
    return {  
        "access_token": token,  
        "token_type": "bearer",  
    }
    
async def authenticate_user(username: str, password: str, db):  
    user = db.query(Users).filter(Users.username == username).first()  
    if not user:  
        return False    
	if not bcrypt_context.verify(password, user.hashed_password):  
        return False    
    return user
    
def create_access_token(username: str, user_id: int, expires_data: timedelta):  
    encode = {"sub": username, "id": user_id}  
    expire = datetime.utcnow() + expires_data  
    encode.update({"exp": expire})  
    return jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
```


사용자가 회원가입을 하면, (username, name, email, password) 를 입력 받도록 했다. 패스워드는  `bcrypt_context.hash()` 를 이용해서 해싱해서 데이터베이스에 저장했다.  로그인 함수는 아래와 같이 구현했다. `pydantic` 라이브러리를 이용해서 Token 클래스를 미리 만들어두고, 리턴값이 Token 이라는 것을 명시했다. 

#### 비동기 함수

`async` 를 사용해서 `login_for_access_token` 함수를 코루틴으로 선언했다. 이렇게 한 이유에 대해 실생활에서 일어날 법한 상황을 예시로 들어 살펴보자. 

만약 대기업 채용 공고가 떠서 여러 명의 사람들이 한꺼번에 로그인 요청을 한다고 하자. 내 로그인 프로세스는 `authenticate_user` 함수에서 DB 를 호출하고 사용자가 입력한 패스워드를 확인하는 작업을 거친다.  

전통적인 **동기 방식(synchronous)** 에서는 여러 명의 요청이 어떻게 이루어지는지 보자. 각 로그인 요청은 하나씩 처리한다. 서버가 데이터베이스의 응답을 기다리는 동안, 다른 작업을 할 수 없다. 이것은 병목 현상을 야기할 수 있다. 뒤에 요청한 사용자들은 많은 시간을 기다려야 할 것이다. 

**비동기 방식(Asynchronous)**  에서는 어떻게 여러 명의 요청을 처리할까? 사용자가 로그인을 하면, 서버는 요청을 처리하기 시작한다. 하지만 데이터베이스의 요청을 처리하는 와중이나 다른 외부 서비스를 대기하는 도중에 서버는 idle 하게 기다리지 않는다. 대신, 요청을 처리하는 함수는 멈춰지고(`await`), 다른 요청들을 처리한다. 데이터베이스 응답이나 외부의 서비스가 응답하면, 서버는 원래 요청으로 돌아간다. 

위의 함수에서는, 데이터베이스에 요청을 보내는 `authenticate_user` 를 await 하게 했다. 따라서 요청량이 많아지면 이 응답을 기다리는 동안 서버는 다른 로그인 요청을 처리할 수 있다.  

여기서 DB의 연산이 non-blocking 인지 blocking 인지도 확인해야 한다. 비동기 컨텍스트에서 DB 연산이 수행될 때는, 이 연산들이 **non-blocking** 이어야 한다. 만약 비동기 + blocking 연산이면, 최약의 결과가 된다. `login_for_access_token` 가 호출한 함수(B) 의 작업 결과와 순서에 관심이 없음에도 B가 blocking 연산이므로 제어권을 가져간다. 그래서 `login_for_access_token` 는 다른 요청을 처리하지 못하고 B의 작업이 끝날 때까지 대기한다.  SQLite `aiosqlite` 와 같은 라이브러리를 사용해서 non-blocking 이 되게끔 해야 한다. 

### OpenAI API 호출

openAI API 를 호출할 때도 비동기 방식을 적용했다. 비동기 방식이 많이 나오는데, python 에서 Async 를 사용한 방법은 아래 글에 자세하게 정리해보았다. 

{{< article link="/post/cs/python/python-asyncio/" >}}


한 번 CV 기반 개인 질문을 생성할 때 5개 생성하도록 했다. 이때 API 호출 속도를 테스트 하기 위해 로컬 환경에서 실험해보았다. 외부 API 를 호출하는 거라 호출할 때마다 차이가 났다. 최단 시간은 23초, 오래 걸릴 때는 44초 등 차이가 많이 났다. 

<img width="520" alt="스크린샷 2024-01-04 오후 10 24 27" src="https://github.com/ddoddii/resume-ai-chat/assets/95014836/af6d1831-17a2-444f-a5d6-5e9cb8b05387">

<img width="592" alt="스크린샷 2024-01-04 오후 3 09 29" src="https://github.com/ddoddii/resume-ai-chat/assets/95014836/09db9299-1029-44c8-a508-bb2e92c8b123">

OpenAI API 하나에만 의존하는 상황은 위험하다고 판단해서, OpenAI API 응답시간을 모니터링 하고 응답시간이 너무 길어지면 다른 모델 / API 로 redirect 하는 방법도 구축하려고 계획하고 있다. 

## Dockerize 하기 

우선 프런트 멤버와 나 모두 친숙한 AWS EC2 를 사용해서 배포하기로 결정했다. 데모데이 때 시현할 때는 그냥 github 에 push 에서 이 레포를 EC2 instance 내에서 pull 해오고, 인스턴스 내에서 uvicorn 을 실행하는 식으로 했다.  공개해서는 절대 안되는 OpenAI API key 도 공개되어 있고 난장판이었다. 시간이 촉박해서 이렇게 했는데, 방학 때 다시 리팩토링 하기로 결정했다. 

따라서 기말이 모두 끝나고 12월  ~ 1월 초에 걸친 리팩토링 과정에서  [@인엽](<[@인엽](https://github.com/inshining)>) 과 같이 환경변수 설정 & 도커화 & 배포 자동화 하는 작업을 했다. 

우선 Docker file 을 작성했다. 

```dockerfile
FROM python:3.10  
  
WORKDIR /app/  
  
COPY . /app/  
COPY ./requirements.txt /app/  
  
RUN pip install -r requirements.txt  
  
VOLUME /app/resume-db  
  
CMD ["uvicorn", "--host=0.0.0.0", "--port", "8000", "main:app"]
```

#### Volume 을 활용해서 데이터 보존하기

여기서 **Volume** 이 중요한 역할을 했다. Volume 없이 도커 이미지를 빌드 후 dockerhub로 push 하고 ec2 인스턴스 에서 그 이미지를 pull 하고 컨테이너를 실행했을 때는, 컨테이너를 중지 / 삭제 하면 그 세션에서 받은 데이터는 삭제된다는 엄청나게 큰 문제가 있었다. 

그래서 도커에서 데이터를 관리하는 방법에 대해 공부했다.  자세한 내용은 아래 포스팅에 있다. 

{{< article link="/post/cs/docker/docker-data-and-volumes/" >}}

우선 SQLite 로 DB 를 정했으므로, 파일 하나로 관리되었다. 따라서 모든 기술 질문, 인성 질문들이 들어있는 DB 파일을 `scp` 를 이용해서 ec2 instance 로 복사했다.

![image](https://github.com/ddoddii/resume-ai-chat/assets/95014836/645e345b-26ea-4c3b-baa6-214c147bf963)

따라서 내 ec2 instance 에도 db 가 생겼다. 

![image](https://github.com/ddoddii/resume-ai-chat/assets/95014836/e4bf7049-9808-45c5-8b63-06ce7ccd3846)

docker run 을 할 때, -v 를 사용해서 컨테이너 실행 시 발생한 데이터를 이 db 에 저장할 수 있도록 매핑 해주었다. (`docker run -v /home/ubuntu/resume_ai_chat.db:/app/resume_ai_chat.db -d soeunuhm/resume-ai-chat`)

## 환경 변수 설정

OpenAI API Key, SQLite db 정보, 해싱 알고리즘 등을 로컬의 .env 파이에 넣어두고 관리했었다. 하지만 도커화 후, ec2 인스턴스에서 컨테이너를 실행했을 때 어떻게 환경변수를 설정할지가 문제였다. 구글링 결과, ec2 인스턴스에 환경 변수 파일을 만들고, docker run 할 때 `--env-file` 로 설정해주었다. 

처음에는 ec2 인스턴스에 .env 이름으로 파일을 만들었는데, hidden file 이라 그런지 인식을 못했다. 따라서 my-env 이름으로 파일을 만들었다. 

또한 ubuntu 에서는 "" 까지 모두 인식했다. 예를 들어, 원래 .env 파일에서는 
```
ALGORITHM = "HS256"
```

이렇게 되어있었는데 계속 아래와 같이 "HS256" 을 인식하지 못한다는 에러가 났다. 

![image](https://github.com/ddoddii/resume-ai-chat/assets/95014836/65ca211e-d2ed-4c00-be3c-9dedb0ef991f)

따라서 "" 를 모두 지우고, 아래와 같이 수정해주었더니 잘 작동했다. 

```
ALGORITHM=HS256
```


## Github actions 를 사용한 배포 자동화

로컬에서 코드를 수정할 때마다 매번 다시 이미지 빌드하고, push 하고, ec2 에서 컨테이너 중지하고 다시 pull 하는 것이 너무 번거로워서 Github actions , Github secrets 를 이용한 배포 자동화 스크립트를 만들었다. 

```yaml
name: ci  
  
on:  
  push:  
    branches:  
      - "main"  
  
jobs:  
  build:  
    runs-on: ubuntu-latest  
    steps:  
      -        name: Checkout  
        uses: actions/checkout@v4  
      -  
        name: Login to Docker Hub  
        uses: docker/login-action@v3  
        with:  
          username: ${{ secrets.DOCKERHUB_USERNAME }}  
          password: ${{ secrets.DOCKERHUB_TOKEN }}  
      -  
        name: Set up Docker Buildx  
        uses: docker/setup-buildx-action@v3  
      -  
        # Build and push to dockerhub  
        name: Build and push  
        uses: docker/build-push-action@v5  
        with:  
          context: .  
          file: ./Dockerfile  
          push: true  
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/${{ secrets.PROJECT_NAME }}:latest  
  
      # EC2 인스턴스 접속 및 애플리케이션 실행  
      -  
        name: Application Run  
        uses: appleboy/ssh-action@v0.1.6  
        with:  
          host: ${{ secrets.EC2_HOST }}  
          username: ${{ secrets.EC2_USERNAME }}  
          key: ${{ secrets.EC2_KEY }}  
  
          script: |  
            sudo docker ps -a --filter "name=${{ secrets.PROJECT_NAME }}" | xargs -r docker stop            sudo docker ps -a --filter "name=${{ secrets.PROJECT_NAME }}" | xargs -r docker kill            sudo docker ps -a --filter "name=${{ secrets.PROJECT_NAME }}" | xargs -r docker rm -f  
            sudo docker rmi ${{ secrets.DOCKERHUB_USERNAME }}/${{ secrets.PROJECT_NAME }}            sudo docker pull ${{ secrets.DOCKERHUB_USERNAME }}/${{ secrets.PROJECT_NAME }}  
              sudo docker run -p  ${{ secrets.PORT }}:${{ secrets.PORT }} \  
            --env-file ${{ secrets.ENV }} \            --name ${{ secrets.PROJECT_NAME }} \            -v /home/ubuntu/resume_ai_chat.db:/app/resume_ai_chat.db \            -d ${{ secrets.DOCKERHUB_USERNAME }}/${{ secrets.PROJECT_NAME }}
```

main 브랜치에 푸쉬를 하면, github action 이 트리거 되어서 아래 이벤트들이 실행되도록 했다. 단계는 크게 아래와 같다. 

1. dockerhub 에 로그인
2. dockerfile 을 이용해서 이미지 빌드하기 
3. 빌드한 이미지 dockerhub 에 push 하기
4. EC2 인스턴스 접속
5. `docker ps -a --filter` 를 통해 현재 실행/중지된 컨테이너 검색해서 컨테이너 stop, kill 하기 
6.  기존에 있던 이미지 삭제 
7. dockerhub 에서 이미지 pull 받기
8. 이미지를 기반으로 컨테이너 실행하기 

![image](https://github.com/ddoddii/resume-ai-chat/assets/95014836/0bf7e653-868b-4ab3-af7f-f64096df86a1 "github action 오류 해결의 과정..")


## 앞으로 남은 일

한차례 리팩토링을 진행했지만, 아직까지 발전시킬 요소가 너무 많다. 특히 적은 사용자가 아닌 다수의 사용자가 요청하여 트래픽이 거대해질 때를 대비하여 업그레이드 시키고 싶다. 학교 수업과 과제만으로는 실제 사용자가 있는 서비스를 만들어내기 쉽지 않다. 그래서 이 프로젝트가 더욱 재미있었던 것 같다. 후반부 작업에 많은 도움을 주고 옆에서 열심히 방향을 알려준 [@인엽](https://github.com/inshining) 오빠에게 특히 고맙다.


앞으로 남은 일을 추려 보자면..
- 실사용자가 많아지면 MySQL 로 DB 마이그레이션 
- 한글 버전 만들기 
- 산학 컨택 
- OpenAI API 에만 의존하지 않도록 다른 API 찾기 + OpenAI API 모니터링 
- Testcode 작성
