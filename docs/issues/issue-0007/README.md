# Issue 7 - 狀態值的說明與待確認事項狀態的檢查 (Small)

## 概述

來源：[GitHub #7](https://github.com/raybird/dev-rules-kit/issues/7)，v4.10.0 發布前的下游試用回報。本 issue 只處理其中第 1、2 點（2026-11-12 使用者指定先做這兩點）；第 3、4 點留在 GitHub #7，之後另行處理。

1. `docs/AGENTS.md`「合法的中間狀態與終態」表只列了需要額外紀錄的三個 `**狀態**` 值。下游 agent 把它讀成只能用這三個值，issue 在審查 PASS、等待合併期間一直寫「待審查」。其他狀態值並沒有被禁止，是標題與說明寫得不清楚。
2. 待確認事項的狀態寫成規定以外的值（試用時寫成「接受為殘餘風險」），沒有工具發現。懸置掃描只認 `待確認` 與 `不影響本次交付`，其他值兩類都不命中，會被默默略過。

2026-11-12 以 [scan_vocab.py](evidence/scan_vocab.py) 唯讀統計 683 份不重複的下游 issue README；2026-11-13 依 review-a77b097、review-d49e8fc 改用與檢查器相同的去符號與切欄規則重跑，下游多 1 份共 684 份，以下為重跑的數字，結果 [s0-scan.txt](evidence/s0-scan.txt)。第一次統計的切欄沒有跳過跳脫的直線符號，當時算出規定以外 201 列 75 份：

- `**狀態**` 有 521 種寫法：375 份是三個特殊值以外的自由描述；以 `已完成` 開頭的 230 份多數在後面加括號說明（例如 `已完成（2026-10-12 併入 dev …）`）。
- 待確認事項狀態欄共 1939 列：1695 列（345 份）以三個值之一開頭；47 列（19 份）加了粗體、反引號或 ✅ 等圖示，去掉後是三個值之一；197 列（72 份）是規定以外的值，最常見的是日期開頭、「已確認」「已定案」「已決定」。

2026-11-13 使用者決定第 3～5 點也在本 issue 處理（AC-5～AC-7，見「第 3～5 點」）。第 1、2 點的交付不在範圍：`**狀態**` 值本身的檢查（自由描述是允許的）。

## 現況

**現行 review**: review-92c1f63.md

| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |
|---|---|---|---|
| 併入本機 main | git merge-base --is-ancestor issue-0007-status-vocabulary main | 已併入（merge commit c83b2d4） | 2026-11-13 |
| 下游試用 | 向試用專案的 session 詢問試用結果 | 一個下游專案以 f249d5a 跑完一個實際 issue：懸置掃描列出 4 列舊的不合法狀態、沒有誤報，合法寫法都放行；agent 依新說明改用自由描述的狀態；verify-artifact 判定 OK、沒有提醒（正確）。回報的圖示範圍不清，發布前改為列出例子 | 2026-11-13 |
| 推送到 origin/main | git fetch origin 後執行 git merge-base --is-ancestor c83b2d4 origin/main | 已推送（exit 0），隨 v4.11.0 發布（tag 指向 175bc7d） | 2026-11-13 |

## 涉及檔案

- `docs/AGENTS.md` - 狀態表改標題、補一句說明；修訂紀錄
- `docs/agents/verification.md` - 指向該表的錨點
- `skills/dev-cycle/references/pending-scan.md` - 新增偵測類型「待確認狀態不合法」
- `skills/review/scripts/verify-artifact.py` - 待確認事項新增或修改的列狀態不合法時印提醒
- `scripts/test-evidence.py` - 提醒的正負向案例
- `CHANGELOG.md`、`docs/rule-verification-status.md`

## 驗收條件

1. **AC-1**：`docs/AGENTS.md` 的狀態表標題改為「有特殊意義的狀態值」，並說明：其他進度可以自由描述（例如「實作中」「審查通過，待合併」）；表中三個值要寫在 `**狀態**` 開頭，後面可以接括號說明。指向該表的連結同步更新。 — 檢查方式：`check-links.py` OK；`grep` 確認舊標題只剩 CHANGELOG 與 issue 歷史文件
   - 失敗路徑：連結失效，或說明沒有列出自由描述的例子
2. **AC-2**：懸置掃描新增偵測類型「待確認狀態不合法」：狀態欄去掉開頭的粗體、反引號與 ✅⏳📝 等符號後，不是以 `待確認`、`已解決`、`不影響本次交付` 之一開頭；歸在「建議整理」。 — 檢查方式：候選組以隔離設定實跑 2 輪懸置掃描，fixture 含規定以外的值、加粗體的標準值與一般標準值各一列；判準先寫進 fixtures/expected.md 並提交
   - 失敗路徑：規定以外的值沒列出，或加粗體的標準值被列出
3. **AC-3**：`verify-artifact.py` 在被審查提交到 HEAD 之間，README 待確認事項新增或修改的列，狀態欄依 AC-2 的規則不合法時，在判定結果之後多印一行提醒，指出編號與寫法，並列出三個合法值。OK／INVALID 與 exit code 不變；未修改的舊列不提醒；提醒的計算出錯時不影響判定。 — 檢查方式：`test-evidence.py` 新增案例先紅後綠：新增不合法列 → OK 加提醒；新增加粗體的標準值 → 無提醒；舊的不合法列沒有修改 → 無提醒；INVALID 時也附提醒，exit code 仍為 1
   - 失敗路徑：任何一個案例不符，或既有案例失敗
4. **AC-4**：一般記帳提交的判定不變。 — 檢查方式：既有測試全部通過；以本分支的檢查器重判 issue #4 的 wf28b3、issue #3 的 wf31，以及 v4.10.0 下游試用的 5 個記帳判定，判定與 exit code 都不變，記錄有無提醒
   - 失敗路徑：任何一個判定或 exit code 改變

## 風險與首要驗證

- **最大風險**：提醒的程式出錯，讓檢查器在原本 OK 的記帳提交上崩潰或改變 exit code，擋住 PASS 沿用
- **風險等級與理由**：Medium。提醒本身不改判定，但寫在 PASS 能否沿用的 gate 裡
- **首要驗證**：AC-3 的 exit code 案例與 AC-4 的重判，先於懸置掃描實跑
- **選擇理由**：直接量測判定有沒有被影響
- **完成證據**：測試輸出與重判結果

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | review-a77b097 PASS 後的 NICE TO HAVE 5 項（含 1 項 `需決策`：去符號的範圍）要不要在分支上修 | 已解決：2026-11-13 使用者選「修 1、2、3 並覆審」；去符號收窄為粗體、反引號、空白與圖示，刪除線與括號不去；第 4、5 項不修（只影響提醒，第 4 項的措辭早於本 issue） | AC-2、AC-3 |
| TBD-2 | review-d49e8fc 的 SHOULD FIX 2 項（表格列不寫結尾直線符號時讀不到整張表；README 與 CHANGELOG 的統計數字與重跑結果不符）要不要在分支上修 | 已解決：2026-11-13 使用者選「兩項都修並覆審」；統計腳本一併改用相同切欄方式（同報告 NICE TO HAVE 1）；pending-scan.md 規則文字不變，不重跑 WF-34 | AC-3 |
| TBD-3 | review-10af0b4 的 NICE TO HAVE 3 項（含 1 項 `需決策`：AC-5 的「重導」範圍太寬）要不要在分支上修 | 已解決：2026-11-13 使用者選「三項都修並覆審」；AC-5 收窄為「管線或 `<`」，並查證跳脫的直線符號在現況表判 OK，但照原文複製執行會出錯，所以管線仍登記在 project.md；第 6 項的可選做法拆開並各附代價；project.md 範本補取名稱的說明 | AC-5、AC-7 |

## 第 3～5 點（2026-11-13 規格修訂）

來源：v4.10.0 試用回報第 3、4 點；v4.11.0 試用回報（記為 GitHub #7 第 5 點）。

- **第 3 點**：`## 現況` 的查證命令寫在記帳章節，不能含 `<`，表格儲存格也不能有未跳脫的直線符號，所以不能接管線或重導。試用的 agent 改用 `-q`、`&& echo yes` 繞過。另外，外部狀態不再適用時（例如改為只推主幹後的「分支推送」列），「上次結果」只能寫成說明文字。project.md「提交與交付」已可登記查證命令（v4.10.0 起），但 `## 現況` 的說明沒有指過去。
- **第 4 點**：使用者決定「之後另開 issue」時，追蹤 issue 開好之前，待確認事項只能先記 `待確認`。試用的 agent 這樣做是對的，但規則沒有寫，它不確定算不算合規。
- **第 5 點**：審查 PASS 之後，`docs/AGENTS.md` 工作流程第 6 項列出的可選做法之一是「提交到主幹」。以快轉合併的專案，主幹多了提交，被審查分支就不能快轉合併。試用的 agent 只好先把那個提交從主幹拿下來，等合併後再補。

5. **AC-5**：`docs/agents/document-types.md` 外部狀態表的說明補上兩件事。一是查證命令含管線或 `<` 時，命令登記在 project.md「提交與交付」，表格只寫它的名稱（2026-11-13 依 review-10af0b4 TBD-3 修訂：原為「需要管線、重導或 `<`」，只用 `>` 的命令可以直接寫在表格；project.md 範本同步補一句）；二是外部狀態不再適用時刪掉該列，不寫成說明文字。檢查器不動。 — 檢查方式：靜態核對文字；check-kit、check-links OK
   - 失敗路徑：說明要求在表格裡寫含 `<` 或直線符號的命令，或檢查器行為改變
6. **AC-6**：`docs/AGENTS.md`「待確認事項」補一句：決定另開追蹤 issue、還沒開好時維持 `待確認`，並寫明要開的 issue；開好後改為 `不影響本次交付`，寫上編號。 — 檢查方式：靜態核對文字
   - 失敗路徑：沒有寫出空窗期間的狀態值
7. **AC-7**：`docs/AGENTS.md` 工作流程第 6 項列可選做法時，一併說明各做法的代價；「提交到主幹」要寫明以快轉合併的專案，被審查分支會因此無法快轉合併。 — 檢查方式：靜態核對文字；發布前在一個下游實際 issue 試用時觀察 agent 列選項的方式
   - 失敗路徑：可選做法沒有提到快轉的代價

第 3、5 點會改變 agent 的做法，依維護指引屬行為變更：發布 v4.12.0 前在一個下游實際 issue 試用。不另做回歸實跑，rule-verification-status 先標「僅靜態撰寫」，試用後依結果更新。

- **核准日期**: 2026-11-13
- **核准來源**: 2026-11-13 使用者要求「第5點也放進去」，並對 AC-5～AC-7 回覆「核准」；同日 AC-5 依 review-10af0b4 的需決策項修訂，使用者選「三項都修並覆審」（TBD-3）
- **核准 commit**: e1bbf05

## 實作與驗證步驟

1. ✅ **AC-3、AC-4：檢查器提醒** — 先寫紅燈案例，再實作；重判實跑與下游試用的記帳提交
   - 完成證據：2026-11-12。
     - 紅燈：[s1-red.txt](evidence/s1-red.txt)，新增 6 個測試方法（四個測試類別各繼承一次，共 24 項），3 個正向案例（修改的列、新增的列、INVALID 時仍提醒）共 12 項因沒有提醒而失敗；3 個負向案例（加粗體與 ✅ 的標準值、未修改的舊列、表頭沒有狀態欄）通過，作為不變的保障。
     - 實作：`main()` 印出判定之後，另以 `tbd_reminders()` 比對被審查提交與 HEAD 的待確認事項表格，依編號找出新增或內容改變、狀態不合法的列，在 stdout 多印一行提醒，引用狀態欄前 20 個字。判定、輸出到 stderr 的 INVALID 與 exit code 不變；提醒的計算有任何例外都略過。
     - 綠燈：[s1-green.txt](evidence/s1-green.txt)，284 項通過。
     - 依 [review-a77b097](review-a77b097.md) 修正（2026-11-13，TBD-1）：紅燈 [s3-red.txt](evidence/s3-red.txt)，事項欄含跳脫的直線符號時切欄錯位而誤報（4 項），刪除線、全形括號與連結開頭的狀態被當成合法（3 個子案例 × 4 類別）；實作後切欄跳過跳脫的直線符號，去符號只去粗體、反引號、空白與 Unicode 圖示（So 類）；綠燈 [s3-green.txt](evidence/s3-green.txt) 292 項通過。
     - 依 [review-d49e8fc](review-d49e8fc.md) 修正（2026-11-13，TBD-2）：紅燈 [s4-red.txt](evidence/s4-red.txt)，表格列不寫結尾直線符號時整張表讀不到、沒有提醒（4 項）；實作後列結尾的直線符號可省略（列仍要以直線符號開頭）；綠燈 [s4-green.txt](evidence/s4-green.txt) 296 項通過。統計腳本改用同一種切欄方式重跑。
     - AC-4 重判：[s1-rejudge.md](evidence/s1-rejudge.md)（兩次修正後各重跑一次，結果與修正前相同）。issue #4 的 wf28b3、issue #3 的 wf31 與 v4.10.0 下游試用的 5 個記帳判定，main 版與本分支版的 exit code 都是 0、判定輸出相同，都沒有提醒。另外重判下游試用寫入「接受為殘餘風險」的那個記帳提交（之後已改正）：兩版都判 OK，本分支版多一行提醒指出該列，這是 #7 第 2 點的真實案例。
2. ✅ **AC-1、AC-2：文件與懸置掃描** — 改狀態表與 pending-scan.md；寫定 fixture 與判準並提交後，實跑 2 輪（相依：1）
   - 完成證據：2026-11-12。
     - AC-1：`docs/AGENTS.md` 標題改為「有特殊意義的狀態值」，表格前補一句說明自由描述的例子與「寫在開頭、後面可接括號說明」，文件版本 2.10；`docs/agents/verification.md` 的錨點同步。check-links OK；舊標題只剩 CHANGELOG、rule-verification-status 的歷史列與 issue 文件。
     - AC-2：`pending-scan.md` 偵測規則新增「待確認狀態不合法」，回報版面歸在建議整理。判準 [fixtures/expected.md](fixtures/expected.md) 與 fixture [build_fixtures.py](fixtures/build_fixtures.py) 先在 `8948ad9` 提交，候選組（kit `8948ad9`）以隔離設定實跑 2 輪：[r1](evidence/s2-wf34/wf34-r1.md)、[r2](evidence/s2-wf34/wf34-r2.md)。兩輪都在「建議整理」列出 3401，指出 TBD-1 的「已定案」不是三個值之一（r2 直接寫出偵測類型名稱）；3402 的粗體標準值與 3403 都沒有列出，兩輪都另外說明 3402 去掉粗體後合法；回合前後 HEAD 與工作樹雜湊相同；沒有權限拒絕。2／2 通過。
     - 依 review-a77b097 修正後重跑（2026-11-13）：重跑範圍先寫進 expected.md 並在 `e19b10d` 提交，候選組以 kit `e19b10d` 重新安裝隔離設定，實跑 2 輪：[r1](evidence/s3-wf34/wf34-r1.md)、[r2](evidence/s3-wf34/wf34-r2.md)。兩輪都以「待確認狀態不合法」列出 3401，3402、3403 只說明為合法；前後 HEAD 與工作樹雜湊相同。r2 有一次讀檔的複合命令被權限拒絕，agent 改用其他方式讀完三份 README。2／2 通過。
3. ✅ **收尾** — CHANGELOG、rule-verification-status；送獨立審查（相依：2）
   - 完成證據：2026-11-13 CHANGELOG 4.11.0、rule-verification-status 已更新。獨立審查 [review-a77b097](review-a77b097.md) PASS，依使用者決定修正 NICE TO HAVE 1～3 後，差異覆審 [review-d49e8fc](review-d49e8fc.md) PASS；再修正其 SHOULD FIX 2 項後，差異覆審 [review-b30f339](review-b30f339.md) PASS。該報告留下的 SHOULD FIX（措辭寫成列開頭的直線符號也可省略）與 NICE TO HAVE（多餘的括號）依使用者決定在合併後於 main 修正

4. ⏳ **AC-5～AC-7：文件** — 改 document-types.md 與 docs/AGENTS.md，文件版本 2.11；CHANGELOG 4.12.0、rule-verification-status；送獨立審查
   - 完成證據：2026-11-13 已修改 document-types.md「`## 現況`」的外部狀態表說明（AC-5）、docs/AGENTS.md 待確認事項（AC-6）與工作流程第 6 項（AC-7），文件版本 2.11；CHANGELOG 4.12.0（未發布）、rule-verification-status 新增三列「僅靜態撰寫」。五項檢查通過。獨立審查 [review-10af0b4](review-10af0b4.md) PASS；依 TBD-3 修正三處措辭並補 project.md 範本後，五項檢查通過，待差異覆審

- **核准日期**: 2026-11-12
- **核准來源**: 2026-11-12 使用者要求「開始處理 #7」（先做第 1、2 點），並選定：狀態表「改標題並補一句」、檢查方式「懸置掃描列出＋檢查器提醒」、加粗體或符號的標準值「算合法」；同日使用者對 AC-1～AC-4 回覆「核准」
- **核准 commit**: 94c44d2

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-12 | 建立；統計下游 683 份 README 的狀態值；使用者選定三項做法 | 使用者／Claude Code |
| 2026-11-12 | 使用者核准 AC-1～AC-4 | 使用者 |
| 2026-11-12 | 獨立審查 [review-a77b097](review-a77b097.md) PASS，沒有 MUST FIX 與 SHOULD FIX；NICE TO HAVE 5 項待使用者決定 | Claude Code |
| 2026-11-13 | 使用者決定修 NICE TO HAVE 1～3 並覆審（TBD-1），PASS 失效 | 使用者／Claude Code |
| 2026-11-13 | 差異覆審 [review-d49e8fc](review-d49e8fc.md) PASS，SHOULD FIX 2 項待使用者決定；報告沒有照抄範本的 PASS 提醒行 | Claude Code |
| 2026-11-13 | 使用者決定兩項 SHOULD FIX 都修並覆審（TBD-2），PASS 失效 | 使用者／Claude Code |
| 2026-11-13 | 差異覆審 [review-b30f339](review-b30f339.md) PASS；SHOULD FIX 1 項（措辭寫成開頭直線符號也可省略，實作只支援結尾）待使用者決定 | Claude Code |
| 2026-11-13 | 使用者決定措辭在合併後修；以 `--no-ff` 合併到本機 main（`c83b2d4`），在 main 修正兩處文字；未推送，GitHub #7 維持開啟（第 3、4 點未處理）；標記已完成 | 使用者／Claude Code |
| 2026-11-13 | 下游試用完成；使用者決定先在 main 補寫圖示範圍再發布，主幹補提交擋住快轉的回報記在 GitHub #7 | 使用者／Claude Code |
| 2026-11-13 | 推送 main 並發布 v4.11.0；GitHub #7 維持開啟（第 3～5 點） | 使用者／Claude Code |
| 2026-11-13 | 規格修訂：使用者決定第 3～5 點也在本 issue 處理，新增 AC-5～AC-7 | 使用者／Claude Code |
| 2026-11-13 | 使用者核准 AC-5～AC-7 | 使用者 |
| 2026-11-13 | 第 3～5 點獨立審查 [review-10af0b4](review-10af0b4.md) PASS，沒有 MUST FIX 與 SHOULD FIX；NICE TO HAVE 3 項（1 項需決策）待使用者決定 | Claude Code |
| 2026-11-13 | 規格修訂：使用者決定修 review-10af0b4 的 NICE TO HAVE 1～3 並覆審（TBD-3），AC-5 收窄為「管線或 `<`」，PASS 失效 | 使用者／Claude Code |
| 2026-11-13 | 差異覆審 [review-92c1f63](review-92c1f63.md) PASS；SHOULD FIX 1 項（改 project.md 範本時漏加舊雜湊，v4.10.0 起已漏一個，需決策）待使用者決定 | Claude Code |

---
**建立日期**: 2026-11-12  
**分級**: Small  
**風險**: Medium  
**狀態**: 實作中（第 3～5 點）
