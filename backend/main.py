import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vite 기본 포트
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

    # 더미 계정 추가
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('user1', 'password1')"
    )
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('user2', 'password2')"
    )

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

    query = f"SELECT * FROM users WHERE username = '{request.username}'"

    print(f"Executing query: {query}")  # 디버깅용

    cursor.execute(query)
    user = cursor.fetchone()

    # 유저를 찾았고 유저네임이 admin인지 체크
    if user and user[1] == 'admin':
        # 패스워드 체크 (취약)

        query = f"SELECT * FROM users WHERE username = '{request.username}' AND password = '{request.password}'"

        print(f"Executing query: {query}")  # 디버깅용

        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            conn.close()

            return {"success": True, "message": "로그인 성공! SQL Injection 취약점을 찾았습니다!"}

        conn.close()

        return {"success": False, "message": "아이디 또는 비밀번호가 잘못되었습니다."}
    else:

        conn.close()
        return {"success": False, "message": "아이디 또는 비밀번호가 잘못되었습니다."}
        

@app.get("/")
async def root():
    return {"message": "SQL Injection Practice Server"}
