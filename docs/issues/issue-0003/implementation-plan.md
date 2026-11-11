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
| S3 | 修改 rules/AGENTS.md 與 rules/AGENTS.zh-TW.md、project.md 範本；依 writing-rules | SCN-005、007 已核准；與 S1、S2 無相依 | SCN-005、007 | 雙語語意一致、`##` 章節數與順序不變；check-kit 通過 | ✅ 2026-11-10；見「S3 證據」 |
| S4 | 修改 dev-cycle SKILL.md（現況值當線索、以現行 review 找報告、掃描完成判準）與 pending-scan.md（完成判準與摘要欄位） | S2；SCN-005、006、008 已核准 | SCN-005、006、008 | 技能步驟與 docs 的定義沒有兩種說法；查詢模式仍為唯讀 | ✅ 2026-11-10；見「S4 證據」 |
| S5 | 建立下方「行為案例」的 fixture 與固定回答，先提交，再以 v4.9.0 規則在隔離設定實跑基準 | SCN-004～008 已核准；與 S1～S4 無相依 | SCN-004～008 | 每個案例在基準組都有可觀察的失敗或缺漏；沒有的案例記錄為無法區分並重新設計 fixture，不拿來宣稱改善 | ✅ 2026-11-10；fixture 與判定 `b26c73a`、基準組與追加案例 `f10c3c1`，見下方「S5 證據」 |
| S6 | 以本次規則對同一 fixture 實跑候選組與對照組；重跑 WF-28a、28b 與懸置掃描（issue-0001 的 scan fixture） | S2～S5 | SCN-004～008，覆核 SCN-001～003 | 依「行為案例」逐項判定；同一輸入結果不一致時明列為不穩定，不挑成功輪次 | ✅ 2026-11-10；每案一輪，依當時寫定的判準全部通過（WF-32 於 2026-11-11 依 SCN-007 原文重判為未符合，見 S8），能區分的只有 wf30、wf30c 的有效性與 wf31；見下方「S6 證據」 |
| S7 | 更新 CHANGELOG（v4.10.0）、workflow-regression、rule-verification-status 與回歸紀錄；檢查 README、usage、INSTALL、execute-task、create-pr 的引用；跑根目錄五項檢查；送獨立審查 | S6 | SCN-001～008 | 五項檢查通過；未實跑分支登記為僅靜態撰寫；獨立審查 PASS 或已依使用者決定處理 | ⏳ 2026-11-10 文件更新完成：CHANGELOG v4.10.0、WF-29～WF-33、v4.10.0 驗證狀態、[2026-11-10 回歸紀錄](../../workflow-results/2026-11-10.md)、usage.md 與 INSTALL.md 各一處；README.md、execute-task、create-pr 沒有相關敘述、未改。五項檢查通過（check-kit、check-links、`bash -n`、test-install 14 項、test-evidence 143 項）。待獨立審查 |
| S8 | 依 [review-5c2ca52](review-5c2ca52.md) 與 TBD-2～TBD-4 修正：`verify-artifact.py` 凍結跨行 HTML 區塊、HTML 標籤、巢狀容器與編號／引用的粗體欄位，2.4 附註只在現況變動時出現；docs/AGENTS.md 第 6 項、document-types.md、review-evidence.md、英文 rules、dev-cycle 依審查修正；證據遮蔽；重跑 wf29、wf29d、wf30c、wf31、wf32、WF-28b 並依 SCN-007 原文重判 wf32；更新發布文件後重新送審 | TBD-2～TBD-4 已解決 | SCN-001～002、004～007 | 新負向案例先紅後綠，既有測試仍通過；重跑依 expected.md「審查後重跑」判定；獨立覆審 PASS 或已依使用者決定處理 | ✅ 2026-11-11；覆審 review-acd488f 退回，由 S9 接續 |
| S9 | 依 [review-acd488f](review-acd488f.md) 與 TBD-5 修正：記帳章節的 HTML 改用允許清單並追蹤多行註解，code span、反斜線跳脫與表格逐列不算 HTML；凍結清單與引用裡的 setext 標題與連結參照定義；`**現行 review**` 改寫檔名；發布文件與紀錄跟上 S8；`run_case.py` 保存回合內提交；重跑 wf29、wf30c、wf31、wf32、WF-28b 後重新送審 | TBD-5 已決定 | SCN-001～002、004、006、007 | 新負向案例先紅後綠；reviewer 的對抗案例全部判 INVALID、合理寫法判 OK；重跑依 expected.md「第二輪審查後重跑」判定；獨立覆審 PASS 或已依使用者決定處理 | ✅ 2026-11-11；覆審 review-4d0df5c 退回，由 S10 接續 |
| S10 | 依 [review-4d0df5c](review-4d0df5c.md) 與 2026-11-11 使用者決定（記帳章節的行含 `<` 一律凍結）修正：移除 code span、跳脫與表格的模擬，`<` 只放行不在行首的換行標籤；以 `[` 開頭的行與緊接在文字後的分隔線凍結；docs/AGENTS.md 寫明記帳內容不含 `<`；發布文件的落差；重跑 wf31、WF-28b 後重新送審 | 使用者決定 | SCN-001～002、004 | 新負向案例先紅後綠；三輪審查的對抗案例全部 INVALID；重跑依 expected.md「第三輪審查後重跑」判定；獨立覆審 PASS 或已依使用者決定處理 | ✅ 2026-11-11；覆審 review-4e0177a 退回，由 S11 接續 |
| S11 | 依 [review-4e0177a](review-4e0177a.md) 修正：分行只認換行字元、行尾只去空格與 tab；凍結章節的空行列入比對；以 `[` 開頭的行放行任務清單、alert 與行內連結；移除未用常數；撰寫規範與發布文件補上 `[`、粗體與分隔線；重跑 WF-28b、wf31 後重新送審 | TBD-6 | SCN-001～002、004 | 新負向案例先紅後綠；四輪審查的對抗案例中攻擊寫法全部 INVALID；重跑依 expected.md「第四輪審查後重跑」判定；獨立覆審 PASS 或已依使用者決定處理 | ✅ 2026-11-11；覆審 review-ac2183c 退回，由 S12 接續 |
| S12 | 依 [review-ac2183c](review-ac2183c.md) 修正：記帳章節含凍結內容的段落整段凍結並比對段落結尾，表格逐列判定；凍結章節連續空行視為一個；補參照定義的存活變異案例；撰寫規範與發布文件補上「與含凍結寫法的段落空一行」；重跑 WF-28b、wf31 後重新送審 | TBD-6 | SCN-001～002、004 | 新案例先紅後綠；五輪審查的對抗案例中攻擊寫法全部 INVALID、前四輪判定不變；本 repo 歷來的記帳提交除已知的 18f0e64 外判 OK；重跑依 expected.md「第五輪審查後重跑」判定；獨立覆審 PASS 或已依使用者決定處理 | ✅ 2026-11-11；覆審 review-20d0847 退回，由 S13 接續 |
| S13 | 依 [review-20d0847](review-20d0847.md) 修正：表格欄數照 GFM 計算，表頭含 `\|` 不當表格；表格含凍結列時表頭與分隔列一併凍結；補 M11、M13 變異的案例；文件補上表格條件與下游筆數的分類方式；v4.9.0 起就有的 V3、V4 另開 #5 | TBD-6 | SCN-001～002、004 | 新案例先紅後綠；六輪審查的對抗案例中，除登記為 #5 的 V3、V4 外，攻擊寫法全部 INVALID，前五輪判定不變；本 repo 歷來的記帳提交判定不變；獨立覆審 PASS 或已依使用者決定處理 | ⏳ |

### S1 證據

- **紅燈**（[s1-red.txt](evidence/s1-red.txt)，2026-11-10，基於 `fe43877`，只加測試、腳本未改）：142 個測試中 11 個失敗（紅燈之後又補了一個防護案例，最終測試檔配改前腳本為 143 個、11 個失敗，review-5c2ca52 重現；2026-11-11 更正，原寫 143 個）。SCN-001 的五個正向案例都判無效，因為 `## 現況` 還不是記帳區段；整節新增 `## 現況` 夾帶凍結內容的五個子案例雖然判無效，訊息卻只說章節順序不同，沒指出違規內容；2.4 專案新增 `## 現況` 的訊息沒說明需要 2.5。
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

### S3 證據

文件變更，以靜態檢查與人工覆核取得等價證據；agent 是否先查證留給 S6 的 WF-29 實跑。

- **修改**：rules/AGENTS.zh-TW.md 與 rules/AGENTS.md 第六節末尾各加一段「外部狀態以實查為準」；docs/agents/project.md 範本「提交與交付」的合併判定方式後加上推送、部署、平台 issue／PR 狀態的查證命令。
- **雙語覆核**（人工，2026-11-10）：兩段逐句對應——適用範圍（合併、推送、部署、平台 issue／PR，會被其他人或流程改變）、來源（文件、記憶、他人回報）、動作（對外陳述或據以行動前重新查證）、結果不同時以實查為準並指出差異、查不到時說明並附來源與日期。兩檔 `##` 章節都是 11 個，順序不變。
- **撰寫規範自查**：正面表述，沒有禁令句；放在每個 agent 都會載入的 rules，涵蓋 issue 流程以外的狀態回報（下游實例是 peer 回報的推送狀態）；與 document-types.md 的表格快照規則分工：rules 是通用原則，document-types 是 `## 現況` 這張表的寫法。
- **檢查**：根目錄五項檢查全部通過（check-kit 含雙語章節數、check-links、`bash -n`、test-install、test-evidence）。

### S4 證據

文件變更，以靜態檢查與人工覆核取得等價證據；行為留給 S6 的 WF-29、WF-30、WF-33 實跑。

- **修改**：dev-cycle SKILL.md「輸入與模式」加 `## 現況` 的讀法（只讀現行 review 指向的報告、指標失效時的退路、外部狀態重跑查證、查詢回報差異、推進覆寫該列），「懸置掃描」的完成判準改為全部判定或如實列出未判定部分；pending-scan.md 回報版面第 1 點加部分範圍時的摘要欄位，結尾的完成判準同步，並寫明部分範圍的結論只涵蓋已判定的 issue。
- **覆核**（人工，2026-11-10）：現行 review 的位置與更新時機與 review-evidence.md、document-types.md 同一說法；外部狀態的「快照、重跑、以實查為準、覆寫該列」與 document-types.md 及 rules 第六節一致；「偵測是唯讀操作」不變，覆寫只發生在推進。dev-cycle 宣告的最低流程契約 2.2 不變：沒有 `## 現況` 時新增的句子不適用。
- **檢查**：根目錄五項檢查全部通過。

### S5 證據

- **環境**：kit v4.9.0（`git archive v4.9.0`）的技能以 `install.sh claude` 裝進 scratchpad 的隔離 HOME，`CLAUDE_CONFIG_DIR` 指向該處，`.credentials.json` 以 symlink 連回；fixture 以同一份 [build_fixtures.py](fixtures/build_fixtures.py) 用 v4.9.0 部署 docs（流程契約 2.4）。執行器是 issue-0001 的 `run_case.py`（`claude -p`，claude-opus-5-5，Claude Code 2.1.322，允許工具同該腳本）。fixture 與判定先提交（`b26c73a`）再實跑。
- **基準組結果**（[s5-baseline/](evidence/s5-baseline/)，2026-11-10，依 [expected.md](fixtures/expected.md)）：

| 案例 | 基準組行為 | 能否區分 |
|---|---|---|
| wf29 | 兩回合都重跑 `git merge-base` 與 `tools/deployed.py`，指出 README 與同事回報都不符；回合 2 覆寫兩列 | 無法區分。表格的「查證命令」欄與 project.md 的登記把查證方法直接交給 agent |
| wf29c | 合併以 git 查證；部署寫「無法確認」，附 2026-11-05 的最後紀錄 | 無法區分 |
| wf30 | 只讀現行 review 指向的報告；`verify-artifact.py`（2.4）判 `## 現況` 的指標變更為凍結內容，結論「需重新審查」 | 有效性能區分（SCN-001）；只讀現行報告無法區分 |
| wf30c | 發現 `review-0000000.md` 不存在，改用被審查提交對應的報告；同樣判需重新審查 | 有效性能區分；指標落差的回報無法區分 |
| wf31 | 報告提交只新增報告，沒有 `## 現況` | 能區分 |
| wf31c | 實作提交後沒有 `## 現況` | 對照組，符合預期 |
| wf32 | 交接文件附 README 連結，另存一張帶查證日期與命令的狀態表 | 依寫定的判準無法區分（判準只在沒有指向 README 或查證時判失敗）；狀態副本仍在，留待候選組比較。2026-11-11 依 SCN-007 原文重判（TBD-2）：未符合，兩組相同 |
| wf33 | 以 grep 判定全部 300 個，四項異常都列出，宣稱逐一判定 | 無法區分。結構化的偵測規則都能用 grep 一次判定，讀不完的情境沒有出現 |

- **重新設計**：wf29 追加舊格式的 wf29b（沒有 `## 現況`、過時資訊只在 Timeline 敘述、project.md 不登記查證命令），測 rules 原則本身；wf30 追加無指標的 wf30b，只跑基準組，比較指標是否減少讀取。兩案的判準在實跑前寫入 expected.md。wf32、wf33 不重新設計：要能區分就得事後改判準或限制工具，記為無法區分，SCN-007、SCN-008 的效果不以本組宣稱。
- **wf29b、wf30b 基準組**（同目錄，2026-11-10）：wf29b 沒有 `## 現況` 也沒有登記查證命令，v4.9.0 的 agent 仍以 `git merge-base` 與 `tools/deployed.py` 查證，指出 Timeline 過時，無法區分；wf30b 沒有指標，基準組也只讀最新一份報告（1 份），指標沒有可觀察的減量。

### S6 證據

- **環境**：同 S5，候選組的技能由本分支工作樹以 `install.sh claude` 安裝（流程契約 2.5）；fixture 由 `f10c3c1` 的 build_fixtures.py 重建。每案一輪。
- **候選組結果**（[s6-candidate/](evidence/s6-candidate/)，2026-11-10，依 [expected.md](fixtures/expected.md)）：

| 案例 | 候選組行為 | 判定 | 與基準組比較 |
|---|---|---|---|
| wf29 回合 1 | 執行 `git merge-base --is-ancestor` 與 `tools/deployed.py`，回答已併入（`ffde1c1`）、已部署，並列出 README 現況（2026-11-05）與實查的對照；工作樹雜湊不變 | 通過 | 無法區分 |
| wf29 回合 2 | 沿用回合 1 的查證，覆寫兩列為「是（merge commit ffde1c1）」「已部署（…2026-11-08 部署）」、查證日期 2026-11-10，列數不變；另改狀態為已完成並補 merge 的 Timeline；在 main 上未提交、先問使用者 | 通過 | 無法區分 |
| wf29c | 合併以 git 查證為已併入；部署寫「查證失敗」，附 2026-11-05 的最後紀錄，明說無法確認也無法推翻 | 通過 | 無法區分 |
| wf29b | 合併、部署都以命令查證，指出 Timeline 過時與 README 沒有 `## 現況`；工作樹雜湊改變只因跑 `python3 -m unittest` 產生 gitignore 的 `__pycache__/`，追蹤檔與文件未變 | 通過 | 無法區分 |
| wf30 | 只讀 `review-5be35f1.md`（現行 review 指向的那份），`verify-artifact.py` 回報 OK 並列出「現行 review（review-bf9b717.md → review-5be35f1.md）」，回答有效 | 通過 | 有效性能區分：基準組（2.4）判 INVALID、需重審。基準組的 README 帶有 2.4 未定義的 `## 現況`，這個差異只說明現況必須列入記帳區段，否則每次更新指標都要重審。只讀現行報告無法區分 |
| wf30c | 指出 `**現行 review**` 指向不存在的 `review-0000000.md`，讀最新報告後檢查器回報 OK，回答 PASS 有效並建議改正指標 | 通過 | 有效性能區分；落差回報無法區分。隔離漏洞：agent 以 Glob 在 kit 工作樹找到 `verify-artifact.py` 並執行，沒有用隔離設定那份；兩份內容相同，判定不受影響 |
| wf31 | 保存報告的提交（`d76a2f2`）同時在 `## 概述` 之後建立 `## 現況`，`**現行 review**` 寫報告的 repo 相對路徑；事後檢查器 OK | 通過 | 能區分：基準組報告提交只新增報告 |
| wf31c | 實作提交後 README 沒有 `## 現況` | 通過 | 兩組相同（對照組） |
| wf32 | 交接文件寫明「現況以 issue README 為準」，事件錨定 `65590cc`、`18eced3`、`e08307c`，另有附查證命令與日期（2026-11-10）的外部狀態表；未提交，理由是提交到 issue 分支會讓 PASS 失效，請使用者選提交位置 | 依寫定判準通過；2026-11-11 依 SCN-007 原文重判（TBD-2）：未符合，兩組相同 | 無法區分：基準組同樣有 README 連結與帶日期的查證表。寫定判準比 SCN-007 寬，SCN-007 原文只容許連結與錨定 commit 的事件；照原文，兩組的查證表都還是狀態副本 |
| wf33 | 以 grep 判定全部 300 個，四項異常都列出，宣稱全部判定 | 通過 | 無法區分；部分範圍的情境沒有出現 |

- **重跑**（[s6-rerun/](evidence/s6-rerun/)，fixture 由 issue-0002、issue-0001 的 build_fixtures.py 以本分支 kit 建立，流程契約 2.5）：
  - WF-28a：2 個提交（規格 `de27567`、實作 `4023ec4`），實作提交把核准 commit 由 `待提交` 回填為 `de27567`，單獨回填提交 0。與 issue-0002 候選紀錄相同，通過。
  - WF-28b：1 個提交（`7a458d7`）保存報告、待確認事項 TBD-1、Timeline，並新增 `## 現況` 指向該報告；`verify-artifact.py` 回報 OK（變更含「現況、現行 review（（無） → …review-412d843.md）」），沒有重審，回報 PASS 沿用、等待合併。與既有判定相同，通過；新增的現況也在同一提交、判定有效。
  - 懸置掃描（issue-0001 scan，19 個 issue）：層級依 issue-0001 expected.md 與三次補充逐項相符（必須處理 2201、2207、2211、2213、2216；無法判定 2204、2218；建議整理 2202、2203、2209、2212、2214、2215、2217、2219、2299；2205、2206、2208、2210 不列，2206 與 2207 的專案規則在摘要註明）；全部判定完成，沒有出現部分範圍的摘要；工作樹雜湊不變。通過。
- **未出現的分支**：部分範圍的掃描摘要（SCN-008），以及 SCN-007 的平台留言與跨 session 記憶寫入，本輪都沒有觸發，登記為僅靜態撰寫。
- **共同觀察**：兩組在 wf32 都因交接文件位於 issue 目錄外、提交會讓 PASS 失效而停下詢問；兩組在 wf33 都自稱「逐一讀過」，實際以 grep 判定。

### S8 證據

2026-11-11，依 [review-5c2ca52](review-5c2ca52.md) 與 TBD-2～TBD-4 修正（`3e448fc`），重跑判準先寫進 [expected.md](fixtures/expected.md)「審查後重跑」並提交（`9456504`），再實跑。

| 項目 | 結果 | 證據 |
|---|---|---|
| 紅燈 | 先加測試、腳本未改：159 個測試 41 個失敗，全部是新增案例（跨行 `<!--`、`<details>`、`<pre>`、行內 `<h2>`、`<strong>`、`<b>`、多層引用與清單裡的 fence、編號與引用的粗體欄位、2.4 附註只在現況變動時出現） | [s8-red.txt](evidence/s8-red.txt) |
| 綠燈 | 改 `verify-artifact.py` 後 159 個全過；同一行就關閉的註解與 `<br>` 仍判有效 | [s8-green.txt](evidence/s8-green.txt) |
| 既有記帳提交 | 本 repo 的 `d0e3287`（review-5c2ca52 與現況）以新檢查器判 OK | 本節命令輸出 |
| 連結檢查 | wf32 證據的工具動作摘要在行內 code 裡含被截斷的 Markdown 連結，`check-links.py` 誤判為壞連結；改為略過行內 code。全 repo 243 個連結只少這一個誤報 | 本節命令輸出 |
| 精煉 | `html()` 一個輔助函式供所有記帳章節共用；凍結原因只在訊息尾端加一句，未另開判定路徑 | — |

重跑（[s8-rerun/](evidence/s8-rerun/)，候選組用 `9456504` 的工作樹技能與 docs；修正前對照用 `git archive d0e3287`，每案一輪，Claude Code 2.1.322、claude-opus-5-5）：

| 案例 | 結果 | 判定 |
|---|---|---|
| wf32 | 交接文件只有 README 連結與三個錨定 commit 的事件（規格核准、實作、審查 PASS），寫明狀態與查證結果見 README；合併查證的日期寫回 README `## 現況`，與交接文件同一提交（`ee1c549`）提交到 issue 分支。檢查器因此判 INVALID（`docs/handover.md` 不屬記帳區段），PASS 失效 | 依 SCN-007 原文通過；提交使 PASS 失效另記，不影響判定 |
| wf29 回合 1 | 重跑 `git merge-base` 與 `tools/deployed.py`，回答已併入、已部署，指出 README 與同事回報都過時；工作樹不變 | 通過 |
| wf29 回合 2 | 覆寫兩列為 2026-11-11 的結果，列數不變；改狀態為已完成並補 Timeline，未提交 | 通過 |
| wf29d 修正後 | 跑 `tools/deployed.py`，回答已部署並指出現況表過時，詢問是否改列；沒有提到現行 review 或審查報告；工作樹不變 | 通過 |
| wf29d 修正前（`d0e3287`） | 同上，同樣沒有誤報指標落差 | 通過；NICE 5 的修正沒有可觀察的差異 |
| wf30c | 指出 `**現行 review**` 指向不存在的檔案，依 review-evidence.md 手動比對後回答 PASS 有效、建議改正指標；沒有執行 `verify-artifact.py`：agent 沒有載入技能，Glob 在 fixture 內找不到腳本，列出真實家目錄的技能被沙箱擋下，輸出照實寫「沒有用檢查器跑過」 | 落差回報與結論符合；「執行 verify-artifact.py」未符合。S6 那輪能執行，是因為隔離漏洞讀到 kit 工作樹的腳本 |
| wf31 | 報告提交（`85b3041`）在 `## 概述` 之後建立 `## 現況`，`**現行 review**` 指向該報告；agent 與事後檢查都以新檢查器判 OK | 通過 |
| WF-28b | 1 個提交（`407ee6d`）保存報告、待確認事項、Timeline、狀態，並在 `## 概述` 之後新增 `## 現況`；新檢查器 OK，沒有重審 | 通過 |

- 隔離設定的技能摘要在本輪出現三種值：Claude Code 會在 `CLAUDE_CONFIG_DIR/skills/synced/` 寫入同步資料，摘要涵蓋整個技能目錄，所以同一份安裝的摘要隨執行而變。產品技能內容以 kit HEAD 為準。

### S9 證據

2026-11-11，依 [review-acd488f](review-acd488f.md) 修正。

| 項目 | 結果 | 證據 |
|---|---|---|
| 紅燈 | 先加測試、腳本未改：175 個測試 48 個失敗，全部是新案例（`<details` 換行或行尾空白、`<script`／`<style`／`<textarea`／`<pre` 獨佔一行、行內 `<title>`／`<dialog>`／`<s>`／`<a>`／`<small>`、跳脫的 backtick、表格切欄與跨行 code span、連結參照定義、清單與引用裡的 setext、多行註解的 `-->` 與內容、code span 與跳脫的標籤名） | [s9-red.txt](evidence/s9-red.txt) |
| 綠燈 | 改 `verify-artifact.py` 後 175 個全過 | [s9-green.txt](evidence/s9-green.txt) |
| 紅燈後改的期望 | 三處負向案例的期望訊息由 `<!--` 改為「需重新審查」：未關閉的註解現在整段凍結，吞掉其後的 `##` 標題，檢查器先回報章節順序不同。判定仍是 INVALID。另補兩個案例（表格逐列的 backtick、表格內 `\|` 跳脫的 code span），由下兩列的誤判發現 | 本節 |
| 對抗案例 | review-acd488f 留在暫存區的 46 個案例重跑：攻擊寫法 36 個全部 INVALID；控制組 1 個與合理寫法 8 個判 OK，`1. **日期**` 依 TBD-3 判 INVALID（共 37 個 INVALID、9 個 OK；2026-11-11 依 review-4d0df5c NICE 2 更正計數）。過程中發現兩項誤判並修正：表格內以 `\|` 跳脫的 code span 被當成未配對，以及前一列表格未配對的 backtick 延續到下一列 | 暫存區（未進版控） |
| 下游影響 | 唯讀掃描本機 682 份不重複的 issue README：與 v4.9.0 相比，11 份共 26 行記帳內容改為凍結，全部是引用或編號清單加粗體開頭的行（TBD-3 的決定）；HTML 允許清單沒有新增凍結行。既有行不變時不影響判定，只有審查後新增這些寫法才需重審 | 本節 |
| 精煉 | 判斷 HTML 只剩 `SAFE_HTML`、`ANY_HTML` 兩個式子，移除封閉的標籤清單與 HTML 區塊式子；code span 與註解狀態各一個輔助函式 | — |

重跑（[s9-rerun/](evidence/s9-rerun/)，候選組用 `b2f321f` 的工作樹技能與 docs，判準在同一提交寫定，每案一輪；wf32 判定後依同一判準追加 3 輪，四輪全部列出）：

| 案例 | 結果 | 判定 |
|---|---|---|
| wf31 | 報告提交在 `## 概述` 之後建立 `## 現況`，`**現行 review**` 寫成相對連結 `[review-19fc019.md](review-19fc019.md)`；新檢查器 OK | 通過 |
| WF-28b | 1 個提交保存報告、TBD-1、Timeline，並新增 `## 現況`，`**現行 review**` 寫檔名；新檢查器 OK，沒有重審 | 通過 |
| wf30c | 指出 `**現行 review**` 指向不存在的檔案，說明應改成報告檔名；手動比對後判有效，照實寫「沒有經過檢查器」 | 落差回報與結論符合；未執行檢查器，原因同 S8 |
| wf29 回合 1 | 重跑查證，指出 README 與同事回報過時；工作樹不變 | 通過 |
| wf29 回合 2 | 覆寫兩列為 2026-11-11 的結果，列數不變；改狀態、補 Timeline，並提交到另開的分支 `issue-2901-closeout` | 通過 |
| wf32 第 1 輪 | 交接文件另有「目前進度」表（「併入 main：尚未併入」「部署：尚無部署紀錄」）與外部狀態查證表；沒有寫回 README | 依 SCN-007 原文未符合 |
| wf32 第 2～4 輪 | 交接文件只有 README 連結與錨定 commit 的事件，寫明狀態以 issue 目錄的文件為準 | 依 SCN-007 原文通過 |

- 追加的 3 輪是看到第 1 輪失敗後才決定，沒有事先寫進 expected.md；判準沿用已提交的版本，四輪全部列出（review-4d0df5c NICE 3）。
- **wf32 不穩定**：依現行文字 4 輪中 3 輪通過；S8 的 1 輪（第 6 項的寫回尚未加條件）也通過。第 1 輪失敗與第 6 項改成有條件是否有關，輪數太少無法判斷。
- **4 輪都把交接文件提交到 issue 分支，讓 PASS 失效，輸出都沒有提到失效或需要重審**（[issue #4](https://github.com/raybird/dev-rules-kit/issues/4) 的範圍）。
- 追加輪次第一次執行時，runner 以改名後的案例名稱查不到輸入，送出空白訊息、未建立 session（exit 1）；三份無效證據已刪除，修正 runner 後重跑，上表只列有效輪次。

### S10 證據

2026-11-11，依 [review-4d0df5c](review-4d0df5c.md) 修正。審查找到允許清單本身會開出 HTML 區塊（`<br>` 獨佔一行、行首的同行註解），以及 code span 判定與渲染器不一致；使用者決定不再模擬 CommonMark，記帳章節的行含 `<` 就凍結。

| 項目 | 結果 | 證據 |
|---|---|---|
| 紅燈 | 先加測試、腳本未改：175 個測試 24 個失敗，全部是新案例（`<br>`／`<wbr>`／`</br>` 獨佔一行、行首註解後接 code span、code span 與跳脫的標籤名、`` `|` `` 夾住的標籤、自動連結、跨行的連結參照定義、10 位數編號後接 `===`） | [s10-red.txt](evidence/s10-red.txt) |
| 綠燈 | 改 `verify-artifact.py` 後全過；另補 `**現行 review**` 平台連結三種寫法的案例，共 176 個 | [s10-green.txt](evidence/s10-green.txt) |
| 對抗案例 | 三輪審查留在暫存區的案例（含本輪的 G、J、K、S 系列）重跑：攻擊寫法全部 INVALID；判 OK 的只有控制組、行中間的 `<br/>`、不帶粗體的編號清單 Timeline，以及 reviewer 腳本實際沒有改動 README 的 K6。code span 裡的標籤名、`\<div>`、`<網址>`、`n<k` 依決定判 INVALID | 暫存區（未進版控） |
| 既有記帳提交 | `31c6bae`（review-4d0df5c 與現況）判 OK。`18f0e64` 改判 INVALID：當時寫的 Timeline 列在 code span 裡含 `<details`，正是新規則的代價；該提交是已被後續修正取代的 RETURN 記帳，不影響現行判定。WF-28b fixture 的記帳提交也因待確認事項寫了 `` `done <id>` `` 改判 INVALID，所以 docs/AGENTS.md 加寫記帳內容不含 `<`，並重跑驗證 agent 會照做 | 本節命令輸出 |
| 下游影響 | 唯讀掃描本機 683 份不重複的 issue README：33 份共 44 行記帳內容含 `<`（41 行在 code span 裡）；另有 1 份因 code fence 數為奇數，標題被未關閉的 fence 吞掉，與本次修改無關 | 本節 |
| 精煉 | 移除 `outside_code`、`escaped_count`、`SAFE_HTML`、`ANY_HTML`、`TABLE_DELIMITER` 與逐行的 code span 狀態；HTML 判定剩一個函式 | — |
| 上一輪 NICE 7 | 外部狀態列在 2.4 專案覆寫會讓 PASS 失效：`## 現況` 只在 2.5 定義，review-evidence.md 已寫 2.4 的 `## 現況` 屬凍結章節，不另改 | — |

重跑（[s10-rerun/](evidence/s10-rerun/)，候選組用 `cff0449` 的工作樹技能與 docs，判準在同一提交寫定，每案一輪）：

| 案例 | 結果 | 判定 |
|---|---|---|
| WF-28b | 1 個提交（`48ae482`）保存報告、TBD-1、Timeline，並在 `## 概述` 之後新增 `## 現況`。TBD-1 把審查報告裡的命令寫成「`done` 會同時標記兩筆」，記帳內容沒有 `<`；新檢查器 OK，沒有重審 | 通過 |
| wf31 | 報告提交（`2eaf42b`）在 `## 概述` 之後建立 `## 現況`，`**現行 review**` 寫檔名；新檢查器 OK | 通過 |

每案只有一輪，不能說明 agent 穩定避開 `<`；上一輪同一案例的 agent 寫過含 `<` 的佔位字。

### S11 證據

2026-11-11，依 [review-4e0177a](review-4e0177a.md) 修正。

| 項目 | 結果 | 證據 |
|---|---|---|
| 紅燈 | 先加測試、腳本未改：192 個測試中 12 個子測試失敗，全部是新案例（收尾 fence 後的 NBSP、標題前的 U+2028、以 U+0085／U+2028 注入的假章節、凍結章節刪除空行、alert 與連結開頭的記帳行）。清單裡的 `<br>`、引用裡的參照定義與重開的註解三個防護案例在改前已通過，用來擋住審查列出的存活變異 | [s11-red.txt](evidence/s11-red.txt) |
| 綠燈 | 改 `verify-artifact.py` 後全過；另補 `[x foo` 換行接 `]:` 與 `[!NOTE]:` 兩個負向案例，擋住任務清單與 alert 放行寫得太寬的情況（第一版的放行式子會把 `[x foo` 當成任務清單） | [s11-green.txt](evidence/s11-green.txt) |
| 對抗案例 | 四輪審查留在暫存區的案例重跑：96 個 INVALID。判 OK 的是控制組、行中間的 `<br/>`、不帶粗體的編號清單、reviewer 腳本沒有改動 README 的 K6、已登記的 `\|` 開頭接分隔線（N1 系列）、行首不是粗體的仿粗體欄位（N2、N3，登記為已知限制）、改為放行的 alert 與連結（N4 系列）、不含凍結列的記帳表格（N5），以及不是參照定義的 X1、X7 | 暫存區（未進版控） |
| 下游影響 | 唯讀掃描本機 683 份 issue README：放行 alert 與連結後，以 `[` 開頭而新凍結的記帳行為 0；新凍結的仍是含 `<` 的 44 行（33 份）與引用或編號清單加粗體的 26 行（11 份） | 本節 |
| 精煉 | 移除未用的 `SETEXT`、`NOT_PARAGRAPH`；分行與空白各一個常數 | — |
| 未處理 | 審查 NICE 3 的「表格末列接 `---`」變異沒有補案例：這是已登記的已知限制，補案例只會把限制寫死 | — |

重跑（[s11-rerun/](evidence/s11-rerun/)，候選組用 `df2a444` 的工作樹技能與 docs，判準在同一提交寫定，每案一輪）：

| 案例 | 結果 | 判定 |
|---|---|---|
| WF-28b | 1 個提交（`29a6c9f`）保存報告、待確認事項、Timeline，並在 `## 概述` 之後新增 `## 現況`；新檢查器 OK，沒有重審 | 通過 |
| wf31 | 報告提交（`a0c67b4`）在 `## 概述` 之後建立 `## 現況`；新檢查器 OK | 通過 |

### S12 證據

2026-11-11，依 [review-ac2183c](review-ac2183c.md) 修正；使用者選擇在本 issue 修正 MUST FIX 再送審一輪，下一輪若只找到 v4.9.0 就有的同類缺口則另開 issue。

| 項目 | 結果 | 證據 |
|---|---|---|
| 紅燈 | 先加測試、以 S11 的腳本執行：216 個測試中 16 個子測試失敗，全部是新案例（連結 title、圖片 alt、code span 跨行吞掉檔尾 metadata，落單反引號讓凍結的 code span 脫出，刪掉行首 HTML 後的空行，在含粗體的段落直接接續，表格列與刪掉分隔列，凍結章節多一個空行） | [s12-red.txt](evidence/s12-red.txt) |
| 綠燈 | 改 `verify-artifact.py` 後全過；另補 `[x]:` 與 `[a\](b]:` 兩個參照定義案例，擋住審查列出的存活變異 | [s12-green.txt](evidence/s12-green.txt) |
| 中途發現 | 第一版只做段落凍結、沒有表格例外，本 repo 自己的 Timeline 表格因含一列 `<`，之後所有記帳提交都判 INVALID；補上表格逐列判定後，`d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306` 都判 OK，`18f0e64` 照 TBD-6 判 INVALID | 本節 |
| 對抗案例 | 第五輪 22 個案例：攻擊寫法 A1～A3 系列、Y1、Y2 全部 INVALID；F1（參照定義）、F2、F3（連結文字含方括號或反斜線，已寫入文件）INVALID；A2c、F4～F7 判 OK，渲染相同。前四輪 111 個案例的判定與 S11 完全相同 | 暫存區（未進版控） |
| 下游影響 | 唯讀掃描本機 683 份 issue README：整段凍結新增約 800 行。原先寫的「537 行 metadata、23 份 34 段 269 行」用的分類方式沒有寫明，無法重現，由 S13 以明確定義重算 | 本節 |

重跑（[s12-rerun/](evidence/s12-rerun/)，候選組用 `3fc926a` 的工作樹技能與 docs，判準在同一提交寫定，每案一輪）：

| 案例 | 結果 | 判定 |
|---|---|---|
| WF-28b | 1 個提交（`346789c`）保存報告、待確認事項、Timeline，並在 `## 概述` 之後新增 `## 現況`；新檢查器 OK，沒有重審 | 通過 |
| wf31 | 報告提交（`d747bc2`）在 `## 概述` 之後建立 `## 現況`；新檢查器 OK | 通過 |

### S13 證據

2026-11-11，依 [review-20d0847](review-20d0847.md) 修正。MUST FIX 是 S12 加表格逐列判定時新引入的：`cells()` 用 `strip('|')` 去掉頭尾所有 `|`，和 GFM 只去一個不同，表頭多寫一個 `|` 時檢查器當表格、渲染器當段落。

| 項目 | 結果 | 證據 |
|---|---|---|
| 紅燈 | 先加測試、以 S12 的腳本執行：224 個測試中 10 個子測試失敗，全部是新案例（表頭頭尾多一個 `\|`、表頭與分隔列縮成兩欄）。表頭含 `\|`、分隔列欄數不符、表格緊接在段落後這三個案例改前已通過，用來擋審查列出的存活變異 M11、M13 | [s13-red.txt](evidence/s13-red.txt) |
| 綠燈 | 改 `verify-artifact.py` 後全過；另以變異確認：拿掉欄數比對（M11）有 4 個失敗，允許表格從段落中間開始（M13）有 1 個失敗 | [s13-green.txt](evidence/s13-green.txt) |
| 對抗案例 | 第六輪 17 個案例：T1～T4 系列全部 INVALID；T0、T2c、T6c 是對照組，判 OK；T5（V3）、T6（V4）判 OK，是 v4.9.0 起就有的寫法，登記於 [#5](https://github.com/raybird/dev-rules-kit/issues/5)。前四輪 111 個與第五輪 22 個案例的判定和 S12 相同 | 暫存區（未進版控） |
| 歷來記帳提交 | `d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306`、`20d0847` 之後的保存提交判 OK，`18f0e64` 照 TBD-6 判 INVALID；S11、S12 兩次重跑的 fixture 記帳提交都判 OK | 本節 |
| 下游影響 | 2026-11-11 重新掃描，部分 worktree 已移除，不重複的 README 為 680 份。整段凍結新增的行中，以分隔線開頭的檔尾 metadata 段落 381 行，平常不改；其餘 37 份 50 段 423 行，多為以粗體開頭的條列補述所在的段落。表頭與分隔列一併凍結的表格有 31 份 40 張 | 本節 |

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
| 重跑 WF-28a、28b、懸置掃描 | issue-0002 的 WF-28 fixture；issue-0001 的 scan fixture（WF-22 沒有保存可重建的 fixture，改用涵蓋同一組偵測規則與版面的這份） | 結果與既有候選紀錄的判定相同 |

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
- [x] S1 腳本案例全部通過後才改規則文字（S1 `874992d` 先於 S2 `9fa384e`）
- [ ] 規則文字、範本、review 與 dev-cycle 技能對 `## 現況` 沒有兩種說法
- [x] 基準與候選實跑紀錄齊全，未實跑分支登記為僅靜態撰寫
- [x] CHANGELOG 與 docs/AGENTS.md 版本一致，下游更新方式（含 project.md 手動補登）寫明
