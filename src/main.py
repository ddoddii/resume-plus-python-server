import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import models
from src.configs import config
from src import database
from src.questions.router import router as questions_router
from src.answers.router import router as answers_router
from src.auth.router import router as auth_router
from src.users.router import router as users_router


app = FastAPI(title="GDSC Resume AI Chat", version="v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(questions_router)
app.include_router(answers_router)
app.include_router(auth_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
