"""
e스포츠 윤리 퀴즈 - 문항 파싱 스크립트
========================================
사용법:
  pip install python-docx
  python parse_questions.py

두 개의 .docx 파일을 읽어 questions.json 을 생성합니다.
생성된 questions.json 을 index.html 과 같은 폴더에 놓으면 퀴즈가 작동합니다.
"""

import re
import json
from pathlib import Path

# ── 파일 경로 설정 ──
QUESTIONS_FILE = "e스포츠_윤리_54문항.docx"          # 문제 파일
ANSWERS_FILE   = "e스포츠_윤리_54문항_풀이.docx"      # 풀이 파일
OUTPUT_FILE    = "questions.json"                     # 출력 파일


def read_docx_paragraphs(path: str) -> list[str]:
    """docx 파일에서 단락 텍스트 목록을 반환합니다."""
    from docx import Document
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs]


def parse_questions(paragraphs: list[str]) -> list[dict]:
    """
    문제 파일의 단락을 파싱하여 문제 목록을 반환합니다.

    각 문제의 형식:
        1. **질문 텍스트  정답_알파벳**
        A. 보기1
        B. 보기2
        ...
    """
    questions = []
    current_q = None

    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]

        # ── 문제 번호 감지 ──
        # 예: "1. **스포츠 윤리의... D**"  또는  "**25. 멘탈..."
        num_match = re.match(r'^(?:\*\*)?(\d+)[.\s]+\*?\*?(.+)', para)
        if num_match:
            qnum = int(num_match.group(1))
            raw_text = num_match.group(2)

            # 여러 줄에 걸친 문제 텍스트 합치기
            j = i + 1
            while j < len(paragraphs):
                next_para = paragraphs[j].strip()
                if re.match(r'^[A-E]\.', next_para):
                    break
                if re.match(r'^(?:\*\*)?(\d+)[.\s]+', next_para):
                    break
                if next_para:
                    raw_text += ' ' + next_para
                j += 1
            i = j - 1  # 다음 루프에서 j 부터 시작

            # 정답 추출 (텍스트 끝 알파벳)
            answer = None
            ans_match = re.search(r'\b([A-E])\s*\*?\*?\s*$', raw_text.rstrip('*').rstrip())
            if ans_match:
                answer = ans_match.group(1)

            # 질문 텍스트 정제
            qtext = re.sub(r'\s+[A-E]\s*\*?\*?\s*$', '', raw_text.rstrip('*')).strip()
            qtext = qtext.replace("'", "'").strip('*').strip()

            if current_q:
                questions.append(current_q)

            current_q = {
                "number": qnum,
                "question": qtext,
                "answer": answer,
                "options": {},
                "explanations": {}
            }

        # ── 보기 감지 ──
        elif current_q:
            opt_match = re.match(r'^([A-E])\.\s*(.*)', para)
            if opt_match:
                letter = opt_match.group(1)
                opt_text = opt_match.group(2).replace("'", "'").strip()

                # 다음 줄이 보기 연속인지 확인
                j = i + 1
                while j < len(paragraphs):
                    next_para = paragraphs[j].strip()
                    if re.match(r'^[A-E]\.', next_para) or re.match(r'^\d+[.\s]', next_para) or not next_para:
                        break
                    opt_text += ' ' + next_para
                    j += 1
                i = j - 1

                current_q["options"][letter] = opt_text.strip()

        i += 1

    if current_q:
        questions.append(current_q)

    return questions


def parse_explanations(paragraphs: list[str]) -> dict[int, dict[str, str]]:
    """
    풀이 파일의 단락을 파싱하여 {문제번호: {알파벳: 설명}} 딕셔너리를 반환합니다.
    """
    explanations = {}
    current_qnum = None
    current_letter = None
    buffer = []

    def flush():
        if current_qnum and current_letter and buffer:
            text = ' '.join(buffer).strip()
            explanations.setdefault(current_qnum, {})[current_letter] = text

    for para in paragraphs:
        para_clean = para.strip()

        # 문제 번호
        num_match = re.match(r'^(?:\*\*)?(\d+)[.\s]+', para_clean)
        if num_match:
            flush()
            current_qnum = int(num_match.group(1))
            current_letter = None
            buffer = []
            continue

        if current_qnum is None:
            continue

        # 보기 알파벳 (단독 줄)
        if re.match(r'^([A-E])\.?$', para_clean):
            flush()
            current_letter = re.match(r'^([A-E])\.?$', para_clean).group(1)
            buffer = []
            continue

        # 정답 표시
        if '정답입니다' in para_clean:
            buffer.append('[정답]')
            continue

        # 설명 텍스트 (보기 텍스트 줄은 건너뜀 — 첫 번째 줄인 경우가 많음)
        if current_letter and para_clean and not re.match(r'^\d+[.\s]', para_clean):
            buffer.append(para_clean.replace("'", "'"))

    flush()
    return explanations


def main():
    print("=" * 50)
    print("e스포츠 윤리 퀴즈 - 문항 파싱 스크립트")
    print("=" * 50)

    # ── 파일 존재 확인 ──
    for fpath in [QUESTIONS_FILE, ANSWERS_FILE]:
        if not Path(fpath).exists():
            print(f"❌ 파일을 찾을 수 없습니다: {fpath}")
            print("   스크립트와 같은 폴더에 .docx 파일을 놓아주세요.")
            return

    # ── 파싱 ──
    print(f"📄 문제 파일 읽는 중: {QUESTIONS_FILE}")
    q_paragraphs = read_docx_paragraphs(QUESTIONS_FILE)
    questions = parse_questions(q_paragraphs)
    print(f"   → {len(questions)}문제 파싱 완료")

    print(f"📄 풀이 파일 읽는 중: {ANSWERS_FILE}")
    a_paragraphs = read_docx_paragraphs(ANSWERS_FILE)
    explanations = parse_explanations(a_paragraphs)
    print(f"   → {len(explanations)}문제의 해설 파싱 완료")

    # ── 합치기 ──
    for q in questions:
        q["explanations"] = explanations.get(q["number"], {})

    # ── 저장 ──
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 완료! {len(questions)}문제가 {OUTPUT_FILE} 에 저장되었습니다.")
    print(f"   누락된 정답이 있는 문제: ", end="")
    missing_ans = [q["number"] for q in questions if not q.get("answer")]
    print(missing_ans if missing_ans else "없음")


if __name__ == "__main__":
    main()
