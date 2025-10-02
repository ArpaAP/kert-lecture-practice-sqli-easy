# SQL Injection 실습 환경

SQL Injection 취약점을 안전하게 학습할 수 있는 실습 환경입니다.

## 학습 목표

- SQL Injection 공격 원리 이해
- 취약한 코드 패턴 학습
- 안전한 코딩 방법 습득

## 프로젝트 구조

- **Frontend**: Vite + React
- **Backend**: FastAPI + SQLite
- **패키지 매니저**: pnpm

## 프로젝트 실행 방법

### 1. Backend 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend 서버가 http://localhost:8000 에서 실행됩니다.

### 2. Frontend 실행

새 터미널 창에서:

```bash
cd frontend
pnpm install
pnpm dev
```

Frontend가 http://localhost:5173 에서 실행됩니다.

## 실습 진행 방법

1. 브라우저에서 http://localhost:5173 접속
2. `admin` 계정으로 로그인 시도
3. SQL Injection을 이용해서 로그인 우회

### 힌트

- 실행되는 SQL 쿼리: `SELECT * FROM users WHERE username = '...' AND password = '...'`
- 어떻게 하면 이 쿼리의 결과를 조작할 수 있을까요?

<details>
<summary>정답 예시</summary>

Username: `admin' --`
Password: (아무거나)

또는

Username: `admin' OR '1'='1`
Password: (아무거나)

</details>

## ⚠️ 주의사항

**이 환경은 교육 목적으로만 사용하세요!**