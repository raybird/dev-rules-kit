# 審查報告

- 審查日期：2026-10-16
- 範圍：最新單一 commit 的局部 diff，完整查核 11 個異動檔案；不代表完整 PR 審查。
- Reviewed BASE SHA：`8baefa322b6b21373ae52d6281d45078911a2087`
- Reviewed HEAD SHA：`86dc980cdb3fa1e610260bac2a9a0b85b2b3b6f0`
- Reviewed patch-id：`70a7d1671a01974cb8056f06897dd73068c18f52`
- 獨立 reviewer：Codex 隔離子代理 `/root/review_latest`；未參與被審查提交的實作。
- Review artifact：`docs/reviews/review-86dc980.md`
- 路徑理由：使用者要求審查最新提交，沒有 issue ID 或指定 PR；沿用本機 `docs/reviews/`，不建立虛構 issue。
- 需求來源：使用者「根據最新 commit 審查」、commit message、CHANGELOG v4.7.0 與 WF-24。以下目標依這些來源推斷，不補造已核准的 AC 或核准來源。

## 問題與風險

### MUST FIX：P2 — 純文件交付被無條件排除於合併判定

位置：`skills/dev-cycle/references/pending-scan.md:13`。

「只含文件提交的分支不算已合併交付」以檔案類型直接否定真實交付，會排除合法的純文件 issue。現有 `docs/agents/verification.md:80` 明認純文件任務可用靜態或人工檢查驗收，`docs/agents/readme-templates.md:168` 也為這種任務提供證據寫法；`skills/dev-cycle/SKILL.md:31` 的一般 merged 分支沒有排除純文件。新的掃描規則因而與同一技能的推進判斷分歧。

可重複的靜態契約查核：

1. 一個 issue 的核准目標只有更新使用手冊，PR 只修改實際交付的文件與 issue 紀錄，已真正 merged，驗收及步驟皆有完成證據。
2. README 的狀態仍是 `待實作`，尚待補結案紀錄；project.md 沒有另訂合併方式，平台 PR 已提供 merged 事實。
3. 依新增第 13 行，該文件分支不能算已合併交付，第 22 行的「已合併未結案」因而不成立。即使另因第 21 行被列為「非核心狀態」，仍丟失真正該補的合併與結案依據；一般推進卻會走 merged 結案分支。
4. 若舊狀態是合法的 `等待外部驗收窗`、原窗口尚未到且該觀察已逐項獲豁免，平台 issue 狀態未知、沒有其他待決項目，則連非核心狀態及窗口到期都不命中，可完全漏報已合併未結案。

建議：依 issue 的核准產出與實際交付判斷。只有 issue 佔位、進度或證據紀錄的提交不足以證明原需求已交付；核准目標本身是文件時，應接受真實 merged 與文件驗收證據。補上「只有 issue 佔位」及「純文件需求確實交付」兩組對照。此項為靜態契約衝突，未宣稱已實跑宿主誤判。

### MUST FIX：P2 — 非核心狀態判定把範本允許的正常進行狀態列成待校正

位置：`skills/dev-cycle/references/pending-scan.md:21`。

該列要求以「AGENTS.md 合法狀態集合」作排他白名單，但 `docs/AGENTS.md:141` 起的狀態表只定義 `等待外部驗收窗`、`不修復`、`已完成` 三種狀態，沒有一般實作階段的完整列舉。相對地，`docs/agents/readme-templates.md:188` 明確要求建立 issue 時填實際狀態，並以 `待實作` 為正確例子。新判定會把依既有範本正確建立的 issue 都視為非核心狀態，增加原本要降低的掃描雜訊；平台已關閉時還會依第 67 行建議另開一次性校正 issue。

可重複的靜態契約查核：

1. 使用現有 Small 範本建立一個 `**狀態**: 待實作` 的 issue；PR 未合併，沒有等待窗口或待確認事項，平台仍 open。
2. 依第 21 行查 AGENTS 的狀態表，`待實作` 不在三個值中，因此必定命中「非核心狀態」。
3. 對照範本第 188 行，該欄正符合既有規範，沒有需要校正的資料問題；BASE 的掃描規則也沒有此誤報類別。

建議：明確區分需要特殊 gate 的三種狀態與一般進行狀態；只有能證明違反實際狀態契約的值才列為非核心。若要採完整白名單，先在權威文件定義並同步範本，包含 project.md 的合法客製方式。補一個範本正常 `待實作` 不被列為異常的對照案例。修正此既有契約衝突不需新增使用者需求決策。

## 已查核維度

### 需求、相容性與證據

| 推斷目標 | 查核來源與結論 |
|---|---|
| 掃描規則集中、可登記唯讀命令 | dev-cycle 只保留入口並指向 pending-scan；JSON 的事實取得與 agent 分類分開，沒有新增執行器或重複掃描實作。WF-24 正向有執行命令摘要，命令失敗／格式錯誤分支明列未測。 |
| 平台 open／closed 與 README 雙向一致性 | 三類新條件及分段方式明確；未登記查詢時保留 unknown，沒有把缺資料當 closed。WF-24 以模擬平台查詢覆蓋，真實 GitHub／GitLab 未測。 |
| 起點及舊狀態降噪 | 起點前且非 open 只計數、open 仍展開，符合案例摘要；非核心狀態集合的契約衝突列 MUST FIX。 |
| 合併判定可登記、推測需揭露 | 先用 project 登記，否則平台 merged 優先，再用 Git merge commit 並標推測；WF-24 有推測型摘要。排除純文件分支過廣列 MUST FIX。 |
| 未執行與步驟、豁免 | AC／SCN 驗證列、未豁免條件及 📝／⏳ 步驟明列；限制揭露不算未執行。WF-24 只覆蓋部分分支，沒有把未測限制寫成完整通過。 |
| 待確認事項追蹤及流程契約 | 核心升為 2.3、dev-cycle 最低維持 2.2；舊版缺「追蹤：」只增加掃描結果，未要求重寫舊核准或改成已解決，與 CHANGELOG 的相容性說明一致。 |
| 地雷來源確認 | document-types 明寫打開證據確認；驗證狀態誠實保留僅靜態撰寫。 |
| project.md 範本提醒 | BASE 範本 SHA-256 為 `8cfc6f540a4273c69544b3f549d54c3a6950f5edc70ff41fb77e55ef540fac1a`，由協調者實算並傳入，與新增常數一致。未變更寫檔、衝突預檢及客製保留邏輯。 |

### 重要失敗面與邊界

| 輸入／狀態 | 預期、覆蓋與判定 |
|---|---|
| 已登記掃描命令，結果完整 | 採用命令事實並依規則分類；WF-24 正向有摘要。腳本未套起點、未讀豁免紀錄時，由該輪 agent 逐份複核補足，不能據此宣稱所有不完整輸出都會正確補救。 |
| 命令失敗／格式不符 | 回報錯誤並改 agent 掃描；規則明確，宿主分支未測。 |
| JSON 欄位缺漏 | 第 60 行保留 unknown；dev-cycle 第 12 行要求缺欄位回傳待處理事項，第 69 行要求全部判定過才能完成。應據此揭露無法判定，不能將未知陣列當作空陣列而宣告無懸置。本次未實跑此分支，不額外推論必然漏報。 |
| 平台未登記／只有平台 open issue | 前者 unknown 並揭露，後者列沒有 README；WF-24 正向與對照分別有摘要。 |
| 起點前且 closed／起點前但 open | closed 摺疊計數，open 仍展開；WF-24 有摘要，平台 unknown 的起點前資料依明文只計總數，這是掃描範圍選擇。 |
| 已完成但 AC 未執行／步驟仍 📝 | 未豁免者列待觀察；已有豁免不算未執行。WF-24 正向覆蓋 📝，先前 WF-23 有豁免摘要；非 AC 敘述排除仍缺專門 fixture。 |
| 正常待實作／真正自訂舊狀態 | 前者應保留正常進行狀態，後者才依明確契約判斷；現規則無法區分，列 MUST FIX。 |
| 已 merged 純文件需求／只有 issue 佔位紀錄 | 應依核准產出分辨交付；現規則一律排除，列 MUST FIX。 |
| 已 merged 且仍待外部觀察 | 主技能的生命週期順序未變，仍先保留等待，再由窗口分支執行及重新偵測；此提交沒有重引前次直接結案問題。 |

### 驗證結果與限制

協調者於 2026-10-16 在固定被審查 HEAD 執行並傳入以下結果；獨立 reviewer 未宣稱自行重跑：

| 命令 | 結果 |
|---|---|
| `python3 scripts/check-kit.py` | exit 0 |
| `python3 scripts/check-links.py` | exit 0 |
| `bash -n scripts/install.sh` | exit 0 |
| `python3 scripts/test-install.py` | exit 0；14 tests OK |
| `python3 scripts/test-evidence.py` | exit 0；6 tests OK |

另讀固定 HEAD 的 `docs/workflow-results/2026-10-16.md` 與 `docs/rule-verification-status.md`。WF-24 為隔離 Claude Code 2.1.301、`claude-opus-5-5`、每組新 session 一輪的摘要；被測內容為發布前未提交修訂，沒有固定到本次 HEAD 的完整內容指紋，fixture 與原始輸出也未永久保留。這限制證據持久力及重建性，本身不構成假綠燈或不實回報。已登記腳本的結果需 agent 補查，摘要也有明確揭露。該兩組未覆蓋上述正常進行狀態與真實純文件交付；靜態／Git fixture 全綠不能代替這些宿主行為證據。

### 架構、安全與品質

- 完整讀取 11 檔 diff，並對照 acceptance、verification、review-evidence、readme-templates 與 dev-cycle 生命週期。未有另外的 issue 核准材料，不補造核准結果。
- 掃描明列唯讀，未新增寫檔、刪除、外送訊息或權限提升。專案命令由 project.md 提供，未要求執行任意新安裝或改平台狀態。
- 依 code-simplify 標準查核整份 diff：偵測規則與版面集中於單一 reference，技能僅保留入口；歷史雜湊沿用小型集合，未發現額外抽象、跨 Task 重複實作或需要另列的過度設計。兩項 MUST FIX 屬行為契約分歧。
- 無 gate 豁免，亦無需使用者選擇需求邊界的新發現。修正後需對新固定範圍重新審查。
- 保存報告前確認 HEAD 仍為被審查 SHA，工作樹乾淨；本次只新增此報告，未修改產品或提交。

## 流程判定

**RETURN TO execute-task**：兩項 P2 MUST FIX。既有 repo checks 通過，但純文件交付與正常進行狀態的掃描規則仍與現行流程契約衝突。
