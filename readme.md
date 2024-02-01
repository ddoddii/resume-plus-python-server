# 🤖 Chat Your Interview 

- [@ddoddii](https://github.com/ddoddii) 의 회고 : [Chat Your Interview](https://ddoddii.github.io/post/project/chatyourinterview/about/)
- [@inshining](https://github.com/inshining) 의 회고 : [도커를 곁들인 프로젝트 리팩토링하기](https://inshining.github.io/posts/2024-01-4-refactoring-with-docekr/)

## ✨About this project
 
> 내일이 면접이라고 😱? 내 자소서 기반으로 맞춤 면접 준비 도와주는 Chat Your Interview 에게 도움을 요청해보세요 ! 🔮

- **대상**
    
    개발직군 (Backend / Frontend / AI / Mobile) 취업 준비생
    
- **기대 효과**
    
    취업 준비생들이 이 서비스를 통해 본인의 CV를 기반으로 맞춤형 질문을 자동으로 생성할 수 있으며, 면접 준비에 큰 도움을 받을 수 있습니다.
    
- **현재 사용 가능한 기능**
    - 사용자가 선택한 직군(BE/FE/AI/Mobile) 별 기술 문제 N개 , 공통 인성 질문 N개, CV 맞춤 질문 5개 가 채팅형식으로 순차적으로 주어지고, 사용자는 그에 맞는 답변을 입력합니다.
    - 모든 질문-답변 이 끝나면, 사용자의 답변을 기반으로 얼마나 맞았는지 평가해줍니다.
        - 이때 기술 질문은 저희가 사전에 제작한 정답 기반, 개인 질문은 여러 criteria 기반으로 평가합니다.
    - 사용자는 각 질문 별로 평가 항목에 따라 점수와 채점 기준등을 제공 받습니다.

- **팀원**
  - BE : 엄소은
  - FE : 김수빈
  - ML : 임예원, 윤장한

- **데모 영상**

https://github.com/ddoddii/resume-ai-chat/assets/95014836/276beb6f-7f4a-4788-b29d-e28ca413a66a


## 🚗 User Flow

1. 사용자가 회원가입 후 로그인 
2. 채팅 시작 후 개인 CV 업로드,  지원하는 포지션 선택
3. 기술 질문 2개 , 인성 질문 2개 질문 (질문 개수는 조정 가능)
4. CV 기반 맞춤 질문 5개 질문 (질문 개수는 조정 가능)
5. 사용자의 답변에 대한 평가 생성


## 💻 Project Stack
- Backend : FastAPI
- Frontend : React
- Infra : AWS EC2
- Model : VAE + Chat GPT 3.5 (with prompt engineering)

## 📌 Upcoming Features

앞으로 계획하고 있는 추가 기능
- 실제 면접 경험과 유사하게 만들기 위한 화상 기능
- 한글 버전
