# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，34 個提交、102 個檔案）。第九輪覆審。**依 README 待確認事項 TBD-7（使用者 2026-11-11 決定），本輪只深入審查第八輪之後的差異 `73202f8..c6eb117`**（`1b59d52` 保存第八輪報告、`486936a` 修正、`c6eb117` 重跑紀錄，14 個檔案）。更早的範圍已經過八輪審查，只做抽查：重跑前幾輪的對抗案例，以及自行執行五項檢查。
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：c6eb1171f88d508fd9d12b62a41678874881be14
- Reviewed patch-id：459a03b7df55b9b1277c72946014b3e332e48faa（2026-11-11 以 `git diff 46e09a5 c6eb117 | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-c6eb117.md
- 審查日期：2026-11-11
- 審查依據：
  - README `## 待確認事項` TBD-2～TBD-7 的使用者決定。
    - TBD-3：跨行 HTML 區塊在本 issue 一起收緊。
    - TBD-6：記帳章節含 `<` 的行一律凍結，不模擬 CommonMark。code span 裡的標籤名與佔位字因此判需重審，是已接受的代價。
    - TBD-7：新找到的「記帳提交利用 Markdown 渲染藏住凍結內容」寫法，前提是被審查版本已違反撰寫規範（`docs/AGENTS.md:139`「不含 `<`」等），而且下游 0 份符合時，不列 MUST FIX，登記到 #5。
    - TBD-5 由 GitHub #4 處理，不在本 issue 範圍。
  - 已登記在 #5 的 V3、V4、V6、V7，以及 CHANGELOG 4.10.0「已知限制」（`CHANGELOG.md:36`）的項目不重報。
  - 判斷是否 v4.9.0 起就有：同一個案例也用 `46e09a5` 的檢查器跑一次，判 OK 的就是 v4.9.0 起就有。

## 問題與風險

### MUST FIX

無。本輪找到的三種藏住凍結內容的新寫法，前提都是被審查版本的記帳章節已含 `<`，下游 0 份符合，依 TBD-7 列在「登記到 #5 的寫法」。

### SHOULD FIX

1. **凍結章節的 code span 寫了沒有結束字串的 `<?php`、`<!DOCTYPE html` 時，之後整份文件都凍結，正當記帳提交被誤判 INVALID，文件沒有說明**
   - 位置：
     - `skills/review/scripts/verify-artifact.py:238-240`：`unclosed()` 在所有章節都會呼叫，不限記帳章節。
     - `:189-193`：進入未關閉狀態後，每一行都直接 `continue`，連 `##` 標題都不辨認，一路到結束字串。
   - 原因：
     - 撰寫規範只限制記帳章節不含 `<`（`docs/AGENTS.md:139`），凍結章節（設計邊界、概述、Gherkin 劇本 fence 外的文字）寫 `` `<?php` `` 是正當的。
     - `486936a` 把追蹤範圍從 `<!--` 擴大到 `<?`、`<!` 接英文字母與 CDATA，而且不看位置，code span 裡的也算。
     - 所以凍結章節出現 `` `<?php` ``、`` `a<?b` ``、`` `<!DOCTYPE html` `` 這類行內文字，就會凍結到下一個 `?>`、`>`。沒有結束字串時一路凍結到檔尾，後面的 Timeline、待確認事項標題都被吞掉。
   - 實測（`<tmp>/review9/adv/cases-r9b.py`）：被審查版本在 `## 設計邊界` 寫一行文字，記帳提交只在 Timeline 補一列。

     | 案例 | 設計邊界的文字 | HEAD | `73202f8` | `46e09a5` |
     |---|---|---|---|---|
     | D1 | ``檔案以 `<?php` 開頭。`` | INVALID | OK | OK |
     | D2 | ``輸出前加 `<!DOCTYPE html` 宣告。`` | INVALID | OK | OK |
     | D3 | ``比較式 `a<?b` 不成立。`` | INVALID | OK | OK |
     | D4（對照） | ``註解寫法 `<!--` 不用。`` | INVALID | INVALID | OK |
     | D5 | 待確認事項的列寫 `` `<?php` ``（違反撰寫規範），之後在 Timeline 補一列 | INVALID | OK | OK |

   - 錯誤訊息也會誤導：D1 的訊息說被審查版本是「章節「設計邊界」的空行」，目前是「章節「設計邊界」的「\| 2026-11-11 \| 第二輪 \| Claude \|」（記帳章節含 `<` 或以 `[` 開頭的行一律凍結）」。Timeline 的列被算成設計邊界的內容，使用者看不出原因是前面章節的 `` `<?php` ``。
   - 影響：
     - 只會多判 INVALID，不會藏住內容。
     - 目前下游 0 份受影響：`73202f8` 與 HEAD 的 `analyse()` 對本機 687 份不重複的 README，結果 0 份不同（`<tmp>/review8/cmp_fix.py`，README 清單沿用 review7）。
     - 有 PHP、XML、HTML 需求的下游專案，在 issue 說明裡寫 `` `<?php` `` 很自然，遇到時判需重審，而且看不出原因。
     - `<!--` 的同一行為（D4）從 `## 現況` 收緊時就有，這一輪擴大到更常見的寫法。
   - 建議（擇一或併用）：
     - 至少補文件：`review-evidence.md:51` 與 `CHANGELOG.md` 的「下游更新」補一句：「任何章節（包括凍結章節的 code span）有未關閉的註解、處理指令、宣告或 CDATA 時，之後到結束字串為止都凍結，可以跨章節；凍結章節寫 `<?php` 這類字樣時，同一行補上結束字串，或放進 code fence。」
     - 訊息：進入未關閉狀態時記下開頭所在的行，錯誤訊息改成指出它，例如「（第 N 行的 `<?` 尚未關閉）」。
     - 若要縮小範圍：`<?`、`<!` 接字母與 CDATA 在瀏覽器裡遇到第一個 `>` 就結束，只有出現在行首（容器前綴之後）時才可能開出跨空行的 HTML 區塊。可以只在行首追蹤這三種，`<!--` 維持任何位置。這會稍微模擬 CommonMark，和 TBD-6 的方向有出入，採用前要先問使用者。

### NICE TO HAVE

1. **「同一行關閉後又開新的」沒有測試擋住**（`<tmp>/review9/m24b/`）：
   - 變異：把 `unclosed()` 找到結束字串後的 `pos, closer = end + len(closer), None` 改成 `return None`，也就是不再找同一行後面新開的。
   - 結果：`test-evidence.py` 232 項仍全過，變異存活。
   - 原因：`test_comment_reopened_after_close_stays_frozen`（`scripts/test-evidence.py:563-569`）重新開的註解和被改的行在同一段落，段落凍結就擋住了，不需要靠 `unclosed()`。
   - 對抗案例 A1、A3、A6（見下方）證明現行程式是對的，只是沒有測試保護。
   - 建議：補一個 `<?x 甲 ?> 乙 <?y`、空行、`?>` 的案例。新案例目前只寫在 Timeline，也可以順便補一個 `## 現況` 的版本（第八輪的 MUST FIX 是在 `## 現況`）。
2. **立即關閉的寫法被當成未關閉**（A7～A9）：
   - `<!-->`、`<!--->`、`<?>` 在 CommonMark 是同一行就關閉，`unclosed()` 從開頭字串之後才找結束字串，所以判成未關閉，一路凍結到下一個結束字串。
   - `<!-->` 在 `73202f8` 判已關閉，這是小幅退步。
   - 只會多判 INVALID；記帳章節裡寫這些本來就違反撰寫規範，下游 0 份。可以併入 SHOULD FIX 1 的文件說明。
3. **`verify-artifact.py:10` 的 docstring 沒有跟著改**：
   - 仍寫「未在同一行關閉的註解到 `-->` 為止整段凍結」。
   - `review-evidence.md:51`、`CHANGELOG.md:31` 與 `rule-verification-status.md:327` 都已經改成四種。
4. **`implementation-plan.md:287` 的對抗案例描述不夠精確**：
   - 寫「Z1 系列與 Z1u … Z5、Z5t … 判 OK」。但 Z1-2.4 與 Z5-2.4 在流程契約 2.4 下判 INVALID，這是正確的。
   - 判 INVALID 的 Z2c（對照）、Z2r、Z2m 沒有列出。
   - reviewer 重跑 21 個案例，判定與這段文字的實質內容相符，只是寫法讓人以為 Z1 系列全部 OK。

### 登記到 #5 的寫法

以下三種寫法的前提，都是被審查版本的記帳章節已經含 `<`，違反 `docs/AGENTS.md:139`。下游 0 份符合（`<tmp>/review9/scan_r9.py`，本機 687 份不重複的 README，2026-11-11 掃描，只輸出筆數）。依 TBD-7 不阻擋本 issue。

所有案例的被審查版本，兩個渲染器都看得到哨兵文字（`<tmp>/review9/adv/before.py`）。下表的渲染結果是記帳提交之後的版本。

| 編號 | 寫法 | 前提 | HEAD | `73202f8` | `46e09a5`（v4.9.0） | 渲染結果 | 下游分布 |
|---|---|---|---|---|---|---|---|
| R9-1（A10） | 被審查版本的記帳章節有一行小寫的 `<![cdata[ 舊說明`，結束字串 `]]>` 在空行之後的另一段；記帳提交刪掉 `]]>` | 記帳章節含 `<` | 現況、Timeline 都 OK | 都 OK | 現況 INVALID、Timeline OK | marked：之後全部變成註解。micromark：看得到（CDATA 只認大寫） | 任何大小寫的 `<![cdata[`：0 處 |
| R9-2（B1～B3） | 檢查器當成 code fence、渲染器不當的行，裡面包著 HTML 區塊的開頭字串，結束字串在 fence 之後的另一段；記帳提交刪掉結束字串。B1：info string 含反引號（`` ``` a`b ``）；B2：同 B1，但用 `<!--` 與 `-->`；B3：段落後四格縮排的 ```` ``` ```` | 記帳章節含 `<` | 現況、Timeline 都 OK | 都 OK | 現況 INVALID、Timeline OK | B2 兩個渲染器都藏住之後全部內容；B1、B3 是 micromark 藏住（照規格，info string 不能含反引號，段落中的縮排行是續行），marked 把它當 fence | 記帳章節裡檢查器當成 fence 的行：1 份 1 行，fence 裡有 HTML 開頭字串：0 行 |
| R9-3（C1、C2） | 被審查版本的記帳章節有一行縮排的 `<!-- 舊說明`（C1 四格，是縮排程式碼區塊；C2 兩格），`-->` 在空行之後的另一段。記帳提交在它前面新增一個清單項加空行，縮排行被收進清單項，HTML 區塊在清單結束時跟著結束，`-->` 變成跳脫過的文字，瀏覽器的註解就不會關閉 | 記帳章節含 `<` | 現況、Timeline 都 OK | 都 OK | 現況 INVALID、Timeline OK | 兩個渲染器都藏住之後全部內容（`ol>li`、`ul>li` 裡的註解） | 記帳章節裡縮排的 HTML 開頭字串：0 行 |

- 是否 v4.9.0 起就有：
  - 三種在 Timeline 都是 v4.9.0 起就有，`46e09a5` 也判 OK。
  - 在 `## 現況` 是本 issue 新引入：流程契約 2.5 把它列入記帳區段，`46e09a5` 把它當凍結章節，判 INVALID。前提的性質和 V7 相同。
  - R9-1 是 `486936a` 修法沒有涵蓋到的大小寫變體。R9-2、R9-3 的 `<!--` 版本在第八輪之前就有，`486936a` 只是讓 `<?`、`<!X` 也適用 R9-2。
- GitHub 的實際結果沒有實測，是推論：
  - R9-1：cmark-gfm 的 `scanners.re` 用 re2c 的單引號字串寫 `<![CDATA[`，不分大小寫，推論 GitHub 上會和 marked 一樣藏住。
  - R9-2、R9-3：照 CommonMark 規格推論，GitHub 和 micromark 相同。
- R9-3 的 C1 和 CHANGELOG 已知限制裡的「縮排程式碼區塊」重疊，但影響比第八輪的 Z5 大：Z5 用的是 `<details>`，會被 `</li>` 關掉；`<!--` 不會被 `</li>` 關掉，會藏住之後的全部內容。C2 不是縮排程式碼區塊，不在已知限制裡。所以兩者一起登記。
- 修法方向，供 #5 參考：
  - R9-1：`HTML_OPENER` 加上 `re.I`，結束字串用大寫查表，約 2 行。
  - R9-2：fence 狀態裡也呼叫 `unclosed()`，收尾 fence 之後延續未關閉的狀態；也可以讓記帳章節裡出現 fence 就整段凍結到下一個標題。
  - R9-3：縮排的 `<!--` 行（行首有空白）之前的記帳內容也凍結；或者記帳章節裡出現跨空行的 `<!--` 時，前一段凍結。

### 需決策

無。SHOULD FIX 1 如果要縮小追蹤範圍（只在行首追蹤 `<?`、`<!X`、CDATA），會稍微模擬 CommonMark，和 TBD-6 的方向有出入，採用前要先問使用者。只補文件與訊息，不需要決策。

## 已查核維度

### 上一輪發現的處理

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：`## 現況` 裡 HTML 區塊第 3～5 型的結束行可以刪掉 | `unclosed()` 取代 `opens_comment()`（`verify-artifact.py:109-125`），兩個呼叫點（`:191`、`:240`）改傳結束字串；`comment` 改存結束字串（`:166`）。<br>• 第八輪的 Z2、Z3、Z4（現況、2.4、Timeline）、Z2m、Z2r 全部 INVALID<br>• 新測試在 `test-evidence.py:571-582`<br>• 文件已同步：`review-evidence.md:51`、`CHANGELOG.md:31`、`rule-verification-status.md:327`<br>• `verify-artifact.py:10` 的 docstring 沒有改（NICE 3） | 完成 |
| NICE 1：M24 存活（表頭省略結尾 `\|`） | `test-evidence.py:660` 補了案例。reviewer 重跑 M24，2 個子測試失敗（BookkeepingTests 與 CurrentStateTests 各 1 個）。計畫寫「1 個失敗」，和上一輪一樣是照單一類別計算 | 完成 |
| NICE 2：驗證狀態少列已知限制 | `rule-verification-status.md:327` 改為「除 #5 登記的寫法與 CHANGELOG 已知限制（以 `\|` 開頭的行接分隔線、不在行首的粗體、縮排程式碼區塊）外」 | 完成 |
| NICE 3：第七輪案例數少算 W1 | `implementation-plan.md` S14 證據改為 12 個，並註明原本漏掉 W1 | 完成 |
| V7（v4.9.0 起就有） | 由 MUST FIX 1 的修法一起關掉；Z2t、Z3t、Z4t 判 INVALID。GitHub #5 留言（2026-11-11T07:52:26Z）補上 V7 與 TBD-7 的登記門檻 | 完成 |

### `unclosed()` 的判定

- **和參考實作比對**（`<tmp>/review9/fuzz_unclosed.py`）：
  - 另寫一個逐字元的參考實作，用含所有開頭與結束字串片段的字元集隨機產生 1～4 行的序列，未關閉的狀態跨行延續。
  - 3 個種子、共 30 萬組序列，0 筆不一致。
- **開頭與結束字串的組合**（`<tmp>/review9/adv/cases-r9.py`，每個案例都有 `## 現況` 與 Timeline 兩個版本，用 HEAD、`73202f8`、`46e09a5` 各跑一次，再用 marked 17.0.5 與 micromark 4.0.2 渲染）：

  | 案例 | 寫法 | HEAD | 判定是否正確 |
  |---|---|---|---|
  | A1 | 同一行先關後開（`<?x 甲 ?> 乙 <?y`），空行後刪 `?>` | INVALID | 正確（`73202f8` 判 OK） |
  | A2 | `<!X 甲 >` 接 `<![CDATA[`，空行後刪 `]]>` | INVALID | 正確 |
  | A3 | 結束字串在行中間，後面又開 `<!X` | INVALID | 正確 |
  | A4 | 巢狀 `<!-- <?x -->`，空行後刪 `?>` | OK | 正確：註解裡的 `<?` 不算，渲染看得到 |
  | A5 | 巢狀 `<?x <!-- ?>`，空行後刪 `-->` | OK | 正確，渲染看得到（`73202f8` 誤判 INVALID） |
  | A6 | 跨行：第二行關閉後又開 `<?x` | INVALID | 正確 |
  | A7～A9 | `<!-->`、`<!--->`、`<?>` 之後的正當修改 | INVALID | 多判（NICE 2） |
  | A10 | 小寫 `<![cdata[` | OK | 漏判（R9-1） |
  | A11 | `<!X` 的結束字串 `>` 是引用標記 | INVALID | 正確（渲染器也以那一行結束） |
  | A12 | Timeline 的 code span 寫 `` `<?php` ``，空行後的正當修改 | INVALID | 依 TBD-6 是已接受的代價，但會跨章節（SHOULD FIX 1） |

- **漏判的寫法**：除了大小寫（R9-1），檢查器在 code fence 狀態下不追蹤開頭字串（R9-2）。另外，清單項的容器會截斷 HTML 區塊（R9-3），這不屬於 `unclosed()` 本身。
- **正當記帳的誤判**：凍結章節的行內文字也會觸發（SHOULD FIX 1）；同一行就關閉的寫法也會觸發（NICE 2）。

### 前幾輪案例抽查

- 前八輪的對抗案例：
  - `<tmp>/review9/prev/`：review2～review7 的腳本共 206 次執行（含 `w1.py`），全部複製到 `<tmp>/review9/` 後執行，沒有寫入前幾輪的目錄。
  - `<tmp>/review9/r8/`：第八輪的 21 個案例。
- 判定比對：
  - 206 次的判定和第八輪用 `73202f8` 跑的結果逐筆相同。
  - 第八輪 21 個案例：Z2～Z4 系列、Z2m、Z2r、Z2c 判 INVALID；Z1、Z1c、Z1t、Z1o、Z1u、Z5、Z5t 判 OK，內容都看得到；Z1-2.4 與 Z5-2.4 判 INVALID。
- 從中挑出不同類別的 15 個，判定都沒有回退：

  | 類別 | 案例 | HEAD |
  |---|---|---|
  | 行內 `<!--` | review2 C1 | INVALID |
  | 跨行 `<details` 屬性 | review2 A1 | INVALID |
  | 搬動 `-->` | review2 F2 | INVALID |
  | 刪掉多行註解的 `-->` | review3 F1 | INVALID |
  | 同一行關閉後接標籤 | review3 G5 | INVALID |
  | 清單內 setext | review3 D1 | INVALID |
  | 參照定義的標籤跨行 | review3 J3 | INVALID |
  | fence 前插入 U+2028 | review4 U1a | INVALID |
  | `#<tab>` 標題 | review4 X4 | INVALID |
  | `\|` 開頭的行接 `===`（已知限制） | review4 N1 | OK（已登記） |
  | 連結 title 跨行 | review5 A1c | INVALID |
  | `[x]:` 參照定義 | review5 Y1 | INVALID |
  | 表頭 `\\|` 多算一欄 | review6 T1g | INVALID |
  | 真表格後刪空行（V3） | review6 T5 | OK（已登記） |
  | 只有一個 `\|` 的假表格 | review7 U1 | INVALID |

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 S15 的 fixture，兩份的 `## 現況` 都建在 `## 概述` 之後（第 7 行）：<br>• wf28b（`69b1e8c`→`0a1e301`）判 OK，變更含 Timeline、待確認事項、現況、現行 review<br>• wf31（`7b946af`→`19e4944`）判 OK，變更含現況、現行 review | 通過 |
| SCN-002 | S15 的紅燈可以重現：HEAD 的測試檔配 `73202f8` 的檢查器跑 232 項，6 個子測試失敗，名稱和 `s15-red.txt` 完全相同。HEAD 232 項全過 | 通過 |
| SCN-003 | 2.4 的案例全過；Z2-2.4～Z5-2.4 在 2.4 下都判 INVALID（`## 現況` 凍結），正確 | 通過 |
| SCN-004 | 見 SCN-001 | 通過 |
| SCN-005～008 | 本輪沒有修改，依 TBD-7 不重審 | 同 review-73202f8 |

其他證據查核：
- **判準先於重跑**：
  - `expected.md:149`「第八輪審查後重跑」和修正一起在 `486936a` 提交（15:52:26）。
  - 兩份 s15-rerun 證據都記錄 kit HEAD `486936a`。
  - fixture 的回合提交都比判準晚：wf28b `0a1e301` 15:53:52，wf31 `19e4944` 15:55:41。
  - 結果在 `c6eb117`（15:57:08）提交。
  - 結論：判準確實先於重跑。
- **記載一致性**：以下幾處都寫「各一輪、新檢查器 OK、沒有重審」，彼此一致，也和 fixture 的實際提交相符：
  - `implementation-plan.md:291-296`
  - `workflow-results/2026-11-10.md:104-106`
  - README Timeline 最後一列
- **計數**：
  - 測試從 228 項增為 232 項：新的測試方法被 4 個類別繼承（BookkeepingTests、CurrentStateTests、LegacyBookkeepingTests、NoContractBookkeepingTests）。
  - 紅燈 6 個：3 種新開頭字串 × 2 個 2.4 以上的類別；2.3 與無契約的類別本來就判 INVALID。
  - 「第八輪 21 個案例」的數目正確（`cases-r8.py` 16 個加 `cases-r8b.py` 5 個），寫法見 NICE 4。
- **既有記帳提交**（HEAD 檢查器），和 `implementation-plan.md:288` 的記載相符：
  - `d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306`、`b4e8708`、`853db0c`、`1b59d52` 判 OK。
  - `18f0e64` 照 TBD-6 判 INVALID。
- **報告保存**：`1b59d52` 保存的 `review-73202f8.md` 和 reviewer 交出的原稿逐字相同；同一個提交把 `**現行 review**` 改成 `review-73202f8.md`，並在 Timeline 補一列。
- **下游**：
  - `73202f8` 與 HEAD 的 `analyse()` 對 687 份 README 的結果 0 份不同。
  - 記帳章節裡沒有任何一行以 `<?`、`<!X`、`<![CDATA[` 開頭或在行中含有它們。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 第 3～5 型結束行在另一段 | Z2～Z4、Z2t～Z4t、Z2m、Z2r | INVALID | 全部 INVALID |
| 同一行多次開關、巢狀、跨行再開 | A1～A6、30 萬組隨機序列 | 依參考實作 | 全部相符；沒有測試保護（NICE 1） |
| 大小寫變體 | A10 | INVALID | OK（R9-1） |
| 假 fence 裡的開頭字串 | B1～B3 | INVALID | OK（R9-2） |
| 清單項截斷 HTML 區塊 | C1、C2 | INVALID | OK（R9-3） |
| 正當記帳被誤判 INVALID | D1～D5、A7～A9 | 只有文件寫明的情況會多重審 | 凍結章節的行內 `<?php` 等會跨章節凍結，文件沒寫（SHOULD FIX 1） |
| 前八輪攻擊寫法 | 206 次加 21 個案例 | 不回退 | 判定與 `73202f8` 相同 |
| 契約閘門 | 2.4、2.5 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - 以下幾處對四種開頭字串的描述一致：
    - `review-evidence.md:51`
    - `CHANGELOG.md:31`
    - `rule-verification-status.md:327`
  - 程式的 docstring 沒有同步（NICE 3）。
  - `docs/AGENTS.md:139` 沒有修改：撰寫規範本來就禁止記帳章節含 `<`，所以不必改，`expected.md:151` 也寫明「撰寫規範不變」。
  - 本輪沒有修改 `rules/` 與 `skills/*/SKILL.md`。
- **CHANGELOG**：
  - `:31` 和程式一致；`:51` 的 232 項正確。
  - `:62`「下游更新」沒有提到凍結章節的 `<?php` 也會觸發跨章節凍結（SHOULD FIX 1）。
- **核准範圍**：本輪 README 的變動只有：
  - `**現行 review**`
  - TBD-7 一列
  - Timeline 兩列
  
  Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：
  - 檢查器仍然唯讀。
  - 第八輪的 MUST FIX 已關閉。
  - 新找到的三種藏住寫法都需要違反撰寫規範的前提，下游 0 份，依 TBD-7 登記。
- **code-simplify**：
  - `unclosed()` 用一個迴圈同時處理「等結束字串」與「找下一個開頭字串」，約 13 行，取代原本的 `opens_comment()` 與呼叫端的切片運算，比原本清楚。
- **資訊衛生**：
  - 搜尋本輪新增的 1207 行，字樣包括 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`、`scratchpad`、`~/`，以及帳號名與信箱前綴。
    - 只命中 `review-73202f8.md` 裡列出搜尋字樣的那兩行。
    - 沒有本機實際路徑。
  - 用本機 115 個專案目錄的名稱另外搜尋，沒有命中，本 repo 自己的名稱除外。
  - 新增的 URL 只有本 repo 的 #5 與 `https://…` 佔位字。
  - s15-rerun 證據的路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`。
  - GitHub #5 的新留言（2026-11-11T07:52:26Z）沒有本機路徑或其他專案的名稱。
  - 3 個新提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。
  - 本報告提到的下游掃描只寫筆數，不寫專案名稱。
- **五項檢查**（reviewer 於 2026-11-11 在 `c6eb117` 自行執行，執行前後工作樹都是乾淨的）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：232 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。
- TBD-1～TBD-4、TBD-6、TBD-7 已解決；TBD-5 不影響本次交付，由 #4 追蹤。
- 依 TBD-7，`73202f8` 之前的範圍只抽查，沒有再做差異掃描、變異測試或全範圍的核准範圍比對。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs11/`）。
- 渲染限制：
  - 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 或 cmark-gfm 實際渲染。
  - R9-1～R9-3 在 GitHub 上的結果是推論。
- 隨機比對的字元集有限，不是窮舉。
- 下游掃描在 2026-11-11 執行，清單沿用 review7 的 README 路徑，去重後是 687 份。
- 腳本都在 `<tmp>/review9/`，都沒有進版控：
  - `adv/`：`cases-r9.py`、`cases-r9b.py`、`before.py`
  - `prev/`、`r8/`：前八輪案例重跑
  - `fuzz_unclosed.py`
  - `red/`：紅燈重現
  - `m24/`、`m24b/`：變異
  - `scan_r9.py`：下游掃描，只輸出筆數
- 已揭露、不構成缺失的限制：
  - wf32 不穩定；WF-28b、wf31 各只跑一輪。
  - 平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
PASS
