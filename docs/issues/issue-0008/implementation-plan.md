# Issue 8 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。S1～S3 可執行；S4 等 S1～S3；S5 等 S4。審查 PASS 後依 TBD-3 先在下游試用，再發布 v4.13.0。

### 部署

`init-project.py` 的部署清單由 `docs/AGENTS.md` 加上 `docs/agents/*.md` 與 `docs/_templates/*.md` 組成，成功後以目前清單重寫整份基線。改法只是從清單移除 `_templates`：

```diff
-    for folder in ('agents', '_templates'):
+    for folder in ('agents',):
```

舊基線多出的 `docs/_templates/` 條目只會被讀進 `previous`，不在清單裡就不會被比對，下次寫基線時自然消失；檔案本身不刪除。S1 以測試確認這個推論，不只靠讀程式。

### 範本與規範

- 三份範本以 `git mv` 搬到 `skills/execute-task/references/`，檔名與內容不變；`install.sh` 本來就複製整個技能目錄，不用改。
- `docs/AGENTS.md`：第 19 行的部署說明改成只部署 `docs/agents/`；「常青文件更新責任」補一句新建常青文件時可參考 execute-task 技能 `references/` 的範本；文件版本 2.12，流程契約不變（沒有技能依賴 `_templates`）。
- `document-types.md` 第 106 行：改成直接寫明順序與互動類的圖用 Mermaid，不再引用 `docs/_templates/`。
- `document-types.md`「常見文件類型範例」：移除【應客製】的 NOTE，改成「以下是範例；專案常用的組合登記在 project.md」。指向 project.md 的哪一節在 S3 依 writing-rules 決定，project.md 範本本身不動。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | `test-install.py`：初始化清單移除三份範本並斷言 `docs/_templates/` 不存在、基線不含其條目；新增案例：以含 `_templates` 條目的舊基線與舊檔建立暫存專案，跑 `--update --dry-run`、`--update`、`--check`。先紅，再改 `init-project.py` | SCN-001、002 已核准 | SCN-001、002 | 新案例先紅後綠；舊檔三份內容不變；dry-run 前後檔案樹相同；既有 test-install 案例全部通過 | ⏳ |
| S2 | `git mv` 三份範本到 `skills/execute-task/references/`；改 `docs/AGENTS.md`（部署說明、常青文件段落、文件版本 2.12、修訂紀錄）與 `document-types.md` 第 106 行；改 execute-task SKILL.md 回寫步驟。依 writing-rules | SCN-003、006 已核准 | SCN-003、006 | `git diff -M` 顯示三份為 100% 相似的改名；`grep -rn "_templates"` 只剩 CHANGELOG 與 `docs/issues/` 下的歷史文件；check-links OK | ⏳ |
| S3 | 改 `document-types.md`「常見文件類型範例」的 NOTE。依 writing-rules | SCN-004 已核准；與 S1、S2 無相依 | SCN-004 | 該節沒有「應客製」；`git diff` 中 `docs/agents/project.md` 沒有變動 | ⏳ |
| S4 | CHANGELOG v4.13.0 條目（下游更新：舊檔可手動刪除、刪除前先查專案自己文件的引用）；檢查 README.md、docs/usage.md、INSTALL.md、skills/README.md、rule-verification-status 有無需要跟著改的引用；跑根目錄五項檢查 | S1～S3 | SCN-005 | 五項檢查通過；CHANGELOG 條目涵蓋 SCN-005 兩點 | ⏳ |
| S5 | 送獨立審查（工具呼叫上限 30 次） | S4 | SCN-001～006 | PASS，或已依使用者決定處理 | ⏳ |

## 測試策略

- **SCN-001、002**：test-install.py 的暫存專案整合測試，屬可自動重跑的行為測試，先紅後綠。
- **SCN-003～006**：文件與檔案搬移，不改變腳本行為，以靜態檢查取得等價證據（verification.md「不改變可觀察行為的任務」）：`git diff -M` 的改名相似度、`grep` 的引用清單、check-kit 與 check-links。
- agent 是否在新建常青文件時讀到 references 的範本，靜態檢查無法證明；依 TBD-3 的下游試用觀察，未觸發時照實記為未觸發。

## 檢查清單

- [ ] 根目錄五項檢查通過
- [ ] `docs/agents/project.md` 沒有變動（PAST_TEMPLATES 不需新增）
- [ ] CHANGELOG 與 docs/AGENTS.md 修訂紀錄的日期為實際日期
- [ ] 下游試用結果記入 README `## 現況`（TBD-3）
