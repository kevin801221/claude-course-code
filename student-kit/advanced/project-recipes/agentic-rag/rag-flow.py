#!/usr/bin/env python3
"""Offline teaching simulation of retrieve/grade/rewrite/generate.

Original student-kit example based on lecture Appendix B concepts.
No LLM, SDK, embedding model, network, or actual relevance grading is used.
"""
import argparse
import json

DOCUMENTS = {
    "hooks": {"id": "lesson-hooks", "text": "Hooks 可以在指定事件觸發可重複的檢查腳本。"},
    "skills": {"id": "lesson-skills", "text": "Skill 用 SKILL.md 描述何時使用與如何完成一項工作。"},
}
REWRITES = {"自動化": "hooks"}


def run(question: str) -> dict:
    query = question.strip().casefold()
    trace = []
    for attempt in range(2):
        trace.append({"node": "retrieve", "query": query})
        document = DOCUMENTS.get(query)
        trace.append({"node": "grade", "relevant": document is not None})
        if document is not None:
            trace.append({"node": "generate"})
            return {"status": "answered", "answer": document["text"],
                    "citations": [document["id"]], "trace": trace}
        if attempt == 0:
            query = REWRITES.get(query, query)
            trace.append({"node": "rewrite", "query": query})
    trace.append({"node": "stop", "reason": "retry-limit"})
    return {"status": "insufficient-evidence", "answer": "沒有足夠證據回答。",
            "citations": [], "trace": trace}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="Try hooks, 自動化, or 天氣")
    args = parser.parse_args()
    print(json.dumps(run(args.question), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
