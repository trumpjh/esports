# 🎮 e스포츠 윤리 퀴즈

e스포츠 윤리 54문항 온라인 퀴즈 앱입니다.  
GitHub Pages로 배포하여 학생들이 웹브라우저에서 바로 풀 수 있습니다.

---

## 📁 파일 구조

```
esports-quiz/
├── index.html          ← 퀴즈 웹앱 (메인 파일)
├── questions.json      ← 문제 데이터 (54문항)
├── parse_questions.py  ← docx → JSON 변환 스크립트 (문제 수정 시 사용)
└── README.md
```

---

## 🚀 GitHub Pages 배포 방법

### 1단계 — 저장소 만들기

1. [github.com](https://github.com) 에서 새 저장소 생성
2. 저장소 이름 예: `esports-quiz`
3. **Public** 으로 설정 (GitHub Pages 무료 사용 조건)

### 2단계 — 파일 업로드

방법 A (웹에서 바로):
1. 저장소 페이지에서 **Add file → Upload files**
2. `index.html`, `questions.json` 두 파일을 업로드
3. **Commit changes** 클릭

방법 B (Git 명령어):
```bash
git init
git add .
git commit -m "첫 커밋: e스포츠 윤리 퀴즈"
git branch -M main
git remote add origin https://github.com/사용자명/esports-quiz.git
git push -u origin main
```

### 4단계 — GitHub Pages 배포 확인

배포된 사이트 확인:
- URL: `https://사용자명.github.io/esports-quiz`
- 웹브라우저에서 접속하여 정상 작동 확인

---

## 🏆 Firebase 실시간 순위표 설정 (선택사항)

### 1단계 — Firebase 프로젝트 생성

1. [firebase.google.com](https://firebase.google.com) 접속
2. **프로젝트 만들기** 클릭
3. 프로젝트 이름 입력 (예: `esports-quiz`)
4. **계속** → **Google 애널리틱스 사용 안함** → **프로젝트 만들기**

### 2단계 — Realtime Database 설정

1. Firebase 콘솔 → **Build** → **Realtime Database**
2. **데이터베이스 만들기** 클릭
3. 위치 선택 (예: `asia-southeast1`)
4. **테스트 모드에서 시작** 선택 → **사용 설정**
5. **규칙** 탭에서 아래 코드 적용:

```json
{
  "rules": {
    "scores": {
      ".read": true,
      ".write": true,
      "$uid": {
        ".validate": true
      }
    }
  }
}
```

### 3단계 — 웹 앱 등록 및 설정

1. 프로젝트 설정 (⚙️ 아이콘) → **프로젝트 설정**
2. **앱** 섹션에서 **웹 앱 등록** (`</>`)
3. 앱 이름 입력 → **앱 등록**
4. 표시된 설정 코드 복사 (firebaseConfig 객체)
5. `index.html` 파일을 텍스트 에디터로 열기
6. 다음 부분을 찾아 수정:

```javascript
// ← index.html 약 456줄 근처
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  databaseURL: "YOUR_DATABASE_URL",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

**Firebase 콘솔의 설정값으로 위의 YOUR_* 부분을 모두 교체하세요.**

예시:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyD_abc123...",
  authDomain: "myproject-12345.firebaseapp.com",
  databaseURL: "https://myproject-12345-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "myproject-12345",
  storageBucket: "myproject-12345.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcd1234efgh5678"
};
```

7. 수정된 `index.html` 파일을 GitHub에 업로드

### 4단계 — 배포 확인

`https://사용자명.github.io/esports-quiz/` 에서 시험을 완료하면:
- ✅ 학번이 자동으로 순위표에 기록됨
- ✅ 실시간 상위 10명의 점수와 자신의 등수 확인 가능
- ✅ 다른 학생들과 동시에 성적 공유 가능

---

## 🔄 문제 수정 방법

docx 파일을 수정했다면 Python 스크립트로 JSON을 다시 생성하세요:

```bash
# 필요한 라이브러리 설치 (최초 1회)
pip install python-docx

# 스크립트와 같은 폴더에 두 개의 docx 파일을 놓고 실행
python parse_questions.py
```

새로 생성된 `questions.json`을 GitHub에 다시 업로드하면 됩니다.

---

## ✨ 기능

**기본 기능:**
- 54문항 중 선택한 개수만 응시 가능
- 모든 문제와 보기는 **무작위로 자동 섞임**
- 답 선택 즉시 정오 피드백 + 상세 해설 표시
- **틀리면 즉시 초기 화면으로 돌아가기** (게임 오버)
- 모든 문항 정답 시에만 최종 점수 표시
- 시험 종료 후 맞춘 개수, 등급, 틀린 문제 복습

**Firebase 순위표 기능 (설정 时):**
- 학번이 자동으로 순위표에 기록
- 실시간 상위 10명 순위 표시
- 모든 학생이 공유된 순위 확인 가능
- 점수 = 맞춘 문항 개수 기준으로 정렬

---

## 📱 접속 링크 학생 공유 방법

GitHub Pages 배포 후 생성된 URL을 카카오톡, 클래스룸 등으로 공유하면  
학생들이 스마트폰, PC 어디서든 바로 접속할 수 있습니다.

> 예시: `https://yourname.github.io/esports-quiz/`

---

## ⚙️ 설정 안내

| 설정 | 기본값 | 설명 |
|------|--------|------|
| 학번 | 필수 | 학생 학번 또는 이름 입력 |
| 문제 수 | 54 | 10/20/30/54/직접 입력 |
| 문제 순서 | 무작위 | **항상 무작위** (선택 불가) |
| 보기 순서 | 무작위 | **항상 무작위** (선택 불가) |
| 틀릴 경우 | 게임 오버 | 한 문제라도 틀리면 시험 중단, 초기화면으로 돌아감 |

---

## 🐛 문제 해결

**Q: 순위표가 안 나타나요.**
- Firebase 설정이 제대로 되었는지 확인하세요.
- 브라우저 개발자 도구(F12) → Console에서 오류 메시지 확인

**Q: 학번을 입력해도 순위에 등재되지 않아요.**
- JavaScript 콘솔을 확인하여 Firebase 연결 상태 확인
- firebaseConfig의 databaseURL이 올바른지 확인

**Q: 문제가 이전과 같은 순서로 나와요.**
- 페이지를 새로고침(Ctrl+F5)하고 다시 시도하세요.
