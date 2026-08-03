# Changelog

本檔案記錄 dev-rules-kit 的重要變更，供下游專案更新已複製的檔案時參考。

**版本策略**：重要變更時打 git tag，規則如下——

- **Major**：破壞性變更（規則語意反轉、目錄結構調整、skill 改名或移除），下游更新前應檢視自己的客製內容
- **Minor**：新增 skill / workflow / 規則章節，下游可安全重新複製
- **Patch**：錯字修正、文字調整、文件補充，不影響行為

每個條目標注影響的目錄，方便下游判斷是否需要重新複製對應檔案。

---

## [2.2.0] - 2026-08-03

### 新增（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

- **Gherkin 分批核准**：核准表新增第三種狀態 `待核准`（原本只有 `已核准` 與 `待重新核准`）。Scenario 多時不必一次核准全部，未取得同意者標為 `待核准`，issue 文件即可建立並就已核准部分進入實作。放行門檻是已核准部分必須涵蓋核心目標的主要成功路徑與已辨識的重要失敗路徑；`create-pr` 前必須全部轉為 `已核准`。`decompose` 遇 `待核准` 不阻塞，只拆已核准部分，其餘列入新的「待核准 Scenario」段落且禁止產生 Task
- **`## 待確認事項`**：`new-issue` 原本允許把非阻塞未知「記錄為待確認事項」，但沒有規定寫在哪、也沒有任何節點負責關掉，寫下去就沉了。現在收斂到 README 固定區段（`TBD-N` 編號，狀態 `待確認` / `已解決` / `不影響本次交付`）。刻意設計為**揭露而非阻擋**：不阻止 `create-pr`，但必須在 PR 原文揭露；`review` 覆核 `已解決` 與 `不影響本次交付` 的理由是否成立

### 變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

- **驗收標準形式改由規模單獨決定**：原規則為「Small + Low 用輕量驗收條件，其餘一律完整 Gherkin」，導致 Small + High 的單檔案修正也要寫 Feature / Scenario / 逐項核准表，文件量遠大於 diff。現改為 **Small 一律輕量驗收條件、Medium / Large 一律完整 Gherkin**，風險不再改變形式。這同時修掉了規範的內部矛盾——原規則本身就違反 `docs/AGENTS.md` 明列的「規模與風險不得互相推導」
- **風險改為決定驗收標準的強度**：Small + Medium / High 維持輕量形式，但每項條件必須寫出失敗路徑、至少一項覆蓋最大風險，並記錄核准 commit 以套用輕量版「規格修訂的查核」（行尾標註 `（待重新核准）`，不需逐項核准表）。這補回放寬後原本會缺失的規格漂移防護
- **相容性**：既有 issue 已將 Small 任務寫成完整 Gherkin 者維持有效，依其實際形式查核，不需改寫，`dev-cycle` 也不會因此退回。本次規則只約束新建立的 issue 與規模變更後的重新規劃

### 修正（`rules/` — 下游建議重新複製）

`rules/AGENTS.md` 與 `AGENTS.zh-TW.md` 是唯一會被寫進 `.windsurfrules` 的檔案，在該環境下 agent 讀不到 `docs/AGENTS.md`，因此兩處措辭漂移實際造成規則弱化：

- **characterization test 漏掉綠燈要求**：原文為「先補上 characterization test 再重構」，缺少 `docs/` 版本的「**並取得綠燈**」，等於允許在紅燈狀態下開始重構
- **外迴圈替代方案漏掉記錄要求**：原文沒有「記錄採用的替代方式」，缺少該要求則無 BDD runner 時的替代選擇無從追溯

另統一三處措辭分歧：等價證據適用範圍（`純文件` / `純文件、格式` / `純文件、排版` → 統一為「純文件、排版或無可執行行為」）、豁免邊界（`docs/` 補上「也不得把假綠燈宣稱為測試通過」）、`略過` → `省略`。

### 重構（`skills/`、`workflows/shared/`）

行為不變，移除對 `docs/AGENTS.md` 的整段複製：

- **`decompose`**（254 → 233 行）：刪除「風險優先決策流程」的完整重述（5 步驟清單、風險來源對照表、垂直切片防誤用段與必答三問），改為要求讀取權威節。保留該 skill 獨有的正反對照範例，並將原本埋在重複清單裡的真實差異獨立寫出——拆解階段是**確認**風險理由是否仍成立，不是重新判定
- **`execute-task`**（198 → 195 行）：等價證據段的兩條完整定義改為一句話摘要加引用，與同檔「假綠燈檢查」的引用模式一致

### 效果

跨檔案完全相同的重複片語由 13 組降至 6 組，且剩餘 6 組全部落在 `docs/AGENTS.md` ↔ `rules/` 這一對——即設計上必須各留一份、且現已逐字一致的那組。`decompose` 與 `execute-task` 對權威規範的複製已完全消除。

## [2.1.1] - 2026-07-27

### 變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

行為與 gate 完全不變，只收攏重複敘述。導入兩個具名用語，把散落各檔的列舉收成單一定義，消除措辭漂移。

- **「紅綠重構證據」**：外迴圈紅燈、單元測試紅燈、最小實作後全綠、重構後全綠四段的合稱。原本這串列舉在 `dev-cycle`、`execute-task`、`review` 逐字複述，`docs/AGENTS.md`、`decompose`、`create-pr`、`rules` 還各有變體且措辭不一致（「實作後全綠」／「最小實作後全綠」）。現在定義於 `docs/AGENTS.md` 與 `rules/`，其餘檔案直接使用該詞
- **「假綠燈」**：以任何方式製造出不代表行為正確的綠燈（刪改測試、mock 掉受測行為、硬編碼答案、空 assertion）。取代原本分散在 `execute-task`、`review`、`rules` 的九項列舉；`execute-task` 的「誠實回報與防作弊檢查」步驟改名為「假綠燈檢查」
- **`git diff` 查核回歸單一真相來源**：2.1.0 把完整指令與三條分支邏輯複製到六個檔案，措辭各有出入。現在只留在 `docs/AGENTS.md`「規格修訂的查核」與 `rules/`（規則檔需自足），五個 skill 改為引用該節
- **Superpowers 樣板去重**：各 skill 不再重複解釋「選用增強、缺少套件不構成阻塞、gate 不降低」——該政策已在 `rules/` 定義，skill 端只保留「可用時優先調用 `{skill}`」

### 效果

六個 skill 合計減少 763 字元（約 2.8%）；`docs/AGENTS.md` 與 `rules/` 因納入定義而增加，全部檔案淨變化約 +168 字元。**主要收益是一致性而非 token**：同一概念先前在六個檔案有六種寫法，正是 `sync-skills.py --check` 抓不到的那類漂移。

## [2.1.0] - 2026-07-27

### 變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

2.0.0 的 gate 對「agent 自行降低標準」與「使用者自主決策」一視同仁，導致小任務與純重構付出不成比例的流程成本。本版把 gate 的對象收斂回 agent，並讓證據強度重新服從既有的規模與風險雙軸。**所有既有 issue 的格式仍然有效**，本版只放寬要求、不新增必填欄位。

- **Gate 豁免機制**（`rules/`、`docs/AGENTS.md`、全部閉環 skill）：使用者明確要求跳過某項 gate 時，agent 必須照做，並在 issue README 的 `## Gate 豁免紀錄` 寫下日期、豁免項目、使用者原話與殘餘風險；`dev-cycle` 依該紀錄放行，`review` 與 `create-pr` 如實揭露而非視為缺失。不得自行推定豁免——沉默、時間壓力或任務看起來很小都不算
- **唯一不可豁免的是誠實回報**：豁免可以跳過流程，但不得把未執行的驗證寫成已通過、未審查的變更寫成已審查。使用者要求刪改測試時照做，但必須記錄真實理由
- **驗收標準依規模與風險分級**（`docs/AGENTS.md`、`new-issue`）：**Small + Low** 改用輕量驗收條件（`AC-1` 起，一句話可觀察結果加可重複執行的檢查方式），不需 Gherkin 語法、Scenario ID 與逐項核准表；其餘組合維持完整 Gherkin。仍須取得使用者明確核准，風險升級時補齊 Gherkin
- **純重構免紅燈**（`rules/`、`docs/AGENTS.md`、`execute-task`、`decompose`、`review`）：紅燈要求只適用於會改變可觀察行為的任務。純重構改以「變更前後執行同一組既有測試皆綠」為等價證據，既有測試不足時先補 characterization test。標為不改變行為即承諾 diff 無行為變更，`review` 會據此查核
- **移除 Gherkin SHA-256，改以 git 見證規格修訂**（`docs/AGENTS.md`、`execute-task`、`decompose`、`review`、`create-pr`、`dev-cycle`）：內容雜湊只對「無法重算 hash 的對手」有效，而 agent 依設計就是唯一的計算者——它同時負責改規格、重算 hash 與判定變更性質，形成自我認證的循環；且自然語言規格本來就該在實作中演進，用防竄改機制約束它是類別錯誤。改為：
  - 核准紀錄記錄 `**核准 commit**` 與**逐 Scenario** 的核准日期與狀態（`已核准` / `待重新核准`），取代單一 hash
  - 查核改用 `git diff {核准 commit}..HEAD -- docs/issues/issue-{ID}/README.md`。見證者是 git 而非 agent，輸出是可讀的 diff 而非布林值，判定交給 reviewer 覆核同一份 diff
  - 差異未觸及 Gherkin 即直接繼續；改變條件、動作或預期結果時**只有受影響的 Scenario** 退回重新核准，其餘不受牽連；純措辭調整於 Timeline 補記即可
  - 明文寫入「規格在實作中被修訂是外迴圈的預期結果，不是違規」，與 kit 既有的 Timeline 保留原則一致
- **Review artifact 不綁特定平台**（`docs/AGENTS.md`、`review`、`dev-cycle`）：優先使用專案的 code review 平台（GitHub、GitLab、Gitea 等）；平台不可用、無權限或純本機流程時，改寫入 `docs/issues/issue-{ID}/review-{HEAD 前 7 碼}.md` 並隨變更提交。兩者都必須含 Reviewed HEAD SHA 與獨立 reviewer，兩種方式都無法完成時才輸出 `UNPERSISTED`
- **BDD runner 不再是硬性工具依賴**（`rules/`、`docs/AGENTS.md`、`execute-task`、`decompose`）：專案沒有 BDD runner 時，以標註 Scenario ID 的整合或端對端測試充當外迴圈。缺少特定工具不構成省略外迴圈的理由

### 相容性與遷移

除核准紀錄外，驗收標準、Proof of Test 與 review artifact 的既有格式全部保持有效，本版只增加可選路徑。既有 Small issue 若已寫完整 Gherkin，不需改寫成輕量格式。

**唯一需要轉換的是 2.0.0 建立的 `## Gherkin 核准紀錄`**：`**狀態**`、`**核准日期**`、`**Scenario IDs**`、`**Gherkin SHA-256**` 四個欄位改為 `**核准 commit**` 加逐 Scenario 核准表。轉換為機械式改寫，核准來源與已取得的核准本身不受影響；`**核准 commit**` 填寫承載該次核准內容的 issue 文件提交（未提交時填 `待提交`，首次提交後回填）。

`docs/AGENTS.md` 更新至 v1.7。

## [2.0.0] - 2026-07-26

### 破壞性變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游更新前需檢查）

開發閉環改為 Gherkin BDD 外迴圈與 TDD 內迴圈，並以可持久化證據阻止 Agent 跳過需求核准、失敗測試、獨立審查或 PR 驗收。既有 issue 若缺少下列資料，`dev-cycle` 會退回對應階段補齊，不再依舊格式直接推進：

- README 中具唯一 Scenario ID 的 Gherkin 驗收劇本
- 核准狀態、日期、來源、完整 Scenario ID 集合與 Gherkin SHA-256
- BDD 紅燈、單元測試紅燈、最小實作後全綠及重構後全綠證據
- 對目前 PR HEAD 的獨立 review artifact
- 與核准 Scenario 集合完全一致的 PR Proof of Test

`execute-task`、`review`、`create-pr` 的輸入與完成契約因此比 1.x 嚴格。下游若有依賴舊版任務格式、只記錄「測試通過」、使用待測 checkbox 作為 PR 驗證，或未保存 review 結果，更新前需先調整。

### BDD + TDD 硬性閉環

- **需求規格化**（`new-issue`、`docs/AGENTS.md`）：一次只問一個問題，取得使用者明確核准後，將驗收標準寫成具 Scenario ID 的 Gherkin；以 SHA-256 綁定核准內容，Given / When / Then 異動後必須重新核准
- **雙迴圈拆解**（`decompose`）：每個 Scenario 映射至 BDD feature / Step Definitions、底層單元測試、預期紅燈原因、最小 production code 與重構後回歸命令
- **紅綠重構狀態機**（`execute-task`）：沒有相關 BDD 紅燈與單元測試紅燈前禁止修改 production code；最小實作與重構後都必須取得全綠證據
- **測試防作弊**（`execute-task`、`review`）：禁止為取得綠燈而刪除、略過、弱化或註解測試，也禁止過度 mock、硬編碼答案或空 assertion
- **雙重審查**（`review`）：要求獨立 reviewer、架構符合度、至少三個破壞性邊界案例，以及包含 Reviewed HEAD SHA 的持久化 PR review / comment
- **測試通過證明**（`create-pr`）：PR Proof of Test 必須完整覆蓋核准 Scenario 集合，並附 Gherkin 原文、hash、實際成功命令及結果
- **跨階段防繞過**（`dev-cycle`）：以 Gherkin 核准、紅綠燈證據、目前 HEAD review 與完整 Proof of Test 判斷下一階段

### Superpowers 相容策略

Superpowers 改為選用的流程增強套件，不是執行期必要依賴：

- 已安裝時優先使用 `brainstorming`、`writing-plans`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`
- 未安裝時由本 kit 的 skills 執行內建等價流程，所有核准、測試、獨立審查與完成 gate 維持強制
- README 新增核心 skill 對應、建議輔助 skills 與五個平台的完整套件安裝入口
- PRD 中不存在的 skill 名稱改為可執行能力映射，不形成無法安裝的外部依賴

### 下游更新

- 建議重新複製 `rules/AGENTS.md` 或 `rules/AGENTS.zh-TW.md`
- 重新複製 `skills/` 或其對應的 `workflows/shared/`
- 以新版 `docs/AGENTS.md` 更新 issue 文件規範
- 既有進行中 issue 應先補齊 Gherkin 核准紀錄與雙迴圈證據，再啟用新版 `dev-cycle`
- Superpowers 可選擇不安裝；若安裝，建議使用完整套件而非散裝複製單一 skill

## [1.5.0] - 2026-07-23

### 變更（`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

強化 skill 的輸入證據、完成判準與跨文件狀態回寫，降低 Agent 提前完成、破壞契約或產生無證據內容的風險。

- **契約安全**（`code-simplify`）：公開 API、跨模組、DI、反射／序列化、override 與 callback 簽章優先於簡化規則；無法證明安全時保留原狀
- **文件單一真相來源**（`docs/AGENTS.md`、`new-issue`）：Small／Medium／Large 的初始文件集合、README 連結、Timeline 與 Agent 工作時序保持一致；`new-issue` 改為引用權威規範並使用完整性 gate
- **Task 完成閉環**（`execute-task`）：完成判準、必要驗證、原任務狀態、驗證證據、README Timeline 與 Changelog 全部回寫後才能宣稱完成；移除未命名的獨立實作報告與程式碼副本
- **拆解覆蓋責任**（`decompose`）：每個 Task 新增完成判準、驗證方式、覆蓋項目與責任角色，並檢查需求、交付成果及風險證據都有唯一責任 Task
- **Shell 安全引用**（`git-squash`）：所有動態參數使用 POSIX 單引號，正確處理內含單引號及 `$()`、backtick、環境變數與雙引號
- **PR 證據追溯**（`create-pr`）：Why、How、變更與測試聲明都必須有來源；沒有測試證據時明列未執行項目、原因與殘餘風險

### 相容性

Skill 名稱、目錄結構與 frontmatter description 保持不變。`execute-task` 與 `create-pr` 的輸出契約更嚴格，下游若有依賴舊版實作報告或固定 PR placeholder，更新前應先調整整合方式。

## [1.4.1] - 2026-07-22

### 變更（`rules/` — 下游建議重新複製）

- 將工作流程分級同步改為「規模 + 風險」雙軸：規模決定流程重量，風險決定驗證順序，兩者不得互相推導
- 補上契約驗證、資料盤點、效能實驗、回歸保護網與垂直切片的選擇條件，並明訂垂直切片不是風險優先的預設答案
- `AGENTS.md` 與 `AGENTS.zh-TW.md` 已同步更新，章節數量與順序保持一致

## [1.4.0] - 2026-07-22

### 變更（`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

Issue 評估從單一規模分級改為「規模 + 風險」雙軸，並加強風險優先提示，避免 Agent 將垂直切片當成預設答案。

- **雙軸分工**：`**分級**`（Small / Medium / Large）只決定文件數量、任務清單來源與是否執行 `decompose`；新增 `**風險**`（Low / Medium / High），只決定任務順序、首要驗證與必要證據。Small + High 不增加文件，Large + Low 仍執行拆解
- **風險決策流程**：先辨識最大未知或失敗後果，再比較契約驗證、資料盤點、效能實驗、回歸保護網、垂直切片與一般相依順序；文件必須記錄最大風險、選擇理由及可重複確認的完成證據
- **垂直切片防誤用**：只有端到端整合或使用者行為是最大未知時才採用；外部契約本身未知時優先最小真實請求，資料樣態未知時優先資料盤點與 dry run
- **證據保存**：`execute-task` 執行首要驗證時，必須輸出實際命令結果、測試輸出、樣本觀察或等效資訊，不得只宣稱「已驗證」

### 相容性

既有 `**分級**` 欄位與 `dev-cycle` 分流邏輯保持不變。舊 issue 缺少 `**風險**` 時不自動推測，只有重新規劃或新增步驟時才補評估。

## [1.3.4] - 2026-07-21

### 變更（`skills/`、`workflows/shared/` — 下游建議重新複製）

四個「生成可複製內容」的 skill 統一加上檔案路徑規範，並改善 `git-squash` 的指令複製體驗。

- **相對路徑規範**（`review`、`create-pr`、`create-commit`、`git-squash`）：產出內容中的檔案路徑一律使用相對於 repo root 的路徑（如 `src/auth/login.ts`），不得使用絕對路徑或 `~` 開頭；需指出具體位置時附行號（如 `src/auth/login.ts:42`）。這些內容會貼到 PR、issue 或聊天工具供他人在不同環境閱讀，絕對路徑無法對應，也會洩漏本機目錄結構
- **`git-squash` 指令拆分**：合併方案的三個步驟改為**各自獨立的 code block**（原本是巢狀清單中的行內指令，複製時會沾到說明文字），並明文禁止合併成單一 block；Step 3 改用兩個 `-m`（subject + body），已實測可完整保留 `#` 開頭的 issue 編號

## [1.3.3] - 2026-07-21

### 修正（`skills/`、`workflows/shared/`、`docs/` — 下游建議重新複製）

以模擬 issue 目錄乾跑 `dev-cycle` 的分級判定後，修正兩個會實際卡住流程的漏洞：

- **`dev-cycle` 分級回推規則不完備**：舊規則（只有 README → Small；有 plan 但無 requirement-analysis → Medium；四件套齊全 → Large）在六種常見檔案組合中有三種無法判定（如 `README + requirement-analysis`、`README + plan + requirement-analysis`），會導致舊 issue 卡在分級判定。改為三條互斥且完備的有序 fallback：有分析文件 → Large；否則有 implementation-plan → Medium；否則 Small
- **Small 範本把「已完成」寫死**：`docs/AGENTS.md` 輕量級 README 範本的 `**狀態**` 欄原本固定為「已完成」，但 `new-issue` 是閉環第一步，實作尚未開始；且 `dev-cycle` 需依此欄位追蹤進度。改為 `{狀態}` 佔位並加註不得預先標記完成

### 文件

- `docs/AGENTS.md`：新增 `## 修訂紀錄 (Changelog)`（此前僅要求其他文件撰寫、自身缺漏），metadata 更新至 v1.2
- `docs/usage.md`：註明完整七步示範為 Large 路徑、Small / Medium 跳過 `decompose` 走六步；`dev-cycle` 章節補上分級分流說明
- `skills/README.md`：維護紀錄補記 `dev-cycle` 加入與本輪變更

## [1.3.2] - 2026-07-21

### 變更（`scripts/`、`workflows/README.md` — 下游若未複製 scripts 可略過）

補上守門機制的缺口：`workflows/README.md` 不在同步腳本的複製範圍內，其描述文字過去只能靠人工比對，實際已累積漂移。

- `scripts/sync-skills.py --check` 新增 `check_workflow_readme()`：驗證 `workflows/README.md` 的 Shared Workflows 清單與 `skills/` 一一對應，且每條描述等於對應 `SKILL.md` `description` 的第一句；可偵測描述漂移、漏列、多列孤兒三種情況
- `workflows/README.md`：修正啟用檢查後抓到的 5 條既有漂移（`create-commit` 仍寫著 commit convention 1.0.0、`new-issue` 停留在舊描述等），並加註此清單的維護規則
- `CLAUDE.md`：Conventions 新增 description 撰寫原則（同時寫出做什麼與何時使用）與 `workflows/README.md` 清單的首句約定

CI 既有的 `sync-skills.py --check` 步驟會自動套用新檢查，無需調整 workflow 設定。

## [1.3.1] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

針對 AI agent 的載入機制優化 skill 文件：`description` 是唯一常駐於 context 的部分，也是 agent 判斷「是否要載入整份 skill」的唯一依據，因此補齊觸發時機與適用範圍。

- **description 補齊觸發條件**：
  - `decompose`：明示**僅適用 Large**，agent 不必載入整份 body 即可排除 Small / Medium 的誤觸發
  - `create-pr`：`peer-request`（非通用術語）更正為 **Pull Request**，內文與 `workflows/README.md` 的殘留一併清除
  - `new-issue`：補上產出位置與觸發時機、三級產出說明
  - `create-commit`：補上 Conventional Commits 與「已 git add 後使用」
- **`decompose` 範本去重**：Output 範本中逐字重複的 Phase 2 結構改為結構說明，並加註「不要因為範本只列兩個 Phase 就固定產出兩個」（189 → 167 行）
- **分級規範 single source**：`docs/AGENTS.md`「文件動態分級規範」標示為唯一權威定義，`dev-cycle`、`execute-task` 內的分級表標注為摘要並指向該節

未引入多檔案 progressive disclosure：`sync-skills.py` 為單檔逐位元組複製，SKILL.md 若引用外部檔案會在其他平台的 workflow 端斷鏈。

## [1.3.0] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

為任務切分加入「風險優先」原則，避免 Phase / 步驟被切成技術分層而把整合風險留到最後。深度依分級遞減。

- `decompose`（Large）：新增「Phase 切分原則」——**Phase 1 應優先打通風險最高、假設最未經驗證的那條路徑**，垂直切片為手段而非目的；依未知的類型（外部整合／重構／資料遷移／需求已凍結）給出對應切法，並附正反對照。需求文件標為「未知／待確認」的事項即為排序第一依據
- `docs/AGENTS.md`（Medium / Large）：`implementation-plan.md` 章節新增「實作步驟的排序原則」，未經驗證的假設應排在最前面
- `new-issue`：新增分級自我校驗——規劃 Medium 步驟時若發現未知大到需要獨立探索階段，應升級為 Large 並補齊分析文件
- `docs/usage.md`：示範的 decompose 產出由技術分層改為垂直切片，與新原則一致

Small 級別不受影響。

## [1.2.0] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

依 issue 分級決定是否需要 `decompose`，修正 Small 級別在閉環中缺少任務清單來源、以及 Medium 級別把實作步驟寫兩遍的問題。

- `docs/AGENTS.md`：新增「任務清單來源」對照表；分級**必須**寫入 `README.md` 結尾 metadata 的 `**分級**` 欄位（兩份 README 範本已加上該欄位）；明訂 Small / Medium 不再產生額外的分解文件
- `new-issue`：將評估出的分級寫回 README；要求實作步驟寫成可直接執行的任務清單（每項有明確產出與完成判準）
- `dev-cycle`：新增「分級判定」小節，僅 Large 觸發 `decompose`，Small / Medium 直接進入 `execute-task`；舊 issue 缺少 `**分級**` 欄位時可由現有檔案回推並補寫
- `decompose`：新增「適用範圍」，標明僅適用 Large
- `execute-task`：description 與 Input 改為依分級查表取得任務清單，不再寫死 Implementation Plan Decomposition

### 下游更新注意事項

既有 issue 文件不需回頭補 `**分級**` 欄位，`dev-cycle` 會依實際存在的檔案自動回推；但新建立的 issue 一律會帶此欄位。

## [1.1.0] - 2026-07-06

### 變更（`skills/`、`workflows/shared/` — 下游建議重新複製）

- `execute-task`：新增「確認工作分支」為第一步，明定分支命名規範（`issue-{ID}` 開頭，可加描述後綴）
- `dev-cycle`：完成階段新增 issue 文件收尾動作（README 狀態、timeline 補記）；明示推進模式為全自動執行（直接 commit、直接建 PR），`create-commit` 的人工把關僅適用於單獨呼叫
- README 開發閉環章節註明 `git-squash` 為閉環外的獨立輔助工具

## [1.0.0] - 2026-07-06

首個正式版本，作為下游專案的更新基準點。

### 現有內容盤點

- **`rules/`**：AI 行為核心規則，中（`AGENTS.zh-TW.md`）英（`AGENTS.md`）雙版，各 10 章節
- **`skills/`**：9 個技能——`new-issue`、`decompose`、`execute-task`、`code-simplify`、`create-commit`、`create-pr`、`review`、`git-squash`、`dev-cycle`，構成完整開發閉環
- **`workflows/shared/`**：與 skills 一一對應的 9 個跨平台工作流（由 `scripts/sync-skills.py` 自動同步）；`workflows/antigravity/` 另有平台特定 workaround
- **`docs/`**：下游 issue 文件規範（`AGENTS.md`）、使用指南（`usage.md`）、實體文件模板（`_templates/`）、五平台安裝指南（`setup/`）

### 本版新增（2026-07-06）

- `scripts/sync-skills.py` 新增 `--check` 模式：驗證配對同步、偵測孤兒工作流、檢查雙語規則章節數
- 新增 `scripts/check-links.py` 與 GitHub Actions CI，於 push / PR 時自動執行檢查
- 新增本 CHANGELOG 與版本策略
- 移除誤入版控的 MCP memory 資料庫並補上 `.gitignore`
- 修正 `workflows/README.md` 漏列 `dev-cycle`、`new-issue` 描述不一致等文件矛盾

### 沿革（1.0.0 之前的里程碑）

- **2026-06-29**：README 新增 Claude Code 下游專案掛載規則（`@AGENTS.md` 匯入法）
- **2026-06-20**：新增 `sync-skills.py` 自動同步腳本、實體文件模板；`new-issue` 實作任務動態分級
- **2026-06-02**：新增 `git-squash` skill 與 workflow
- **2026-05-28**：新增 `dev-cycle` orchestration skill 與使用指南 `usage.md`
- **2026-05-18**：新增五平台安裝指南與 `CLAUDE.md` 維護指引
- **2026-05-08**：建立 `skills/` 目錄結構
- **2026-04-16**：初始版本（`rules/` 與 `workflows/`）
