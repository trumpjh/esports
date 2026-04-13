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

### 3단계 — GitHub Pages 활성화

1. 저장소 → **Settings** 탭
2. 왼쪽 사이드바 → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** / **/ (root)** 선택 후 **Save**
5. 잠시 후 `https://사용자명.github.io/esports-quiz/` 주소로 접속 가능

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

- 54문항 전체 또는 원하는 범위/개수만 선택 가능
- 문제 무작위 섞기 / 보기 무작위 섞기
- 답 선택 즉시 정오 피드백 + 해설 표시
- 시험 종료 후 점수, 등급, 틀린 문제 복습
- 틀린 문제만 다시 풀기

---

## 📱 접속 링크 학생 공유 방법

GitHub Pages 배포 후 생성된 URL을 카카오톡, 클래스룸 등으로 공유하면  
학생들이 스마트폰, PC 어디서든 바로 접속할 수 있습니다.

> 예시: `https://yourname.github.io/esports-quiz/`
