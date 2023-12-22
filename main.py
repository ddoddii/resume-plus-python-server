import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database.models as models
from database.setup import engine
from routers import question, answer, auth, user


app = FastAPI(
    title = 'GDSC Resume AI Chat',
    version = 'v1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.35.192:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind = engine)


app.include_router(question.router)
app.include_router(answer.router)
app.include_router(auth.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)