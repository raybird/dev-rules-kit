# Issue 2 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)，記帳區段與凍結內容依 [README 的設計邊界](README.md#設計邊界)。本檔是唯一任務與執行證據來源。2026-11-03 使用者回覆「核准」，核准 README 中 SCN-001～006 及本計畫。S1、S2 可執行，S3 等 S1，S4 等 S2、S3，S5 等 S4。

### verify-artifact.py 判定

介面：`--reviewed`、`--head` 必填；`--artifact`（本機報告）與 `--issue`（issue 目錄，報告在平台時使用）至少一個，兩者都給時必須指向同一個 issue。

1. 讀被審查提交上的 `docs/AGENTS.md` 流程契約（實作時由 HEAD 改為被審查提交，與 review-evidence.md 一致）。讀不到、低於 2.4 或 major 不是 2 時走現行判定（恰好一個只新增該報告的提交），無效訊息附註新判定需要 2.4 以上的 2.x；現行判定下 `--issue` 只在 HEAD 等於被審查提交時有效。
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

沒有輸出或結果不在被審查提交的祖先內時，判定缺少核准基線。報告新增欄位「核准基線」，核准 commit 為 `待提交` 時必填，記錄推導出的 SHA 與推導方式。（S3 實作時另要求 ref 上仍有核准來源欄位行；S6 依審查把 pattern 錨定在行首欄位。）

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | 依上方判定修改 `verify-artifact.py`，在 `test-evidence.py` 補正負向案例 | SCN-001～003 已核准 | SCN-001～003 | 下方「腳本案例」全部通過，既有 6 個測試不變仍通過；每個負向案例的訊息指出違規位置 | ✅ 2026-11-03；見「S1 證據」 |
| S2 | 建立 WF-28 fixture，以 v4.8.1 規則在隔離設定實跑基準 | SCN-006 已核准；與 S1 無相依 | SCN-006 | 記錄只為回填或記帳的提交數、因記帳觸發的重審次數、環境與完整輸出；fixture 與固定回答先提交再實跑 | ✅ 2026-11-03；見「S2、S4 證據」 |
| S3 | 修改 review-evidence.md、acceptance.md、readme-templates.md、review SKILL.md 與 docs/AGENTS.md 版本；檢查 execute-task、create-pr、dev-cycle、README、usage 的引用（依 writing-rules） | S1；SCN-001、004、005 已核准 | SCN-001、004、005 | 規則文字與腳本判定一致，沒有自相矛盾的舊句；文件版本 2.8、流程契約 2.4；有語意落差的引用已同步 | ✅ 2026-11-03；見「S3 證據」 |
| S4 | 以本次規則對同一 fixture 實跑候選組與對照組，重跑 WF-14 | S2、S3 | SCN-004～006，覆核 SCN-001～003 | 依下方「行為案例」逐項判定；任一語意變更沿用 PASS 即判回歸失敗並回到原因修正 | ⚠️ 部分完成 2026-11-03；見「S2、S4 證據」。沒有語意變更沿用 PASS；完成判準中 WF-14 重跑、28c 的 reviewer 端與刪除核准來源行的對照組未達成，reviewer 端改由 S7 的 28e 補上 |
| S5 | 更新 CHANGELOG（v4.9.0）、workflow-regression、rule-verification-status 與回歸紀錄；跑根目錄五項檢查；送獨立審查 | S4 | SCN-001～006 | 五項檢查通過；未實跑分支登記為僅靜態撰寫；獨立審查 PASS 或已依使用者決定處理 | 🔄 第一次審查 [review-c77928c](review-c77928c.md) RETURN，經 S6、S7 處理後送覆審 |
| S6 | 依 review-c77928c 修正：review 技能步驟 5 隨報告回填、推導 pattern 錨定、`verify-artifact.py` 收緊非範本寫法與其他放行路徑、技能附 2.3 以下的章節名稱、回歸紀錄與驗證狀態更正 | S5 審查 | SCN-001～005 | 審查列出的 MUST FIX、SHOULD FIX 都有修正與證據；新增測試先紅後綠；reviewer 的對抗腳本改判無效 | ✅ 2026-11-03；見「S6 證據」 |
| S7 | 以最終規則重跑候選 28a、28b、28c、28d，新增 28b3、28e；基準組跑 28d 第二輪與 28e | S6；判定先提交（`aa6e624`） | SCN-004～006 | 依 expected.md「審查後重跑」逐項判定 | ✅ 2026-11-03；見「S7 證據」，28b3 依判準為無法區分 |

### S1 證據

2026-11-03，對應 SCN-001～003。腳本是 production code，測試以 `test-evidence.py` 在拋棄式 Git repo 跑真實命令；腳本判定沒有另一層外部行為，外迴圈與單元紅燈合併為同一組（agent 行為另由 S4 實跑）。

| 段落 | 命令與結果 | 紀錄 |
|---|---|---|
| 紅燈 | 舊版 `verify-artifact.py` 跑 `python3 scripts/test-evidence.py`：69 個測試 31 個失敗、0 個錯誤，exit 1。失敗原因是現行判定拒絕記帳提交、無效訊息沒指出違規位置、不支援 `--issue`、2.3 專案沒有提示需要 2.4；原本 6 個測試仍通過 | [s1-red.txt](evidence/s1-red.txt) |
| 綠燈 | 新版跑同一組：69 個全過；根目錄五項檢查與 `py_compile` 全部 exit 0 | [s1-green.txt](evidence/s1-green.txt) |
| 判定訊息 | 每個案例的實際訊息：2.4 的 27 次判定、2.3 的 28 次判定，負向案例都指出違規的路徑、章節或欄位 | [s1-messages.txt](evidence/s1-messages.txt) |
| 精煉 | no-op：腳本結構與上方六個判定步驟一一對應，沒有分歧的重複邏輯；綠燈即最終狀態 | — |

已知限制：README 標題名稱與範本不同的下游，該節一律視為凍結（只會更嚴）；記帳章節內的縮排程式碼區塊不視為 code fence，內容可自由修改，讀者只從驗收章節的 fence 取得 Gherkin。

### S3 證據

2026-11-03，對應 SCN-001、004、005。規則文字依 writing-rules 修改；agent 是否照做由 S4 實跑，本步只取得靜態與命令證據。

| 檔案 | 變更 |
|---|---|
| `docs/agents/review-evidence.md` | 「本機 artifact 提交後的有效性」改名「審查之後的提交」：2.4 起三項條件與凍結內容，2.3 以下維持單一報告提交；報告欄位新增核准基線 |
| `docs/agents/acceptance.md` | 核准 commit 在下一個本來就要做的提交回填；`待提交` 時的推導命令（放在原比對命令之後，`test-evidence.py` 依序取用兩段命令）；刪除核准來源行也算缺少基線 |
| `docs/agents/readme-templates.md` | 兩處核准 commit 說明補上回填時機 |
| `skills/review/SKILL.md` | 步驟 3 推導基線、步驟 5 改用新判定與 `--issue`、報告範本加核准基線 |
| `skills/dev-cycle/SKILL.md` | 第 44 行原本要求記錄 `需決策` 後一律重新 review，正是本 issue 的連鎖來源；改為原判定 PASS 且判定有效時沿用，RETURN 仍重審 |
| `docs/usage.md` | 審查有效性的說明改為 2.4／2.3 兩種判定 |
| `docs/AGENTS.md` | 文件版本 2.8、流程契約 2.4、修訂紀錄 |

`create-pr`、`execute-task`、根目錄 README、INSTALL.md 沒有描述這兩條規則的句子，不需修改。

| 證據 | 結果 | 紀錄 |
|---|---|---|
| 推導命令紅燈 | 以 HEAD 的 acceptance.md（沒有推導命令）跑新增的兩個推導測試：2 個失敗，原因是缺少該命令，exit 1 | [s3-baseline-red.txt](evidence/s3-baseline-red.txt) |
| 綠燈 | 推導測試執行文件中的字面命令：核准後的記帳提交不改變基線、重新核准移到新提交、以被審查提交為 ref 時不受之後的提交影響、沒有核准來源行時無輸出；刪除該行的提交也會被找到，因此規則另要求 ref 上仍有該行。根目錄五項檢查 exit 0，`test-evidence.py` 75 個測試通過 | [s3-green.txt](evidence/s3-green.txt) |

### S2、S4 證據

2026-11-03，對應 SCN-006，覆核 SCN-001、004、005。案例與判定在實跑前寫定於 [expected.md](fixtures/expected.md)（`8eec4de`；28d 於看過 28a、28c 結果後追加，`6874d9a`），結果與環境見 [2026-11-03 回歸紀錄](../../workflow-results/2026-11-03.md)，每輪完整輸出見 [evidence/s2-baseline/](evidence/s2-baseline/) 與 [evidence/s4-candidate/](evidence/s4-candidate/)。

| 指標 | 基準組（v4.8.1） | 候選組（2.4） |
|---|---|---|
| 單獨回填提交（28a＋28c＋28d） | 1（28d） | 0 |
| 記帳觸發的重審（28b） | 1 | 0 |
| 語意變更沿用 PASS（28b2） | — | 0（檢查器 INVALID 後重審） |

候選組五個案例都符合判定，SCN-006 通過。與上方「行為案例」表的差異：28a 改為規格尚未提交；28c 改為實作前推導基線，reviewer 端的推導只在 28b2 觀察到；28c 刪除核准來源行的對照組與 WF-14 沒有 agent 實跑，只有腳本測試；每案例每組一輪。觀察到的偏差（28b2 沒有隨報告提交回填、fixture 的 PASS 報告本身有誤）記在回歸紀錄「觀察」。

### S6 證據

2026-11-03，對應 [review-c77928c](review-c77928c.md) 的 MUST FIX 1、SHOULD FIX 3～5 與 NICE TO HAVE 7～13；MUST FIX 2、SHOULD FIX 6 屬紀錄更正，見回歸紀錄與驗證狀態。

| 段落 | 命令與結果 | 紀錄 |
|---|---|---|
| 紅燈 | 修正前的 `verify-artifact.py` 與 acceptance.md（`de2e1f9`）跑新增測試：96 個測試 20 個失敗，exit 1。失敗原因是非範本寫法的欄位、標題與 fence 被放行，記帳章節可重排或重複，核准 commit 接受 SHA 加尾隨文字，`diff.relative` 加子目錄 `--repo` 時 `--issue` 回報「無變更」，3.0 走新判定，推導命令選中提到欄位名的 Timeline 提交 | [s6-red.txt](evidence/s6-red.txt) |
| 綠燈 | 修正後 99 個測試全過，exit 0；另加的「整節刪除待確認事項」正向測試守住 review-evidence.md 的既有規則（修正前本來就通過，非紅燈測試） | [s6-green.txt](evidence/s6-green.txt) |
| 對抗腳本 | reviewer 留在 scratchpad 的對抗腳本以新版重跑：列為放行的寫法都改判無效；仍放行的只有已揭露的縮排程式碼區塊、非粗體純文字行與只改檔案模式；2.3 與無契約下新舊腳本 10 種情境結果相同 | 回歸紀錄「審查後修正與重跑」 |
| 精煉 | no-op：新增判定集中在 `analyse()` 與標題順序檢查，沒有分歧的重複邏輯 | — |

### S7 證據

2026-11-03，對應 SCN-004～006。判定與新增案例在實跑前寫定（`aa6e624`），結果、SCN-006 綜合對照與未覆蓋項見 [2026-11-03 回歸紀錄](../../workflow-results/2026-11-03.md)「審查後修正與重跑」，每輪輸出與檢查器實際輸出見 [evidence/s7-rerun/](evidence/s7-rerun/)。候選組所有案例符合判定，28b3 依判準為無法區分（協調者同時改了計畫檔）；28e 證實 reviewer 端推導基線與隨報告回填。

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
- [x] S1 腳本案例全部通過後才改規則文字
- [x] 規則文字、範本與 review 技能對同一判定沒有兩種說法
- [x] 基準與候選實跑紀錄齊全，未實跑分支登記為僅靜態撰寫
- [x] CHANGELOG 與 docs/AGENTS.md 版本一致，下游更新方式寫明
