#!/usr/bin/env python3
"""以 claude -p 在 fixture 執行一輪，並把輸入、工具動作、輸出與前後狀態寫入證據檔。

用法：
  CLAUDE_CONFIG_DIR=<隔離設定> python3 run_case.py <fixture 目錄> <證據 .md> <raw 目錄> "<使用者訊息>" [--resume <session_id>]

同一證據檔重複呼叫時以「回合」附加。需要前後狀態一致的查詢案例，比對工作樹雜湊與 HEAD。
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ALLOWED = ["Read", "Edit", "Write", "Glob", "Grep", "Skill",
           "Bash(git:*)", "Bash(python3:*)", "Bash(ls:*)", "Bash(cat:*)", "Bash(date:*)"]
MODEL = "claude-opus-5-5"


def snapshot(cwd):
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=cwd, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=cwd,
                            capture_output=True, text=True).stdout
    digest = hashlib.sha256()
    for path in sorted(p for p in Path(cwd).rglob("*") if p.is_file() and ".git" not in p.parts):
        digest.update(str(path.relative_to(cwd)).encode())
        digest.update(path.read_bytes())
    return head, status, digest.hexdigest()[:16]


def brief(tool_input):
    text = json.dumps(tool_input, ensure_ascii=False)
    return text if len(text) <= 160 else text[:157] + "..."


def main():
    args = sys.argv[1:]
    resume = None
    if "--resume" in args:
        i = args.index("--resume")
        resume = args[i + 1]
        del args[i:i + 2]
    fixture, evidence, raw_dir, message = Path(args[0]), Path(args[1]), Path(args[2]), args[3]
    raw_dir.mkdir(parents=True, exist_ok=True)
    before = snapshot(fixture)
    cmd = ["claude", "-p", message, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--allowedTools", *ALLOWED]
    if resume:
        cmd += ["--resume", resume]
    start = time.time()
    proc = subprocess.run(cmd, cwd=fixture, capture_output=True, text=True)
    elapsed = time.time() - start
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip().startswith("{")]
    turn = 1 + (evidence.read_text().count("\n## 回合 ") if evidence.exists() else 0)
    raw = raw_dir / f"{evidence.stem}-turn{turn}.jsonl"
    raw.write_text(proc.stdout)
    tools, result, session, models, denials = [], "", None, [], []
    for event in events:
        if event.get("type") == "assistant":
            for block in event["message"].get("content", []):
                if block.get("type") == "tool_use":
                    tools.append(f"{block['name']} {brief(block.get('input', {}))}")
        if event.get("type") == "result":
            result = event.get("result", "")
            session = event.get("session_id")
            models = list((event.get("modelUsage") or {}).keys())
            denials = event.get("permission_denials") or []
    after = snapshot(fixture)
    lines = []
    if turn == 1:
        lines += [f"# {evidence.stem}", "", f"- fixture：`{fixture.name}`", f"- 指定模型：`{MODEL}`",
                  f"- 允許工具：{', '.join(ALLOWED)}", ""]
    lines += [f"## 回合 {turn}", "", f"- session：`{session}`；實際模型：{', '.join(models) or '未知'}；"
              f"exit {proc.returncode}；耗時 {elapsed:.0f}s", f"- 前：HEAD `{before[0][:7]}`、工作樹雜湊 `{before[2]}`",
              f"- 後：HEAD `{after[0][:7]}`、工作樹雜湊 `{after[2]}`；git status：{'無變更' if not after[1] else '有變更'}",
              "", "### 使用者輸入", "", "```text", message, "```", "", "### 工具動作", ""]
    lines += [f"{n}. `{t}`" for n, t in enumerate(tools, 1)] or ["（無）"]
    if denials:
        lines += ["", "權限拒絕：" + "; ".join(brief(d) for d in denials)]
    if after[1]:
        lines += ["", "### 回合後 git status", "", "```text", after[1].rstrip(), "```"]
    lines += ["", "### 最終輸出", "", "````markdown", result.rstrip(), "````", ""]
    with evidence.open("a") as handle:
        handle.write("\n".join(lines) + "\n")
    print(json.dumps({"session": session, "turn": turn, "changed": before != after, "exit": proc.returncode}))
    print(result)


if __name__ == "__main__":
    main()
