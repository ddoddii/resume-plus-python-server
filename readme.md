# 🤖 Chat Your Interview 

- [@ddoddii](https://github.com/ddoddii) 의 회고 : [Chat Your Interview](https://ddoddii.github.io/post/project/chatyourinterview/about/)
- [@inshining](https://github.com/inshining) 의 회고 : [도커를 곁들인 프로젝트 리팩토링하기](https://inshining.github.io/posts/2024-01-4-refactoring-with-docekr/)

## ✨About this project

- **대상 타겟**
    
    개발직군 (Backend / Frontend / AI / Mobile) 취업 준비생
    
- **기대 효과**
    
    취업 준비생들이 이 서비스를 통해 본인의 CV를 기반으로 맞춤형 질문을 자동으로 생성할 수 있으며, 면접 준비에 큰 도움을 받을 수 있습니다.
    
- **현재 프로젝트 진행 상태**
    - 사용자가 선택한 직군(BE/FE/AI/Mobile) 별 기술 문제 N개 , 공통 인성 질문 N개, CV 맞춤 질문 5개 가 채팅형식으로 순차적으로 주어지고, 사용자는 그에 맞는 답변을 입력합니다.
    - 모든 질문-답변 이 끝나면, 사용자의 답변을 기반으로 얼마나 맞았는지 평가해줍니다.
        - 이때 기술 질문은 저희가 사전에 제작한 정답 기반, 개인 질문은 여러 criteria 기반으로 평가합니다.
    - 사용자는 각 질문 별로 평가 항목에 따라 점수와 채점 기준등을 제공 받습니다.

- **데모 영상**

https://github.com/ddoddii/resume-ai-chat/assets/95014836/d1add248-0a06-485f-9f4f-e2f8ed250203

    
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/cgK4MzohPjA/0.jpg)](https://www.youtube.com/watch?v=cgK4MzohPjA)

- 팀원
  - BE : 엄소은
  - FE : 김수빈
  - ML : 임예원, 윤장한

## 🚗 User Flow

1. 사용자가 회원가입 
2. 채팅 시작 후 개인 CV 업로드,  지원하는 포지션 선택
3. 기술 질문 2개 , 인성 질문 2개 질문 (질문 개수는 조정 가능)
4. CV 기반 맞춤 질문 5개 질문 (질문 개수는 조정 가능)
5. 사용자의 답변에 대한 평가 생성


## 💻 Project Stack
- Backend : FastAPI
- Frontend : React
- Infra : AWS EC2
- Model : VAE + Chat GPT 3.5 (with prompt engineering)

## 📌 To Do

한차례 리팩토링을 진행했지만, 아직까지 발전시킬 요소가 너무 많다. 특히 적은 사용자가 아닌 다수의 사용자가 요청하여 트래픽이 거대해질 때를 대비하여 업그레이드 시키고 싶다. 
학교 수업과 과제만으로는 실제 사용자가 있는 서비스를 만들어내기 쉽지 않다. 그래서 이 프로젝트가 더욱 재미있었던 것 같다. 후반부 작업에 많은 도움을 주고 옆에서 열심히 방향을 알려준 [@인엽](https://github.com/inshining) 오빠에게 특히 고맙다.


앞으로 남은 일...
- 실제 면접 경험과 유사하게 만들기 위한 화상 기능 추가 
- 한글 버전
- OpenAI API 에만 의존하지 않도록 다른 API 찾기 + OpenAI API 모니터링 
- Testcode 작성
