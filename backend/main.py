import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 기존 데이터 삭제
    cursor.execute('DELETE FROM users')

    # admin 계정 추가
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('admin', 'super_secret_password_123')"
    )

    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/login")
async def login(request: LoginRequest):
    # SQL Injection 취약점이 있는 코드
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 의도적으로 취약한 쿼리 (교육용)
    query = f"SELECT * FROM users WHERE username = '{request.username}' AND password = '{request.password}'"

    print(f"Executing query: {query}")  # 디버깅용

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"success": True, "message": "로그인 성공! SQL Injection 취약점을 찾았습니다!"}
    else:
        return {"success": False, "message": "로그인 실패"}

@app.get("/")
async def root():
    return {"message": "SQL Injection Practice Server"}
