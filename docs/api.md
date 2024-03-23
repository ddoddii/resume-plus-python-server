# API Docs

## User
### Create user
- Method : `POST`
- Endpoint : `/auth`
- Request Parameters:
  - username (string) : max length 20
  - name (string) : max length 20
  - email (string) : max length 30
  - password (string) : max length 20
- Success Response
  - Status : 201 Created
  - Content : 
  ```json
  {'message' : 'User sucessfully created'}
  ```
- Bad Response
  - Status : 400 
  - Content : `Username already exists`


### Get user CVs
- Method : `GET`
- Endpoint: `/cv`
- Success Response:
  - Status : 200
  - Content
  ```json
  [
    {
      "position": "be",
      "id": 1,
      "user_id": 1,
      "content": "soeun's cv- be",
      "upload_time": "2023-12-02 12:57:27"
    },
    {
      "position": "ml",
      "id": 2,
      "user_id": 1,
      "content": "soeun's cv - ml",
      "upload_time": "2023-12-02 13:56:18"
    }
  ]
  ```

### CV upload
- Method : `POST`
- Endpoint : `/cv`
- Request Parameters:
  - content (string)
  - position : ['ai','be','fe','mobile]
- Success Response
  - Status : 200
  - Content : `{"message" : "CV upload success"}`
- Bad Response
  - Status : 401
  - Content : `Authentication Failed`

### CV update
- METHOD : `PUT`
- Endpoint : `/cv/{cv_id}`
- Request Parameters : 
  - cv_id (int) : 수정하려는 cv id
  - content (string)
  - position : ['ai','be','fe','mobile]
- Success Response
  - Status : 200
  - Content : `{"message" : "CV update success"}`
- Bad Response
  - Status : 404
  - Content :  `"CV not found"`


### CV delete
- METHOD : `DELETE`
- Endpoint : `/cv/{cv_id}`
- Request Parameters : 
  - cv_id (int) : 수정하려는 cv id
- Success Response
  - Status : 204
  - Content : `{"message" : "CV delete success"}`

## Question
### Get Personal Questions
- Method : `GET`
- Endpoint : `/personal_question`
- Sample Response
  ```json
  {
    "personal_questions": [
      {
        "idx": 5,
        "question": "Can you provide an example of a project or research you have worked on related to large multimodal learning or vision-language model?",
        "criteria": [
          "Relevance to research interest",
          "Project details and implementation",
          "Problem-solving approach",
          "Collaboration and teamwork",
          "Results and impact"
        ]
      },
      {
        "idx": 6,
        "question": "How did you leverage questions decomposition for query generation and seamlessly incorporate external open-domain knowledge in the fact-checking framework for LLMs during your research internship at Linq?",
        "criteria": [
          "Problem-solving approach",
          "Innovation and creativity",
          "Technical skills",
          "Adaptability",
          "Impact and results"
        ]
      },
      {
        "idx": 9,
        "question": "Can you explain the process of integrating EHR graph with generated explanation text to enhance medical representation and capture the progression of diagnoses in the Medication Combination Recommender System project at Data Mining Lab @ KAIST AI?",
        "criteria": [
          "Technical skills",
          "Problem-solving approach",
          "Collaboration and teamwork",
          "Project details and implementation",
          "Results and impact"
        ]
      },
      {
        "idx": 12,
        "question": "How did you approach the research on unsupervised continual learning and few-shot learning during your time at Machine Learning Lab @ Yonsei Univ.?",
        "criteria": [
          "Problem-solving approach",
          "Research methodology",
          "Technical skills",
          "Adaptability",
          "Results and impact"
        ]
      },
      {
        "idx": 15,
        "question": "Can you discuss how you quantified brand image using text rank and sentiment analysis on crawled text data during your internship at LG H&H?",
        "criteria": [
          "Project details and implementation",
          "Problem-solving approach",
          "Analytical skills",
          "Results and impact",
          "Adaptability"
        ]
      }
    ]
  }
  ```

### Get Common Questions
- Method : `GET`
- Endpoint : `/common_question`
- Sample response: 
  ```json
  {
    "tech_questions": [
      {
        "id": 1,
        "question": "Compare Relational DB (SQL) vs NoSQL. It's also really nice to know about newSQL (a kind of auto sharding DB which support SQL stuff but scale like NoSQL)"
      },
      {
        "id": 151,
        "question": "Explain context switching."
      }
    ],
    "behav_questions": [
      {
        "id": 6,
        "question": "What are the three things that are most important to you in a job?"
      },
      {
        "id": 14,
        "question": "Describe the best partner or supervisor you’ve worked with. What part of their management style appealed to you?"
      }
    ]
  }
  ```
## Answer

### Get Asked Questions in current session
- Method : `GET`
- Endpoint : `/asked_question`
- Success Response
  - Status : 200
  - Content
  ```json
  {
    "tech_ids": [
      108,
      155
    ],
    "behav_ids": [
      8,
      18
    ]
  }
  ```


### User answer response - tech question
- Method : `POST`
- Endpoint : `/submit_tech_answer/{question_id}`
- Request Parameters :
  - question_id (int) : tech question id
- Success Response:
  - Status : 200 OK
  - Content :

  ```json
  {
    "type": "techQ",
    "question": "Explain context switching.",
    "user_answer": "I DON'T KNOW",
    "evaluation": {
      "evaluation": [
        {
          "criteria": "Accuracy",
          "score": "1",
          "rationale": "The answers does not provide any accurate information about context switching."
        },
        {
          "criteria": "Clarity",
          "score": "1",
          "rationale": "The answers lacks clarity and does not effectively communicate any understanding of the concept."
        },
        {
          "criteria": "Relevance",
          "score": "1",
          "rationale": "The answers is not relevant to the questions and does not address the topic of context switching."
        },
        {
          "criteria": "Depth",
          "score": "1",
          "rationale": "The answers lacks depth and does not demonstrate any understanding or knowledge of context switching."
        },
        {
          "criteria": "Coherence",
          "score": "1",
          "rationale": "The answers is not coherent and does not present any logical or organized thoughts on the topic."
        }
      ]
    }
  }
  ```
### User answer response - behav question
- Method : `POST`
- Endpoint : `/submit_behav_answer/{question_id}`
- Request Parameters :
  - question_id (int) : behav question id
- Success Response:
  - Status : 200 OK
  - Content :

  ```json
  {
    "type": "behavQ",
    "question": "Describe the best partner or supervisor you’ve worked with. What part of their management style appealed to you?",
    "user_answer": "I DON'T KNOW",
    "evaluation": {
      "score": 1,
      "rationale": "The answers does not demonstrate any collaboration as it lacks specific details or examples of working with a partner or supervisor. It does not provide any insight into the management style that appealed to the candidate."
    }
  }
  ```

### User answer response - personal question
- Method : `POST`
- Endpoint : `/submit_personal_answer`
- Success Response:
  - Status : 200 OK
  - Content :

  ```json
  {
    "type": "perQ",
    "question": "Describe the best partner or supervisor you’ve worked with. What part of their management style appealed to you?",
    "user_answer": "I DON'T KNOW",
    "evaluation": {
      "score": 1,
      "rationale": "The answers does not demonstrate any collaboration as it lacks specific details or examples of working with a partner or supervisor. It does not provide any insight into the management style that appealed to the candidate."
    }
  }
  ```

