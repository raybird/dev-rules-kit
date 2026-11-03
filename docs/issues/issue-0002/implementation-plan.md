# Issue 2 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)，記帳區段與凍結內容依 [README 的設計邊界](README.md#設計邊界)。本檔是唯一任務與執行證據來源。2026-11-03 使用者回覆「核准」，核准 README 中 SCN-001～006 及本計畫。S1、S2 可執行，S3 等 S1，S4 等 S2、S3，S5 等 S4。

### verify-artifact.py 判定

介面：`--reviewed`、`--head` 必填；`--artifact`（本機報告）與 `--issue`（issue 目錄，報告在平台時使用）至少一個，兩者都給時必須指向同一個 issue。

1. 讀目前 HEAD 的 `docs/AGENTS.md` 流程契約。讀不到或低於 2.4 時走現行判定（恰好一個只新增該報告的提交），無效訊息附註新判定需要 2.4；現行判定需要 `--artifact`。
2. 2.4 以上：被審查提交必須是 HEAD 的祖先，範圍內沒有 merge 提交。
3. 以 `git diff --no-renames --name-status` 取淨差異：只允許新增 `--artifact` 指定的報告（一般檔案、含相符的 Reviewed HEAD SHA）與修改該 issue 的 `README.md`；其他路徑一律無效。
4. README 比對：在 code fence 之外以 `## ` 標題切節，產生兩個版本的凍結內容並逐行比較——非記帳章節的全部行（含標題本身）、所有 code fence 內容、任何章節的粗體欄位行；`**狀態**` 與 `**核准 commit**` 兩個欄位只比欄位名稱與數量，值另外檢查。
5. `**核准 commit**` 的值改變時，舊值必須以 `待提交` 開頭，新值必須以可解析的 SHA 開頭，且該提交是被審查提交本身或其祖先。
6. 有效時列出變更的記帳章節、欄位與核准 commit 的新舊值；無效時指出第一個違規的路徑、章節或欄位。指令維持唯讀。

### 回填與基線

`待提交` 時的基線命令（reviewer 與 execute-task 共用，寫入 acceptance.md）：

```bash
git log -1 --format=%H -G '\*\*核准來源\*\*' "${reviewed_sha}" -- "docs/issues/issue-${issue_id}/README.md"
```

沒有輸出或結果不在被審查提交的祖先內時，判定缺少核准基線。報告新增選填欄位「核准基線」，記錄推導出的 SHA 與推導方式。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | 依上方判定修改 `verify-artifact.py`，在 `test-evidence.py` 補正負向案例 | SCN-001～003 已核准 | SCN-001～003 | 下方「腳本案例」全部通過，既有 6 個測試不變仍通過；每個負向案例的訊息指出違規位置 | ✅ 2026-11-03；見「S1 證據」 |
| S2 | 建立 WF-28 fixture，以 v4.8.1 規則在隔離設定實跑基準 | SCN-006 已核准；與 S1 無相依 | SCN-006 | 記錄只為回填或記帳的提交數、因記帳觸發的重審次數、環境與完整輸出；fixture 與固定回答先提交再實跑 | 📝 待實作 |
| S3 | 修改 review-evidence.md、acceptance.md、readme-templates.md、review SKILL.md 與 docs/AGENTS.md 版本；檢查 execute-task、create-pr、dev-cycle、README、usage 的引用（依 writing-rules） | S1；SCN-001、004、005 已核准 | SCN-001、004、005 | 規則文字與腳本判定一致，沒有自相矛盾的舊句；文件版本 2.8、流程契約 2.4；有語意落差的引用已同步 | 📝 待實作 |
| S4 | 以本次規則對同一 fixture 實跑候選組與對照組，重跑 WF-14 | S2、S3 | SCN-004～006，覆核 SCN-001～003 | 依下方「行為案例」逐項判定；任一語意變更沿用 PASS 即判回歸失敗並回到原因修正 | 📝 待實作 |
| S5 | 更新 CHANGELOG（v4.9.0）、workflow-regression、rule-verification-status 與回歸紀錄；跑根目錄五項檢查；送獨立審查 | S4 | SCN-001～006 | 五項檢查通過；未實跑分支登記為僅靜態撰寫；獨立審查 PASS 或已依使用者決定處理 | 📝 待實作 |

### S1 證據

2026-11-03，對應 SCN-001～003。腳本是 production code，測試以 `test-evidence.py` 在拋棄式 Git repo 跑真實命令；腳本判定沒有另一層外部行為，外迴圈與單元紅燈合併為同一組（agent 行為另由 S4 實跑）。

| 段落 | 命令與結果 | 紀錄 |
|---|---|---|
| 紅燈 | 舊版 `verify-artifact.py` 跑 `python3 scripts/test-evidence.py`：69 個測試 31 個失敗、0 個錯誤，exit 1。失敗原因是現行判定拒絕記帳提交、無效訊息沒指出違規位置、不支援 `--issue`、2.3 專案沒有提示需要 2.4；原本 6 個測試仍通過 | [s1-red.txt](evidence/s1-red.txt) |
| 綠燈 | 新版跑同一組：69 個全過；根目錄五項檢查與 `py_compile` 全部 exit 0 | [s1-green.txt](evidence/s1-green.txt) |
| 判定訊息 | 每個案例的實際訊息：2.4 的 27 次判定、2.3 的 28 次判定，負向案例都指出違規的路徑、章節或欄位 | [s1-messages.txt](evidence/s1-messages.txt) |
| 精煉 | no-op：腳本結構與上方六個判定步驟一一對應，沒有分歧的重複邏輯；綠燈即最終狀態 | — |

已知限制：README 標題名稱與範本不同的下游，該節一律視為凍結（只會更嚴）；記帳章節內的縮排程式碼區塊不視為 code fence，內容可自由修改，讀者只從驗收章節的 fence 取得 Gherkin。

## 使用方式對照

| 情境 | 變更前 | 變更後 |
|---|---|---|
| PASS 後記下使用者對 `需決策` 的答案並保存報告 | 報告與記錄必須分開，記錄提交讓 PASS 失效 | 報告與記錄可同一個提交；`verify-artifact.py` 有效並列出變更章節 |
| 規格核准後第一次提交 | 下一步常是只改一行的回填提交 | 回填寫進第一個實作提交 |
| 送審時核准 commit 仍為 `待提交` | 視為缺核准基線，或先補一個回填提交 | reviewer 依核准來源行推導基線並記在報告，回填隨報告提交 |

## 測試策略

腳本判定以 `test-evidence.py` 在拋棄式 Git repo 實跑真實命令；agent 是否照新規則少開提交、是否仍在語意變更時重審，只能以宿主新 session 實跑驗證，靜態檢查與腳本測試不能代替（根目錄 AGENTS.md）。實跑沿用隔離設定：以 scratchpad 為 HOME 安裝工作樹技能，`CLAUDE_CONFIG_DIR` 指向該處，不動全域技能；測試 agent 只收到 fixture 與使用者輸入，不給預期答案。

### 腳本案例（S1）

| 類型 | 案例 |
|---|---|
| 有效（2.4） | 報告＋Timeline＋待確認事項＋狀態＋核准 commit 由待提交改成 R，一個提交；同樣內容分三個提交；新增整節 Gate 豁免紀錄；`--issue` 平台模式只改記帳章節；只新增報告 |
| 無效（2.4） | Gherkin 步驟改一字；Small 的 AC 改字；核准表狀態或核准來源改動；Timeline 節內的 `**風險**`／`**分級**` 改動；插入 `## Timeline` 標題吞掉凍結內容；把 Gherkin 搬到 Timeline 底下；Timeline 內新增或修改 code fence；implementation-plan.md、evidence、其他 issue 或 issue 目錄外檔案改動；修改既有報告；核准 commit 由 SHA 改成另一個 SHA；待提交改成不是 R 祖先的提交；範圍含 merge；R 不在 HEAD 祖先；報告是 symlink 或 Reviewed HEAD SHA 不符 |
| 現行判定（2.3、無 AGENTS.md） | 只動記帳章節的提交判定無效並附註需要 2.4；只新增報告仍有效 |

### 行為案例（S2、S4）

| 案例 | 準備與輸入 | 判定 |
|---|---|---|
| WF-28a 回填 | Medium issue 規格已核准並提交、核准 commit 為 `待提交`，一個小型已核准 Task；輸入「繼續處理 issue」 | 計算只改核准 commit 的提交數；候選組回填併入實作提交，實作前以正確基線比對 |
| WF-28b 記帳 | 被審查提交 R 已有 PASS 報告（未提交），報告一項 SHOULD FIX 標 `需決策`；輸入「照建議，追蹤到下一個 issue」 | 計算因記帳觸發的重審；候選組把報告、決策與回填放進提交後 `verify-artifact.py` 有效、不重審；對照組的答案需要改 AC 文字，候選組仍要求重審 |
| WF-28c 基線 | 被審查提交上核准 commit 為 `待提交`；呼叫 review | 報告記錄推導出的核准基線；對照組刪除核准來源行，判定缺少核准基線 |
| WF-14 | 既有案例 | 純報告提交仍有效，同次改程式、修改既有報告或 symlink 仍需重審 |

基準組與候選組使用同一份 fixture、固定回答、工具權限與宿主設定，版本差異只限本次規則與必要引用；同一輸入結果不一致時明列為不穩定，不挑成功輪次。

### 文件與腳本檢查

```bash
python3 scripts/check-kit.py
python3 scripts/check-links.py
bash -n scripts/install.sh
python3 scripts/test-install.py
python3 scripts/test-evidence.py
```

## 檢查清單

- [x] SCN-001～006 已核准，TBD-3 已解決
- [ ] S1 腳本案例全部通過後才改規則文字
- [ ] 規則文字、範本與 review 技能對同一判定沒有兩種說法
- [ ] 基準與候選實跑紀錄齊全，未實跑分支登記為僅靜態撰寫
- [ ] CHANGELOG 與 docs/AGENTS.md 版本一致，下游更新方式寫明
