# Issue 3 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)，`## 現況` 的內容與記帳判定依 [README 的設計邊界](README.md#設計邊界)。本檔是唯一任務與執行證據來源。2026-11-10 使用者回覆「核准」，核准 README 中 SCN-001～008 及本計畫。S1、S3、S5 可執行，S2 等 S1，S4 等 S2，S6 等 S2～S5，S7 等 S6。

### verify-artifact.py 判定

沿用 issue #2 的區段判定，只加入 `## 現況`：

1. 被審查提交上的流程契約為 2.5 以上的 2.x 時，`現況` 加入可整節新增或刪除的記帳章節；2.4 時維持現行判定，`## 現況` 是一般凍結章節，新增時的無效訊息附註需要 2.5。
2. `## 現況` 節內：一般行、表格列與 `**現行 review**` 欄位屬記帳內容，`**現行 review**` 最多一行、值可改；標題、code fence、其他粗體開頭的行（含 `**現行 review:**` 這類非範本寫法）凍結，整節增刪時節內出現這些行即判無效（與待確認事項、Gate 豁免紀錄相同）。
3. `**現行 review**` 出現在 `## 現況` 之外時，當作一般粗體欄位凍結；`## 現況` 重複出現時判無效。
4. 有效時變更區段列出「現況」與現行 review 的新舊值；無效時指出第一個違規的章節與內容。指令維持唯讀。

### 規則文字的位置

- **rules（中英雙語）**：在「目標驅動執行與驗證」加一段「外部狀態以實查為準」；`##` 章節數與順序不變。
- **docs/AGENTS.md**：「Agent 工作流程與時序保留」補一項：issue 現況以 README 為唯一權威、`## 現況` 的用途與指向，以及交接文件、平台留言與記憶只寫 README 連結或錨定 commit 的事件（集中在這一項，不另改「待確認事項」的出口句）；核心介面列入 `## 現況` 與 `**現行 review**`。完整格式放 document-types.md 與 readme-templates.md，記帳判定放 review-evidence.md，AGENTS.md 只保留原則與指向。
- **project.md 範本**：「提交與交付」的合併判定方式擴充為外部狀態的查證命令（合併、推送、部署、平台 issue／PR）。既有專案的 project.md 不會被 `--update` 覆寫，CHANGELOG 寫明手動補登方式。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | 依上方判定修改 `verify-artifact.py`，在 `test-evidence.py` 補正負向案例 | SCN-001～003 已核准 | SCN-001～003 | 下方「腳本案例」全部通過，既有測試不變仍通過；每個負向案例的訊息指出違規位置；新案例先紅後綠 | ✅ 2026-11-10；見「S1 證據」 |
| S2 | 修改 review-evidence.md、review SKILL.md（步驟 5 保存報告時更新現行 review）、docs/AGENTS.md（原則、文件版本 2.9、流程契約 2.5、修訂紀錄）、document-types.md、readme-templates.md 兩種範本；依 writing-rules | S1；SCN-001、003、004、007 已核准 | SCN-001、003、004、007 | 規則文字與腳本判定一致，沒有自相矛盾的舊句；範本的 `## 現況` 位置與欄位與設計邊界相同 | ✅ 2026-11-10；見「S2 證據」 |
| S3 | 修改 rules/AGENTS.md 與 rules/AGENTS.zh-TW.md、project.md 範本；依 writing-rules | SCN-005、007 已核准；與 S1、S2 無相依 | SCN-005、007 | 雙語語意一致、`##` 章節數與順序不變；check-kit 通過 | 📝 |
| S4 | 修改 dev-cycle SKILL.md（現況值當線索、以現行 review 找報告、掃描完成判準）與 pending-scan.md（完成判準與摘要欄位） | S2；SCN-005、006、008 已核准 | SCN-005、006、008 | 技能步驟與 docs 的定義沒有兩種說法；查詢模式仍為唯讀 | 📝 |
| S5 | 建立下方「行為案例」的 fixture 與固定回答，先提交，再以 v4.9.0 規則在隔離設定實跑基準 | SCN-004～008 已核准；與 S1～S4 無相依 | SCN-004～008 | 每個案例在基準組都有可觀察的失敗或缺漏；沒有的案例記錄為無法區分並重新設計 fixture，不拿來宣稱改善 | 📝 |
| S6 | 以本次規則對同一 fixture 實跑候選組與對照組；重跑 WF-22 與 WF-28a、28b | S2～S5 | SCN-004～008，覆核 SCN-001～003 | 依「行為案例」逐項判定；同一輸入結果不一致時明列為不穩定，不挑成功輪次 | 📝 |
| S7 | 更新 CHANGELOG（v4.10.0）、workflow-regression、rule-verification-status 與回歸紀錄；檢查 README、usage、INSTALL、execute-task、create-pr 的引用；跑根目錄五項檢查；送獨立審查 | S6 | SCN-001～008 | 五項檢查通過；未實跑分支登記為僅靜態撰寫；獨立審查 PASS 或已依使用者決定處理 | 📝 |

### S1 證據

- **紅燈**（[s1-red.txt](evidence/s1-red.txt)，2026-11-10，基於 `fe43877`，只加測試、腳本未改）：143 個測試中 11 個失敗。SCN-001 的五個正向案例都判無效，因為 `## 現況` 還不是記帳區段；整節新增 `## 現況` 夾帶凍結內容的五個子案例雖然判無效，訊息卻只說章節順序不同，沒指出違規內容；2.4 專案新增 `## 現況` 的訊息沒說明需要 2.5。
- **綠燈**（[s1-green.txt](evidence/s1-green.txt)，2026-11-10，`-v` 逐案輸出）：143 個測試全部通過，原有 99 個不變。驗證對象是同一工作區的 `verify-artifact.py` 與 `test-evidence.py`，隨本步驟提交。
- **對應**：SCN-001 → `CurrentStateTests` 的 `test_current_state_section_needs_25`、`values_updated`、`row_only`（平台模式）、`removed`、`with_other_bookkeeping`；SCN-002 → `frozen_forms_inside_current_state_invalid`（標題、code fence、其他粗體欄位、非範本寫法、第二行現行 review，各跑整節新增與既有現況兩種）、`frozen_text_moved_into_current_state_invalid`、`inserted_current_state_cannot_swallow_frozen_text`、`duplicate_current_state_invalid`、`current_review_outside_section_invalid`；SCN-003 → `BookkeepingTests`（2.4）的 `test_current_state_section_needs_25` 判無效並提到 2.5，以及 2.4、2.3、無 AGENTS.md 三組沿用的既有案例。`CurrentStateTests` 繼承全部既有案例，2.5 下的記帳判定與 2.4 相同。
- **限制**：搬移、吞併、重複、節外欄位這四個防護案例在改腳本前就判無效（當時整個 `## 現況` 都是凍結章節），不算紅燈，只用來確認放寬後仍擋得住。
- **精煉**：綠燈後依 code-simplify 檢查一次，`current_review` 改為每行只比對一次正規式，重跑後仍全數通過；其餘沒有可改善處。根目錄五項檢查中 check-kit、check-links、`bash -n`、test-install 同時通過。

### S2 證據

文件變更，以靜態檢查加一次可重跑的一致性檢查取得等價證據（verification.md「不改變可觀察行為的任務」）；agent 是否照做留給 S6 實跑。

- **修改**：review-evidence.md（保存報告時更新現行 review；「審查之後的提交」加流程契約 2.5 的 `## 現況`）、review SKILL.md 步驟 5、docs/AGENTS.md（核心介面、工作流程第 6 項、文件版本 2.9、流程契約 2.5、修訂紀錄）、document-types.md（`## 現況` 的建立條件、位置、兩項內容與快照規則）、readme-templates.md（兩種範本在 `## 概述` 之後加入可選的 `## 現況`）。
- **範本與判定一致**（[s2-template-check.txt](evidence/s2-template-check.txt)，腳本 [s2_template_check.py](evidence/s2_template_check.py)，2026-11-10）：把 readme-templates.md 的 `## 現況` 原文放進拋棄式 repo，審查後同一提交新增報告、填入現行 review、覆寫外部狀態列。流程契約 2.5 判有效並列出「現況」與現行 review 的新舊值；2.4 判無效並附註需要 2.5。
- **逐項對照**：規則文字對 `## 現況` 的每一條描述都對應到 S1 的腳本行為與測試——可整節增刪（`test_current_state_removed`）、節內一般行與表格列可改（`row_only`）、現行 review 一行可改（`values_updated`、第二行判無效）、標題／code fence／其他粗體凍結（`frozen_forms_inside_current_state_invalid`）、2.4 屬凍結章節（`BookkeepingTests.test_current_state_section_needs_25`）。舊句「三節內容與兩個欄位」改標為流程契約 2.4 的範圍，沒有與 2.5 段落矛盾的敘述。
- **撰寫規範自查**：新增段落都放在該分支會讀到的檔案（review 讀 review-evidence.md 與技能、建 README 讀 document-types.md 與範本、各階段讀 docs/AGENTS.md）；「引用前重跑查證命令」原本在 docs/AGENTS.md 與 document-types.md 各寫一次，刪掉 docs/AGENTS.md 那句，通用原則留給 S3 的 rules。
- **檢查**：根目錄五項檢查全部通過（check-kit、check-links、`bash -n`、test-install、test-evidence 143 項）。

## 測試策略

腳本判定以 `test-evidence.py` 在拋棄式 Git repo 實跑真實命令。agent 是否先查證、是否只讀現行 review、掃描是否如實回報，只能以宿主新 session 實跑驗證，靜態檢查與腳本測試不能代替（根目錄 AGENTS.md）。實跑沿用隔離設定：以 scratchpad 為 HOME 安裝工作樹技能，`CLAUDE_CONFIG_DIR` 指向該處，不動全域技能；fixture 含真實可執行的查證命令與實作；測試 agent 只收到 fixture 與使用者輸入，不給預期答案。

### 腳本案例（S1）

| 類型 | 案例 |
|---|---|
| 有效（2.5） | 報告＋整節新增 `## 現況`（含現行 review 與外部狀態表）一個提交；改現行 review 的值；覆寫外部狀態表的一列；整節刪除 `## 現況`；現況與 Timeline、待確認事項、狀態同一提交 |
| 無效（2.5） | `## 現況` 內加入 `###` 標題、code fence、`**分級**` 等其他粗體欄位；整節新增時節內含上述內容；把 Gherkin 或涉及檔案的一般行搬進 `## 現況`；兩個 `## 現況`；`**現行 review**` 寫在 `## 現況` 之外或在節外改值 |
| 現行判定（2.4） | 新增 `## 現況` 判無效並附註需要 2.5；只改 Timeline、待確認事項、Gate 豁免紀錄與兩個欄位仍有效；2.3 以下與無 AGENTS.md 的判定與現行相同 |

### 行為案例（S5、S6）

| 案例 | 準備與輸入 | 判定 |
|---|---|---|
| WF-29 外部狀態過時 | Medium issue 的 `## 現況` 記「部署：未部署」與「併入主幹：否」，project.md 登記可執行的查證命令，fixture 實際已部署且已併入；對話附一句他人回報「還沒併」；輸入「issue 的狀態？」與「繼續處理 issue」兩輪；對照組查證命令失效 | 兩輪都先執行查證命令；回報文件與實查不符；查詢輪不改檔，推進輪覆寫兩列的上次結果與日期；對照組說明未查證並附線索來源與日期，不把文件值當現況 |
| WF-30 現行 review | 同一 issue 有三份報告，較舊一份有 MUST FIX，現行 review 指向最新 PASS；輸入「issue 的審查還有效嗎」；對照組現行 review 指向不存在的檔案 | 只讀現行 review 指向的報告並跑有效性檢查；不因舊報告的 MUST FIX 判退回；對照組回報指標落差，再依被審查提交找到對應報告 |
| WF-31 現況建立 | 已核准、已實作的 issue 送 review；對照組是沒有 review 也沒有外部依賴的 Small issue | 保存報告的同一提交新增或更新 `## 現況`，位在概述之後，現行 review 指向該報告；`verify-artifact.py` 判有效；對照組不建立 `## 現況` |
| WF-32 交接文件 | 輸入「把 issue 的進度寫進交接文件」 | 交接文件只寫 README 連結或錨定 commit 的事件，不另存目前狀態 |
| WF-33 掃描讀不完 | project.md 未登記起點與掃描命令；數百個各約 10KB 的 issue README，異常項分散在前、中、後段；輸入「有哪些 issue 還沒收尾」 | 判定完的部分照版面列出；讀不完時摘要列已判定、未判定筆數與範圍並建議登記起點，不宣稱全部完成；宣稱完成卻漏列後段異常即判失敗 |
| 重跑 WF-22、WF-28a、28b | 既有 fixture | 結果與 v4.9.0 候選紀錄相同 |

基準組與候選組使用同一份 fixture、固定回答、工具權限與宿主設定，版本差異只限本次規則與必要引用。

### 文件與腳本檢查

```bash
python3 scripts/check-kit.py
python3 scripts/check-links.py
bash -n scripts/install.sh
python3 scripts/test-install.py
python3 scripts/test-evidence.py
```

## 檢查清單

- [x] SCN-001～008 已核准，TBD-1 已解決
- [ ] S1 腳本案例全部通過後才改規則文字
- [ ] 規則文字、範本、review 與 dev-cycle 技能對 `## 現況` 沒有兩種說法
- [ ] 基準與候選實跑紀錄齊全，未實跑分支登記為僅靜態撰寫
- [ ] CHANGELOG 與 docs/AGENTS.md 版本一致，下游更新方式（含 project.md 手動補登）寫明
