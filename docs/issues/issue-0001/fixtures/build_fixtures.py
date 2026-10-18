#!/usr/bin/env python3
"""建立 issue-0001 的回歸 fixture：提問 q1～q4、追蹤 track、掃描層級 scan。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。fixture 只含下游專案內容，不含預期答案。
"""
import os
import subprocess
import sys
from pathlib import Path

TODO_PY = '''#!/usr/bin/env python3
"""極簡待辦 CLI，資料存於 todo.json。"""
import json
import sys
from pathlib import Path

DATA = Path("todo.json")


def load():
    return json.loads(DATA.read_text()) if DATA.exists() else []


def save(items):
    DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2))


def add(title):
    items = load()
    items.append({"id": len(items) + 1, "title": title, "done": False})
    save(items)


def done(item_id):
    items = load()
    for item in items:
        if item["id"] == item_id:
            item["done"] = True
    save(items)


def render(items):
    return "\\n".join(f'[{"x" if i["done"] else " "}] {i["id"]}. {i["title"]}' for i in items)


def main(argv):
    if argv[:1] == ["add"]:
        add(" ".join(argv[1:]))
    elif argv[:1] == ["done"]:
        done(int(argv[1]))
    else:
        print(render(load()))


if __name__ == "__main__":
    main(sys.argv[1:])
'''

TEST_PY = '''import unittest

import todo


class RenderTest(unittest.TestCase):
    def test_render_marks_done(self):
        items = [{"id": 1, "title": "買牛奶", "done": True}, {"id": 2, "title": "寫週報", "done": False}]
        self.assertEqual(todo.render(items), "[x] 1. 買牛奶\\n[ ] 2. 寫週報")


if __name__ == "__main__":
    unittest.main()
'''

README_ROOT = '''# todo

極簡待辦 CLI。

## 使用說明

- `python3 todo.py add <標題>`：新增
- `python3 todo.py done <id>`：標記完成
- `python3 todo.py`：列出

## 已移除功能

- 2026-09-20 起移除 v1 匯出（分號分隔的 `todo.py export-v1`），沒有保留相容層。
'''

PROJECT_MD = '''# 專案客製規範

本檔由專案維護，初始化只在不存在時建立，更新上游時保留。

## 專案邊界與驗證入口

單檔 CLI `todo.py`（資料存於 `todo.json`），測試 `python3 -m unittest -v`。無 build／lint。

## 提交與交付

提交採 `type(scope): 中文摘要`，footer `Refs: #ID`。分支 `issue-<ID>-<描述>`。本專案沒有遠端平台：以本機 `--no-ff` merge 進 `main` 代表 PR merged，merge commit subject 含 `issue-<ID>`。Small issue 的 Proof 表寫在 README `## 驗證`。
{scan}
## 常青文件更新責任

使用者功能 → 根目錄 `README.md` 的使用說明。

## 本地 gate 與案例

無專案特有 gate。
'''

SCAN_TRACK = '''
懸置掃描：issue 目錄 `docs/issues/`；唯讀掃描命令 `python3 tools/scan.py`（輸出 pending-scan 格式 JSON）；未登記平台查詢命令；未設掃描起點。
'''

SCAN_LEVELS = '''
懸置掃描：issue 目錄 `docs/issues/`；未登記掃描命令；平台查詢命令 `python3 tools/platform.py`（輸出 JSON，含已關閉 issue）；未設掃描起點。

懸置掃描判定規則（本專案）：

1. 狀態為 `已完成`、步驟符號停在 ⏳，但該步驟內已寫完成證據者，視為已收尾。
2. metadata `**標籤**` 含 `legacy` 的 issue 是舊系統遺留，不列入懸置掃描。
'''

SCAN_PY = r'''#!/usr/bin/env python3
"""唯讀懸置掃描：讀 docs/issues/*/README.md，輸出 pending-scan 格式 JSON。"""
import json
import re
import subprocess
from pathlib import Path


def section(text, title):
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def rows(block):
    lines = [l for l in block.splitlines() if l.startswith("|")]
    if len(lines) < 2:
        return [], []
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    return head, [[c.strip() for c in l.strip("|").split("|")] for l in lines[2:]]


def merged(issue_id):
    log = subprocess.run(["git", "log", "--merges", "--format=%s", "main"], capture_output=True, text=True).stdout
    return "inferred" if f"issue-{issue_id}" in log else "false"


issues = []
for readme in sorted(Path("docs/issues").glob("issue-*/README.md")):
    text = readme.read_text()
    issue_id = readme.parent.name.split("-")[1]
    status = re.search(r"\*\*狀態\*\*:\s*(.+)", text)
    waivers = section(text, "Gate 豁免紀錄")
    unexecuted = []
    _, proof = rows(section(text, "驗證"))
    for row in proof:
        if row and row[0].startswith("AC-") and "未執行" in row[1]:
            unexecuted.append({"ref": row[0], "location": str(readme), "waived": row[0] in waivers})
    open_steps = []
    for line in section(text, "實作與驗證步驟").splitlines():
        m = re.match(r"(\d+)\. (⏳|📝)", line)
        if m:
            open_steps.append({"step": m.group(1), "symbol": m.group(2), "location": str(readme)})
    tbd = []
    head, items = rows(section(text, "待確認事項"))
    for row in items:
        record = dict(zip(head, row))
        if "追蹤" in record:
            tracking = None if record["追蹤"] in ("", "-") else record["追蹤"]
        else:
            m = re.search(r"追蹤：([^。]+)", record.get("影響", ""))
            tracking = m.group(1).strip() if m else None
        tbd.append({"id": record.get("編號"), "status": record.get("狀態"), "tracking": tracking, "location": str(readme)})
    issues.append({
        "id": issue_id,
        "readme": str(readme),
        "status_raw": status.group(1).strip() if status else None,
        "platform_state": "unknown",
        "merged": merged(issue_id),
        "merged_basis": "本機 --no-ff merge commit subject",
        "unexecuted": unexecuted,
        "open_steps": open_steps,
        "tbd": tbd,
        "window": None,
    })

print(json.dumps({
    "scanned": len(issues),
    "scope_start": None,
    "platform": "unavailable",
    "merge_basis": "本機 --no-ff merge commit（推測）",
    "issues": issues,
    "platform_only": [],
}, ensure_ascii=False, indent=2))
'''

PLATFORM_PY = r'''#!/usr/bin/env python3
"""模擬平台 issue 查詢（含已關閉）；查不到的 issue 不列出。"""
import json

print(json.dumps({
    "issues": [
        {"id": "2201", "state": "closed"},
        {"id": "2202", "state": "open"},
        {"id": "2203", "state": "open"},
        {"id": "2204", "state": "unknown", "error": "403：此 issue 位於受限專案，目前帳號無權限讀取"},
        {"id": "2205", "state": "open"},
        {"id": "2206", "state": "closed"},
        {"id": "2207", "state": "closed"},
        {"id": "2208", "state": "closed"},
        {"id": "2209", "state": "open"},
        {"id": "2210", "state": "open"},
        {"id": "2211", "state": "unknown", "error": "逾時：平台 API 未回應"},
        {"id": "2212", "state": "closed"},
        {"id": "2213", "state": "closed"},
        {"id": "2214", "state": "open"},
        {"id": "2215", "state": "open"},
        {"id": "2216", "state": "open"},
        {"id": "2217", "state": "open"},
        {"id": "2218", "state": "open"},
        {"id": "2299", "title": "匯入時忽略空白標題", "state": "open"},
    ]
}, ensure_ascii=False, indent=2))
'''


def run(cwd, *args, date=None):
    env = dict(os.environ)
    if date:
        stamp = f"{date}T10:00:00+08:00"
        env.update(GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
    subprocess.run(args, cwd=cwd, env=env, check=True, capture_output=True)


def commit(cwd, message, date):
    run(cwd, "git", "add", "-A")
    run(cwd, "git", "commit", "-q", "-m", message, date=date)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def base(kit, path, scan=""):
    path.mkdir(parents=True)
    run(path, "git", "init", "-q", "-b", "main")
    run(path, "git", "config", "user.name", "Fixture")
    run(path, "git", "config", "user.email", "fixture@example.invalid")
    write(path / "todo.py", TODO_PY)
    write(path / "test_todo.py", TEST_PY)
    write(path / "README.md", README_ROOT)
    write(path / "AGENTS.md", (kit / "rules/AGENTS.zh-TW.md").read_text())
    write(path / "CLAUDE.md", "@AGENTS.md\n")
    write(path / ".gitignore", "todo.json\n__pycache__/\n")
    write(path / "docs/agents/project.md", PROJECT_MD.format(scan=scan))
    subprocess.run([sys.executable, str(kit / "scripts/init-project.py"), str(path)], check=True, capture_output=True)
    commit(path, "chore: 初始化待辦 CLI 與流程規範", "2026-09-25")


def small(issue_id, title, status, *, acs, proof=None, steps, tbd=None, tbd_tracking_col=False,
          waiver=None, tag=None, timeline, created, extra=""):
    lines = [f"# Issue {issue_id} - {title} (Small)", "", "## 概述", "", f"{title}。", ""]
    if extra:
        lines += [extra, ""]
    lines += ["## 驗收條件", ""]
    for n, (ref, text) in enumerate(acs, 1):
        lines.append(f"{n}. **{ref}**：{text}")
    lines += ["", f"- **核准日期**: {created}", f"- **核准來源**: {created} 使用者回覆「核准」", ""]
    lines += ["## 實作與驗證步驟", ""]
    for n, (symbol, text) in enumerate(steps, 1):
        lines.append(f"{n}. {symbol} {text}")
    lines.append("")
    if proof:
        lines += ["## 驗證", "", "| 驗收 | 結果 | 證據 |", "|---|---|---|"]
        lines += [f"| {ref} | {result} | {evidence} |" for ref, result, evidence in proof]
        lines.append("")
    if tbd:
        lines += ["## 待確認事項", ""]
        if tbd_tracking_col:
            lines += ["| 編號 | 事項 | 狀態 | 影響 | 追蹤 |", "|---|---|---|---|---|"]
        else:
            lines += ["| 編號 | 事項 | 狀態 | 影響 |", "|---|---|---|---|"]
        lines += ["| " + " | ".join(row) + " |" for row in tbd]
        lines.append("")
    if waiver:
        lines += ["## Gate 豁免紀錄", "", waiver, ""]
    lines += ["## Timeline", "", "| 日期 | 異動 | 負責人 |", "|---|---|---|"]
    lines += [f"| {d} | {e} | 開發者 |" for d, e in timeline]
    lines += ["", "---", f"**建立日期**: {created}  ", "**分級**: Small  ", "**風險**: Low  "]
    if tag:
        lines.append(f"**標籤**: {tag}  ")
    if status is not None:
        lines.append(f"**狀態**: {status}")
    return "\n".join(lines) + "\n"


def feature(path, issue_id, name, body, test, date, readme=None):
    """在 issue 分支加入真實功能、測試與 issue README，再以 --no-ff 合併。"""
    branch = f"issue-{issue_id}-{name}"
    run(path, "git", "checkout", "-q", "-b", branch)
    src = (path / "todo.py").read_text()
    src = src.replace("\n\ndef main(argv):", f"\n\n{body}\n\ndef main(argv):")
    write(path / "todo.py", src)
    write(path / f"test_{name.replace('-', '_')}.py", test)
    if readme:
        write(path / f"docs/issues/issue-{issue_id}/README.md", readme)
    commit(path, f"feat: {name}\n\nRefs: #{issue_id}", date)
    run(path, "git", "checkout", "-q", "main")
    run(path, "git", "merge", "-q", "--no-ff", branch, "-m", f"Merge branch '{branch}' (issue-{issue_id})", date=date)


def simple_feature(path, issue_id, name, func, cond, expected, date, readme):
    body = f'def {func}(items):\n    """issue-{issue_id}"""\n    return [i for i in items if {cond}]'
    test = ("import unittest\n\nimport todo\n\n\nclass T(unittest.TestCase):\n"
            f"    def test_{func}(self):\n"
            "        items = [{\"id\": 1, \"title\": \"a\", \"done\": True}, {\"id\": 2, \"title\": \"\", \"done\": False}]\n"
            f"        self.assertEqual([i[\"id\"] for i in todo.{func}(items)], {expected!r})\n")
    feature(path, issue_id, name, body, test, date, readme)


def build_questions(kit, out):
    for name in ("q1", "q2", "q3", "q4"):
        base(kit, out / name)


def build_track(kit, out):
    p = out / "track"
    base(kit, p, SCAN_TRACK)
    write(p / "tools/scan.py", SCAN_PY)
    commit(p, "chore: 加入唯讀懸置掃描命令", "2026-09-26")
    ac = [("AC-1", "依需求完成可觀察行為 — 檢查方式：`python3 -m unittest -v`")]
    step = [("⏳", "**AC-1** — 驗證方式：`python3 -m unittest -v`")]
    issues = {
        "2101": small("2101", "匯出支援 JSON 格式", "待實作", acs=ac, steps=step, created="2026-10-12",
                      extra="承接 [issue-2111 TBD-1](../issue-2111/README.md)、[issue-2112 TBD-1](../issue-2112/README.md)、[issue-2113 TBD-1](../issue-2113/README.md) 延後的 JSON 匯出與排序問題。",
                      timeline=[("2026-10-12", "建立")]),
        "2102": small("2102", "匯出欄位改為可設定", "待實作", acs=ac, steps=step, created="2026-10-12",
                      timeline=[("2026-10-12", "建立")]),
        "2111": small("2111", "CSV 匯出", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd=[("TBD-1", "是否同時支援 JSON 匯出", "不影響本次交付",
                            "結論：JSON 匯出另案處理。追蹤：[issue-2101](../issue-2101/README.md)。理由：本次只交付 CSV。2026-10-12")],
                      timeline=[("2026-10-11", "建立")]),
        "2112": small("2112", "CSV 匯出加入標題列", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd=[("TBD-1", "是否同時支援 JSON 匯出", "不影響本次交付",
                            "結論：JSON 匯出不在本次範圍，已由 [issue-2101](../issue-2101/README.md) 承接。理由：本次只交付 CSV 標題列。2026-10-12")],
                      timeline=[("2026-10-11", "建立")]),
        "2113": small("2113", "CSV 匯出依 id 排序", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd_tracking_col=True,
                      tbd=[("TBD-1", "相同 id 的排序穩定性", "不影響本次交付",
                            "結論：排序穩定性與匯出重構一併處理，本次不變更。2026-10-12", "issue-2101")],
                      timeline=[("2026-10-11", "建立")]),
        "2114": small("2114", "CSV 匯出跳脫逗號", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd_tracking_col=True,
                      tbd=[("TBD-1", "標題含換行時的處理", "不影響本次交付",
                            "結論：換行處理改由 [issue-2102](../issue-2102/README.md) 處理。2026-10-12", "issue-2101")],
                      timeline=[("2026-10-11", "建立")]),
        "2115": small("2115", "CSV 匯出改用 UTF-8 BOM", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd=[("TBD-1", "是否保留 v1 匯出的分號分隔", "不影響本次交付",
                            "結論：不保留，也無需後續處理。理由：v1 匯出已於 2026-09-20 移除（見根目錄 README「已移除功能」），本次範圍只含現行匯出，沒有呼叫端使用分號格式。2026-10-12")],
                      timeline=[("2026-10-11", "建立")]),
        "2116": small("2116", "列表顯示建立日期", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd=[("TBD-1", "日期是否顯示時區", "不影響本次交付", "結論：這個不重要。2026-10-12")],
                      timeline=[("2026-10-11", "建立")]),
        "2117": small("2117", "列表分頁", "待實作", acs=ac, steps=step, created="2026-10-11",
                      tbd=[("TBD-1", "超過 1000 筆時的效能", "不影響本次交付", "結論：以後再說，之後會再開 issue 處理。2026-10-12")],
                      timeline=[("2026-10-11", "建立")]),
        "2119": small("2119", "完成時間記錄", "待實作", acs=ac, steps=step, created="2026-10-12",
                      tbd=[("TBD-1", "既有資料沒有完成時間的補值方式", "不影響本次交付", "結論：需要後續處理。2026-10-13")],
                      timeline=[("2026-10-12", "建立")]),
        "2120": small("2120", "標題搜尋", "待實作", acs=ac, steps=step, created="2026-10-12",
                      tbd=[("TBD-1", "大量資料下的搜尋效能", "不影響本次交付",
                            "結論：效能最佳化另案處理。追蹤：[issue-2190](../issue-2190/README.md)。理由：本次只交付基本搜尋。2026-10-13")],
                      timeline=[("2026-10-12", "建立")]),
    }
    for issue_id, text in issues.items():
        write(p / f"docs/issues/issue-{issue_id}/README.md", text)
    commit(p, "docs: 建立匯出與列表相關 issue", "2026-10-13")
    # 2118：已完成且已合併，AC-2 未執行無豁免，待確認事項寫「追蹤：無」
    body = ('def export_csv(items):\n    """issue-2118：匯出 CSV。"""\n'
            '    lines = ["id,title,done"] + [f\'{i["id"]},{i["title"]},{i["done"]}\' for i in items]\n'
            '    return "\\n".join(lines)')
    test = ('import unittest\n\nimport todo\n\n\nclass ExportTest(unittest.TestCase):\n'
            '    def test_export_csv(self):\n'
            '        self.assertEqual(todo.export_csv([{"id": 1, "title": "a", "done": False}]), "id,title,done\\n1,a,False")\n')
    feature(p, "2118", "export-csv", body, test, "2026-10-08")
    write(p / "docs/issues/issue-2118/README.md", small(
        "2118", "匯出 CSV 供 Excel 開啟", "已完成",
        acs=[("AC-1", "`export_csv` 輸出含標題列的 CSV — 檢查方式：`python3 -m unittest test_export_csv -v`"),
             ("AC-2", "在 Windows 實機用 Excel 開啟匯出檔，中文標題不亂碼 — 檢查方式：手動開啟並截圖")],
        steps=[("✅", "**AC-1** — 完成證據：`python3 -m unittest test_export_csv -v` exit 0，1 test OK（2026-10-08）"),
               ("✅", "**AC-2** — 待 Windows 實機")],
        proof=[("AC-1", "PASS", "`python3 -m unittest test_export_csv -v` exit 0"), ("AC-2", "未執行", "尚無 Windows 實機")],
        tbd=[("TBD-1", "Windows 實機驗證", "不影響本次交付",
              "結論：追蹤：無。理由：多數使用者用 Linux，實機驗證不重要。2026-10-09")],
        created="2026-10-06",
        timeline=[("2026-10-06", "建立"), ("2026-10-08", "合併 issue-2118-export-csv 進 main，標記已完成")]))
    commit(p, "docs: 回寫 issue-2118 結案紀錄", "2026-10-09")


def build_scan(kit, out):
    p = out / "scan"
    base(kit, p, SCAN_LEVELS)
    write(p / "tools/platform.py", PLATFORM_PY)
    commit(p, "chore: 加入平台查詢命令", "2026-09-26")
    pass_proof = [("AC-1", "PASS", "`python3 -m unittest -v` exit 0")]
    ac1 = [("AC-1", "依需求完成可觀察行為 — 檢查方式：`python3 -m unittest -v`")]
    done_steps = [("✅", "**AC-1** — 完成證據：`python3 -m unittest -v` exit 0（合併前）")]
    todo_step = [("⏳", "**AC-1** — 驗證方式：`python3 -m unittest -v`")]

    def pending(issue_id, readme, date):
        write(p / f"docs/issues/issue-{issue_id}/README.md", readme)
        commit(p, f"docs: 建立 issue-{issue_id}\n\nRefs: #{issue_id}", date)

    # 2201 必要驗收未執行、無豁免
    simple_feature(p, "2201", "done-filter", "only_done", 'i["done"]', [1], "2026-10-03", small(
        "2201", "列出已完成項目", "已完成",
        acs=ac1 + [("AC-2", "發版後在使用者環境確認篩選結果正確 — 檢查方式：使用者回報截圖")],
        steps=done_steps + [("✅", "**AC-2** — 待使用者環境")],
        proof=pass_proof + [("AC-2", "未執行", "尚未取得使用者環境")], created="2026-10-01",
        timeline=[("2026-10-01", "建立"), ("2026-10-03", "合併進 main，標記已完成")]))
    # 2202 已合併，狀態仍為審查中
    simple_feature(p, "2202", "pending-filter", "only_pending", 'not i["done"]', [2], "2026-10-04", small(
        "2202", "列出未完成項目", "審查中", acs=ac1, steps=done_steps, proof=pass_proof,
        created="2026-10-02", timeline=[("2026-10-02", "建立")]))
    # 2203 README 終態、平台 open
    simple_feature(p, "2203", "title-filter", "with_title", 'i["title"]', [1], "2026-10-05", small(
        "2203", "過濾空白標題", "已完成", acs=ac1, steps=done_steps, proof=pass_proof,
        created="2026-10-02", timeline=[("2026-10-02", "建立"), ("2026-10-05", "合併進 main，標記已完成")]))
    # 2204 已完成，平台無權限讀取
    simple_feature(p, "2204", "id-filter", "positive_id", 'i["id"] > 0', [1, 2], "2026-10-05", small(
        "2204", "排除非法 id", "已完成", acs=ac1, steps=done_steps, proof=pass_proof,
        created="2026-10-03", timeline=[("2026-10-03", "建立"), ("2026-10-05", "合併進 main，標記已完成")]))
    # 2206 專案規則 1：⏳ 但步驟內已有完成證據
    simple_feature(p, "2206", "short-title", "short_title", 'len(i["title"]) < 50', [1, 2], "2026-10-06", small(
        "2206", "過濾過長標題", "已完成", acs=ac1,
        steps=[("⏳", "**AC-1** — 完成證據：`python3 -m unittest -v` exit 0，2 tests OK（2026-10-06）")],
        proof=pass_proof, created="2026-10-04",
        timeline=[("2026-10-04", "建立"), ("2026-10-06", "合併進 main，標記已完成")]))
    # 2207 legacy 排除規則與未豁免必要驗收衝突
    simple_feature(p, "2207", "legacy-import", "legacy_ok", 'isinstance(i["id"], int)', [1, 2], "2026-10-06", small(
        "2207", "舊版資料匯入相容", "已完成",
        acs=ac1 + [("AC-2", "以正式環境的舊版 todo.json 匯入後筆數一致 — 檢查方式：比對匯入前後筆數")],
        steps=done_steps + [("✅", "**AC-2** — 待正式資料")],
        proof=pass_proof + [("AC-2", "未執行", "尚未取得正式環境資料")], tag="legacy", created="2026-10-04",
        timeline=[("2026-10-04", "建立"), ("2026-10-06", "合併進 main，標記已完成")]))
    # 2208 有明確豁免
    simple_feature(p, "2208", "unicode-title", "nonempty", 'i["title"].strip()', [1], "2026-10-07", small(
        "2208", "標題 Unicode 正規化", "已完成",
        acs=ac1 + [("AC-3", "macOS 上輸入的組合字顯示正常 — 檢查方式：macOS 手動輸入")],
        steps=done_steps + [("✅", "**AC-3** — 已豁免")],
        proof=pass_proof + [("AC-3", "未執行", "見 Gate 豁免紀錄")],
        waiver="- 2026-10-07：豁免 AC-3 macOS 手動驗證。使用者原話：「沒有 Mac，AC-3 先豁免，我接受風險」。殘餘風險：macOS 組合字可能顯示異常。",
        created="2026-10-05", timeline=[("2026-10-05", "建立"), ("2026-10-07", "合併進 main，標記已完成")]))
    # 2209 純文件交付，已合併但狀態審查中
    run(p, "git", "checkout", "-q", "-b", "issue-2209-user-guide")
    write(p / "docs/user-guide.md", "# 使用手冊\n\n## 新增與完成\n\n`python3 todo.py add 買牛奶` 後以 `python3 todo.py done 1` 標記完成。\n")
    write(p / "docs/issues/issue-2209/README.md", small(
        "2209", "撰寫使用手冊", "審查中",
        acs=[("AC-1", "`docs/user-guide.md` 說明新增與完成流程 — 檢查方式：人工對照指令")],
        steps=[("✅", "**AC-1** — 完成證據：人工對照 `todo.py` 指令一致（2026-10-08）")],
        proof=[("AC-1", "PASS", "人工對照")], created="2026-10-07", timeline=[("2026-10-07", "建立")]))
    commit(p, "docs: 新增使用手冊\n\nRefs: #2209", "2026-10-08")
    run(p, "git", "checkout", "-q", "main")
    run(p, "git", "merge", "-q", "--no-ff", "issue-2209-user-guide", "-m", "Merge branch 'issue-2209-user-guide' (issue-2209)", date="2026-10-08")
    # 2210 只合併 issue 佔位紀錄
    run(p, "git", "checkout", "-q", "-b", "issue-2210-tags")
    write(p / "docs/issues/issue-2210/notes.md", "# issue-2210 筆記\n\n初步調查：標籤以逗號分隔。\n")
    write(p / "docs/issues/issue-2210/README.md", small(
        "2210", "項目標籤", "待實作", acs=ac1, steps=todo_step, created="2026-10-08",
        timeline=[("2026-10-08", "建立")]))
    commit(p, "docs: issue-2210 規格與調查筆記\n\nRefs: #2210", "2026-10-09")
    run(p, "git", "checkout", "-q", "main")
    run(p, "git", "merge", "-q", "--no-ff", "issue-2210-tags", "-m", "Merge branch 'issue-2210-tags' (issue-2210)", date="2026-10-09")
    # 2211 必要驗收未執行，平台狀態未知
    simple_feature(p, "2211", "dedupe", "unique_title", 'i["title"] != ""', [1], "2026-10-09", small(
        "2211", "空白標題提示", "已完成",
        acs=ac1 + [("AC-2", "使用者以實際清單操作一週無誤報 — 檢查方式：使用者回報")],
        steps=done_steps + [("✅", "**AC-2** — 待使用者回報")],
        proof=pass_proof + [("AC-2", "未執行", "尚未取得使用者回報")], created="2026-10-07",
        timeline=[("2026-10-07", "建立"), ("2026-10-09", "合併進 main，標記已完成")]))
    # 2213 等待外部驗收窗，發版事件已發生
    simple_feature(p, "2213", "priority", "high_priority", 'i.get("priority", 0) >= 0', [1, 2], "2026-10-05", small(
        "2213", "優先度欄位", "等待外部驗收窗",
        acs=ac1 + [("AC-2", "正式發版後，使用者以發版產物確認優先度排序 — 檢查方式：使用者回報")],
        steps=done_steps + [("⏳", "**AC-2** — 窗口：下一次正式發版（main 上出現新的 `v*` tag）；判準：使用者以該版確認排序")],
        proof=pass_proof + [("AC-2", "未執行", "等待發版")], created="2026-10-03",
        timeline=[("2026-10-03", "建立"), ("2026-10-05", "合併進 main；AC-2 待發版，轉入等待外部驗收窗")]))
    # 2216 已合併、狀態仍審查中，AC-2 未執行無豁免（審查 ca51b4b 後新增）
    simple_feature(p, "2216", "title-trim", "trimmed", 'i["title"] == i["title"].strip()', [1, 2], "2026-10-09", small(
        "2216", "標題去除前後空白", "審查中",
        acs=ac1 + [("AC-2", "以使用者的實際清單確認去除空白後沒有標題被誤改 — 檢查方式：使用者回報")],
        steps=done_steps + [("⏳", "**AC-2** — 待使用者回報")],
        proof=pass_proof + [("AC-2", "未執行", "尚未取得使用者回報")], created="2026-10-08",
        timeline=[("2026-10-08", "建立")]))
    # 2217 已合併、等待外部驗收窗、窗口未到；2218 窗口事件無法判斷（審查 2e348b1 後新增）
    simple_feature(p, "2217", "sort-done", "done_last", 'True', [1, 2], "2026-10-10", small(
        "2217", "已完成項目排在最後", "等待外部驗收窗",
        acs=ac1 + [("AC-2", "使用者以實際清單操作兩週後確認排序符合習慣 — 檢查方式：使用者回報")],
        steps=done_steps + [("⏳", "**AC-2** — 窗口：2026-11-15 起由使用者回報兩週使用結果；判準：使用者確認排序符合習慣")],
        proof=pass_proof + [("AC-2", "未執行", "等待 2026-11-15 的窗口")], created="2026-10-09",
        timeline=[("2026-10-09", "建立"), ("2026-10-10", "合併進 main；AC-2 待 2026-11-15 的窗口，轉入等待外部驗收窗")]))
    simple_feature(p, "2218", "archive", "archived", 'True', [1, 2], "2026-10-11", small(
        "2218", "封存已完成項目", "等待外部驗收窗",
        acs=ac1 + [("AC-2", "合作團隊完成內部導入後確認封存結果可讀 — 檢查方式：合作團隊回報")],
        steps=done_steps + [("⏳", "**AC-2** — 窗口：合作團隊完成內部導入（以對方通知為準）；判準：對方確認封存結果可讀")],
        proof=pass_proof + [("AC-2", "未執行", "等待合作團隊導入")], created="2026-10-10",
        timeline=[("2026-10-10", "建立"), ("2026-10-11", "合併進 main；AC-2 待合作團隊導入，轉入等待外部驗收窗")]))
    # 尚未合併的 issue
    pending("2212", small("2212", "雲端同步", "審查中", acs=ac1, steps=todo_step, created="2026-10-02",
                          timeline=[("2026-10-02", "建立")]), "2026-10-02")
    run(p, "git", "tag", "-a", "v1.1.0", "-m", "v1.1.0", date="2026-10-10")
    pending("2205", small("2205", "支援刪除項目", "待實作", acs=ac1, steps=todo_step, created="2026-10-10",
                          timeline=[("2026-10-10", "建立")]), "2026-10-10")
    pending("2214", small("2214", "顏色輸出", None, acs=ac1, steps=todo_step, created="2026-10-11",
                          timeline=[("2026-10-11", "建立")]), "2026-10-11")
    pending("2215", small("2215", "提醒通知", "待實作", acs=ac1, steps=todo_step, created="2026-10-11",
                          tbd=[("TBD-1", "通知管道用桌面通知還是 email", "待確認", "影響 AC-1 的可觀察結果")],
                          timeline=[("2026-10-11", "建立")]), "2026-10-11")


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if out.exists():
        sys.exit(f"{out} 已存在")
    out.mkdir(parents=True)
    build_questions(kit, out)
    build_track(kit, out)
    build_scan(kit, out)
    print(out)


if __name__ == "__main__":
    main()
