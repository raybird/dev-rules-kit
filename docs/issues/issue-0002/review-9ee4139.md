# 審查報告
- 範圍：完整 PR（issue-0002-bookkeeping-commits 對 main）
- Reviewed BASE SHA：6bd2504d70047aa2982195cd138ee0e6c003289b
- Reviewed HEAD SHA：9ee413960a87c73fc5d5f875132aaef07ef23621
- Reviewed patch-id：b83a3a0b2022349a49fa3a2b0d553d8205ff5596
- 獨立 reviewer：隔離 subagent（未參與實作）
- Review artifact：docs/issues/issue-0002/review-9ee4139.md
- 審查日期：2026-11-03

本次覆審的對象是上次 [review-c77928c](review-c77928c.md) 判定 RETURN 之後的完整 PR。範圍識別已自行重算：`git diff 6bd2504 9ee4139 | git patch-id --stable` 得到 `b83a3a0b…`，與委派值相同，工作樹乾淨。核准 commit 已回填為 `e383a69`。`git diff e383a69 9ee4139 -- docs/issues/issue-0002/README.md` 只有三類變動：關鍵差異表的連結改名、核准 commit 回填、兩列 Timeline。Gherkin 與核准紀錄都沒有改，原核准仍有效。

協調者宣稱的處理方式都逐項查核過，沒有直接採信，查核依據是 fixture repo 的 Git 歷史與原始 stream-json。另外，reviewer 在 `<scratchpad>/review/` 用拋棄式 repo 以 HEAD 的 `verify-artifact.py` 重跑上次的對抗腳本，並新增 `r2/adv2.py`，也用本機下游 126 份 issue README 做語料模擬（`r2/corpus.py`）。路徑依本 issue 證據的慣例遮蔽為 `<scratchpad>`。

## 問題與風險

### MUST FIX

無。

### SHOULD FIX

無。

### NICE TO HAVE

1. **計畫「S2、S4 證據」的結論沒有跟著更正**：`docs/issues/issue-0002/implementation-plan.md:78-84`。
   - 現況：表格仍以「28a＋28c＋28d」合計單獨回填提交，第 84 行寫「SCN-006 通過」，沒有附註。回歸紀錄（`docs/workflow-results/2026-11-03.md:38`、`:77`）已改寫成如實的分列對照：實跑前寫定的 28a＋28c 兩組都是 0，回填的減少只來自追加的 28d 與 28e。
   - 為什麼不列為 SHOULD FIX：表格已標出「1（28d）」；28d 的判定在實跑前寫進 expected.md（`6874d9a`），依當時寫定的判準，這句話不算錯。
   - 建議：第 84 行補一句「分列對照見 S7 證據與回歸紀錄『SCN-006 綜合對照』」，讓計畫與回歸紀錄的說法一致。

2. **計畫 S6「對抗腳本」列的出處與「已揭露」說法不精確**：`implementation-plan.md:94`，對照 `:51`。
   - 出處：這一列說結果記在回歸紀錄「審查後修正與重跑」，但回歸紀錄只有第 91 行提到「reviewer 的對抗腳本」，沒有記錄結果。
   - 「已揭露」：這一列說仍放行的寫法都已揭露，可是第 51 行的已知限制只列了縮排程式碼區塊。「非粗體純文字行」與「只改檔案模式」在計畫、README 與 review-evidence.md 都找不到揭露。
   - 我重跑後的結論與該列相同：上次 17 個放行或對照向量都判定正確，仍放行的是縮排程式碼區塊、footer 的無粗體「風險：Low」、只改 mode，以及回填成 R 本身（依設計允許）。
   - 建議：出處改指本報告；把後兩項補進第 51 行的已知限制。

3. **仍有少數 HTML 或表格形式的寫法會放行**：`skills/review/scripts/verify-artifact.py:19`、`:21`、`:23`。
   - 重現（`r2/adv2.py`）：在 Timeline 寫入下列內容，或對範本 footer 做下列修改，都回報 OK：
     - `<div><h2>驗收條件</h2></div>`：`LOOSE_HEADING` 只錨定行首的 `<h`。
     - `<strong>驗收條件</strong>`。
     - footer 的 `<b>風險</b>: High` 改成 `Low`：`BOLD_LINE` 只認 `**`／`__`。
     - `| 驗收條件 |` 段落後面直接接 `---`：`NOT_PARAGRAPH` 排除了以 `|` 開頭的行，所以不當成 setext。
   - 影響：本機 126 份 README 都沒有這些寫法，觸發機率極低。
   - 建議：登記為已知限制即可。不建議把 `|` 自 `NOT_PARAGRAPH` 移除，因為 Timeline 表格最後一列緊接 footer `---` 時會誤判。

4. **整節新增或刪除時的限制沒有寫明**：`docs/agents/review-evidence.md:44`、`:47`，`docs/AGENTS.md:129`。
   - 規則交互：`:44` 允許待確認事項、Gate 豁免紀錄整節新增或刪除；`:47` 又凍結記帳章節內像標題的行與粗體開頭的行。兩者合起來，只有不含這兩類行的章節才能整節增刪。
   - 實測結果：
     - 以欄位寫法新增 Gate 豁免紀錄（`- **豁免項目**：…`）一律無效。這在 `c77928c` 就是如此，不是 S6 引入的。
     - 本機語料有 1 份 README 的待確認事項含 `###` 子標題，S6 之後整節刪除改判無效。
     - 新增區段若放在 Timeline 與 footer 之間，或刪除的是緊接 footer 的最後一節，footer 欄位會換到另一個章節，因此判定無效。範本把 Gate 豁免紀錄放在 Timeline 之前（`docs/agents/readme-templates.md:170`），照範本做不會碰到。
   - 這些都是 fail-closed，代價只是一次重審。語料中一般記帳（新增 Timeline 列並改狀態）117/117 有效，S6 沒有造成主路徑誤判。
   - 建議：在 `:44` 補半句，說明整節增刪時節內不能有標題或粗體開頭的行；`docs/AGENTS.md:129` 建議豁免紀錄用表格或一般清單。

5. **驗證狀態用詞**：`docs/rule-verification-status.md:308`。
   - 狀態定義（`:27`、`:336`）中，「曾失效並修正」指交付後在實跑中被發現執行不了。這一列的缺陷是交付前由 reviewer 的對抗腳本找到的，修正也只有腳本層驗證。
   - 已加註「（腳本層）」，讀者不會誤解，可以維持；或改成在驗證來源欄註明「審查發現」。

## 已查核維度

### 上次 MUST FIX／SHOULD FIX 的處理

| 項目 | 宣稱的處理 | 查核 | 結論 |
|---|---|---|---|
| MUST FIX 1 隨報告回填 | 採 (A)：review 技能步驟 5 補指示，新增 28e | `skills/review/SKILL.md:18` 已寫明「流程契約 2.4 起，報告記有核准基線且 README 仍為 `待提交` 時，保存報告的同一個提交把 `**核准 commit**` 改成該 SHA」；`:32` 的核准基線欄改為待提交時必填。fixture 查核：候選 28e 的 `e9c9a9e` 同時新增報告並把 `待提交` 改成 `ee1ad33…`；候選 28b3 的 `dd79e06` 回填 `94f4493`。reviewer 用 HEAD 腳本重跑，兩者都 OK | 已解決 |
| MUST FIX 2 28b2 誤記 | 更正紀錄、補「檢查器實際輸出」、新增 28b3 | `workflow-results:22` 改為實際訊息（第一個違規是 `implementation-plan.md`），並註明原紀錄是推斷。reviewer 自原始 stream-json 抽出第一輪 9 份與 S7 8 份的檢查器結果，和各證據檔附錄逐一相符（含「未取得判定」的權限拒絕）。`rule-verification-status:307` 改為「已實跑驗證（子情境）」，並寫明 28b2 擋下的是計畫檔、28b3 沒有執行檢查器 | 已解決 |
| SHOULD FIX 3 推導錨定 | pattern 錨定行首欄位 | `docs/agents/acceptance.md` 改為錨定 pattern。reviewer 實測：Timeline 提到 `**核准來源**` 時不會被選中；`- **核准來源**：`、`**核准來源**:`、`* **核准來源** ：`、縮排清單都能比對到；表格寫法沒有輸出，依規則判定缺少基線，屬 fail-closed。在 28e fixture 上，錨定版得到 `ee1ad33`，舊命令得到實作提交 `2db1d5f`，與回歸紀錄相符。紅燈測試 `test_baseline_ignores_text_mentioning_approval_source` 在 `s6-red.txt` 確實失敗 | 已解決 |
| SHOULD FIX 4 非範本寫法放行 | 收緊 `analyse()` 並檢查標題順序 | 上次列的向量全部改判無效：`**風險:**`、`__風險__`、`- **分級：**`、前置空白／tab／H1／`<h2>`／setext（`===`、`---`）、引用與清單裡的 fence、章節重排、重複 Timeline。`- - ```gherkin` 這種巢狀清單 fence 也無效。殘留項見 NICE 3 | 已解決 |
| SHOULD FIX 5 2.3 相容措辭 | 技能附 2.3 以下的章節名，步驟 3 改條件式 | `skills/review/SKILL.md:16`、`:18`，`skills/dev-cycle/SKILL.md:44` 已改。`check-kit.py` 通過，最低契約不變。`rule-verification-status` 新增一列「僅靜態撰寫」 | 已解決（未實跑，已登記） |
| SHOULD FIX 6 SCN-006 陳述 | 分列對照、補記帳提交數、28d 第二輪、S4 改為部分完成 | 回歸紀錄第一輪與綜合對照已分列「實跑前寫定」與「追加」，並寫明 0 對 0。基準 28b 只為記帳的提交 4 個（`5d8d961`、`aa08c96`、`98bd427`、`9aebb67`），候選 1 個，reviewer 逐一查核屬實。28d 第二輪：基準 `4192aa2` 只改核准 commit 一行，候選 `f963767` 維持 `待提交`。S4 已標「⚠️ 部分完成」並列出未達成的判準 | 已解決；計畫內殘留一句（NICE 1） |
| NICE 7～13 | S6 修正 | `diff.relative` 加子目錄 `--repo` 在 `--issue` 模式下改判無效（`relative_cfg.py`）；SHA 尾隨文字無效；平台模式新增負向測試；計畫第 11 行改正；核准基線欄位統一為待提交時必填；3.0 走現行判定；`skills/README.md:58` 改寫；環境段註明 kit HEAD；新增平台模式驗證列 | 已解決 |

### 驗收與證據

| SCN | 證據位置 | 結論 |
|---|---|---|
| SCN-001 | `test-evidence.py` 的有效案例。S7 候選 28b `59ae331`：一個提交保存報告、TBD-1 與 Timeline，檢查器 OK 並列出變更區段，最終輸出列出被審查 HEAD 與變更。28e `e9c9a9e` 的檢查器 OK 列出「新增報告、核准 commit」 | 成立 |
| SCN-002 | 腳本層有新增的負向測試（S6 紅燈 20 個失敗、綠燈 99 個通過），訊息都指出位置。reviewer 重現「只保留 README 變更的探測」：從 `4579fad` 取出 `94f4493` 的 README 與舊報告另行提交，檢查器判定無效並指向「Gherkin 驗收劇本」。agent 層 28b2、28b3 都有重審 | 成立。「只改驗收 → 檢查器無效」在 agent 層無法區分，已如實揭露 |
| SCN-003 | 舊判定類別測試。reviewer 以 v4.8.1 與 HEAD 腳本比對 10 種情境，2.3 與無契約下結果完全相同。2.3 下 `--issue` 只有在 HEAD＝R 時有效 | 成立，沒有 agent 實跑（已登記） |
| SCN-004 | 候選 28a `64029cc` 回填 `5b2416c`；28c `9ec4272` 回填 `ee1ad33`；28d 兩輪都維持 `待提交`。基準 28d 兩輪都有單獨回填提交（`b902cb2`、`4192aa2`） | 成立 |
| SCN-005 | Then 1：28e 的 reviewer 以錨定命令推導出 `ee1ad33`，報告記明命令與比對結果，Timeline 提到欄位名的實作提交沒有被選中。Then 2：28e、28b3 保存報告的提交都有回填。Then 3：只有命令測試 | Then 1、2 已在 agent 層實跑。Then 3 只有靜態撰寫與腳本測試，已登記 |
| SCN-006 | 回歸紀錄「第一輪」與「SCN-006 綜合對照」、`evidence/s7-rerun/`、fixture repo。實跑前寫定的 28b 兩輪候選，記帳提交 4→1、重審 1→0；追加的 28d 兩輪 1、1→0、0；28e 基準 RETURN 只因缺回填，候選 PASS 並隨報告回填；28b2、28b3 都沒有沿用 PASS | 成立。原判準下 28a＋28c 為 0 對 0，已分列揭露 |

S7 的前置條件與執行環境：
- `aa6e624` 的提交時間 17:24:03（+0800）早於 8 個 session 的第一筆事件 09:24:30Z（17:24:30 +0800），判定確實在實跑前寫定。
- 隔離設定 `home-cand2` 安裝的 `verify-artifact.py` 與 review `SKILL.md` 都和 `git show aa6e624:…` 相同。
- 2616e15 只改 `describe()` 的空行顯示，與回歸紀錄的說明相符。
- 8 個 repo 的測試都通過、工作樹乾淨、main 未移動、沒有 remote。
- fixture HEAD（`8b7b6e2`、`3fa47bc` 與第一輪三個 SHA）與回歸紀錄一致。

28b3 判為「無法區分」合理：
- expected.md 實跑前寫定「協調者若同次又改了其他檔案，判為無法區分」。`94f4493` 確實同時改了計畫 S1，補記新 Then 已由既有測試覆蓋。
- agent 也沒有執行檢查器（stream-json 只有一個被拒的 `ls`）。依寫定的判準，這一輪不能算通過，也不能算回歸。
- 協調者沒有挑選結果，也沒有修 fixture 重跑來換取通過。
- 「改驗收時協調者會一起改計畫」本身就是實務發現，回歸紀錄的「重跑觀察」已記錄。
- 28b3 跳過檢查器，偏離 review-evidence.md:39「一律以 `verify-artifact.py` 判定」，但方向是 fail-safe（直接重審），而且已在回歸紀錄第 82 行與驗證狀態揭露，不列為缺失。

根目錄五項檢查由 reviewer 於 2026-11-03 在 `9ee4139` 自行執行：

| 檢查 | 結果 |
|---|---|
| `check-kit.py` | exit 0 |
| `check-links.py` | exit 0 |
| `bash -n scripts/install.sh` | exit 0 |
| `test-install.py` | 14 個測試 OK，exit 0 |
| `test-evidence.py` | 99 個測試 OK，exit 0 |

### 相關失敗面

| 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
|---|---|---|---|
| 一般記帳：新增 Timeline 列、改狀態、改 TBD 狀態、清單式 Timeline | 有效 | 腳本測試；`adv2.py`；本機語料 117/117 | 通過 |
| 非範本寫法的標題、欄位、fence，章節重排或重複 | 無效 | 新測試與上次的對抗向量 | 通過 |
| Timeline 內 `###` 子標題、粗體開頭的註記、緊貼 footer `---` 的段落 | 凍結（setext 對讀者就是標題） | `adv2.py` | 無效，屬 fail-closed，符合設計邊界「所有章節標題」凍結 |
| 整節新增／刪除待確認事項、Gate 豁免紀錄（表格或一般清單） | 有效 | 腳本測試；`adv2.py` | 通過 |
| 整節增刪時節內有欄位寫法或子標題；新節插在 Timeline 與 footer 之間 | 設計上未明說 | `adv2.py`、語料 | 無效，屬 fail-closed（NICE 4） |
| 重複新增待確認事項、把它搬到 Gherkin 之前 | 無效 | `adv2.py` | 通過 |
| 待確認事項改名為 Gate 豁免紀錄 | 等同刪一節加一節 | `adv2.py` | 有效，符合已核准的整節增刪 |
| HTML 標題或粗體、`|` 段落接 `---` | 理想上無效 | `adv2.py` | 放行（NICE 3） |
| 縮排程式碼區塊、無粗體純文字欄位、只改 mode | 已知限制 | 對抗腳本 | 放行；揭露不完整（NICE 2） |
| 核准 commit：SHA 加尾隨文字、非祖先、另一個 SHA | 無效 | 新測試 | 通過；回填成 R 本身依設計有效 |
| `diff.relative` 加子目錄 `--repo`（兩種模式） | 無效 | 新測試；`relative_cfg.py` | 通過 |
| 3.0 契約、2.3、無契約 | 現行判定 | 新測試；`legacy_equiv.py` | 通過 |
| 推導基線：Timeline 或說明文字提到欄位名、各種欄位寫法、表格寫法 | 選中真正的核准提交；表格寫法判定缺少基線 | 新測試；reviewer 實測；28e 實跑 | 通過 |

### 需求、架構、安全、品質

- **需求**：S6 的收緊都落在設計邊界「所有章節標題與順序」「記帳區段內外的其他粗體欄位行」凍結的範圍內，方向只會更嚴，沒有放寬 TBD-1～3 的核准內容。S7 在實跑前補寫判準，沒有改動既有判準。
- **單一說法**：「核准 commit 為 `待提交` 時必填核准基線」「2.4 起隨報告回填」「契約取自被審查提交、限 2.x」三點，在 review 技能、review-evidence.md、acceptance.md、CHANGELOG 4.9.0 與計畫中都一致。殘留的不一致只有計畫內兩處陳述（NICE 1、2）。
- **版本**：文件版本 2.8、流程契約 2.4、CHANGELOG [4.9.0] 彼此一致。技能的最低契約沒有改，check-kit 也確認相容。安裝指令沒有變，INSTALL.md 不需要更新。雙語 rules 沒有改動。
- **安全**：腳本維持唯讀。改用 plumbing 的 `diff-tree` 加 `--show-toplevel`，不再受使用者的 diff 設定影響。
- **品質**：
  - 新判定集中在 `analyse()` 與 `check_readme()` 開頭的標題順序檢查，`legacy()` 沒有改動，沒有分歧的重複邏輯。
  - 新測試以真實 Git 執行，負向測試都斷言違規位置。紅燈有 20 個失敗，每一項都對應上次指出的放行路徑，沒有發現假綠燈。
  - `s6-green.txt` 隨 2616e15 提交，不在修正提交 36b0da5 內。reviewer 在 HEAD 重跑同樣是 99 個 OK。

### 豁免、待確認與限制

- README 沒有 Gate 豁免紀錄，TBD-1～3 都已解決，本次沒有需要使用者決策的項目。
- 已揭露且屬實的限制如下。依 verification.md，揭露的限制不構成缺失：
  - S4 部分完成：WF-14 沒有重跑，刪除核准來源行的對照組沒有 agent 實跑。
  - 「只改驗收 → 檢查器無效」在 agent 層無法區分。
  - 2.3 相容措辭與平台模式只有靜態撰寫或腳本測試。
  - 只測 Claude Code，每案例每組一到兩輪。
  - fixture 的 28b 報告前提有誤。
- reviewer 沒有重跑宿主 agent。S7 的 agent 行為依 fixture 的 Git 歷史與原始 stream-json 查核。對抗腳本與語料模擬放在 reviewer 的 scratchpad，不是永久產物。

## 流程判定
PASS
