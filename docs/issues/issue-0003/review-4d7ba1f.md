# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，28 個提交、91 個檔案）；第七輪覆審，重點是上一輪 [review-20d0847](review-20d0847.md) 之後的修正 `b4e8708..4d7ba1f`（主要是 `eea9ac8`）
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：4d7ba1f34a716c6651825d3d0a4effea1fd6e070
- Reviewed patch-id：3a9bc87733386ed680dfaf0c5e92d363006df98f（2026-11-11 以 `git diff 46e09a5 4d7ba1f | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-4d7ba1f.md
- 審查日期：2026-11-11
- 審查依據：
  - README `## 待確認事項` TBD-2～TBD-6 的使用者決定。TBD-6 決定記帳章節含 `<` 的行一律凍結，code span 裡的標籤名與佔位字因此判需重審，這是已接受的代價，本報告不列為缺陷。TBD-5 由 GitHub #4 處理，不在本 issue 範圍。
  - README Timeline 2026-11-11 的使用者決定：v4.9.0 起就有的同類缺口另開 issue，不阻擋本 issue。所以本報告把「本 issue 新引入的缺陷」與「v4.9.0 起就有的同類缺口」分開列。判定方式：同一個案例也用 `46e09a5` 的檢查器（v4.9.0）跑一次，判 OK 的就是 v4.9.0 起就有。
  - CHANGELOG 4.10.0「已知限制」已登記的項目（V3、V4、假表格接 `---`）不重報，除非影響比登記的大。

## 問題與風險

### MUST FIX

1. **表頭只有一個 `|` 時，檢查器算成 1 欄、當作表格；兩個渲染器都不當表格。`## 現況` 的假表格仍能藏住後面所有章節，判 OK**
   - 位置：`skills/review/scripts/verify-artifact.py:124-135`（`cells()`、`starts_table()`）。
     - `cells('|')`：去掉開頭的 `|` 後 body 是空字串，`''.split('|')` 得 1 欄。分隔列 `|-|` 也是 1 欄，欄數相同，所以判為表格，每列各自 flush。
     - marked 與 micromark 都不把 `|` 加 `|-|` 當表格，整段渲染成段落。段落裡的行內語法可以跨行，就是上一輪 MUST FIX 1 的同一種形態。
     - 這是上一輪 T2n／T2s 的同型寫法，只是假表頭換成單獨一個 `|`。上一輪的建議與本輪修正都只處理了頭尾多一個 `|` 與 `\|` 兩種情況。
   - 實測方式：
     - 在 `<tmp>` 建拋棄式 repo（沿用前幾輪的 `probe4.py`）。PASS 之後的提交新增報告並改寫 README。
     - 渲染用 marked 17.0.5（GFM），以及 micromark 4.0.2 加 micromark-extension-gfm。再用 parse5 7.3.0 找標記文字的位置（沿用 `render.mjs`）。
     - 同一組案例也用 `20d0847`（S12）與 `46e09a5` 的檢查器各跑一次。

     | 案例 | 審查版本 | 記帳提交（只動記帳章節，都不含 `<`） | HEAD | `46e09a5`（v4.9.0） | 渲染結果（兩個渲染器相同） |
     |---|---|---|---|---|---|
     | U1 | `## 現況` 的外部狀態表之後空一行，接一段 ``**備註**：用 `<details>` 收合。``（凍結） | 在凍結段落前新增 `\|`、`\|-\|`、``\| 補記 ` \|`` 三行，並刪掉它與凍結段落之間的空行 | OK | INVALID（2.4 以前 `## 現況` 是凍結章節） | 落單反引號和凍結段落的第一個反引號配對，`<details>` 跑出 code span。之後的設計邊界、Gherkin、metadata 全部收進關閉的 details |
     | U1b | 同 U1，但凍結段落是一般文字（非粗體） | 同 U1 | OK | INVALID | 同 U1 |
     | U1c | 同 U1 | 分隔列改成 `\| - \|` | OK | INVALID | 同 U1 |
     | U1-2.4 | 同 U1，流程契約 2.4 | 同 U1 | INVALID | INVALID | 同 U1（2.4 下 `## 現況` 凍結，判定正確） |
     | 對照 U1d | 同 U1 | 假表格與凍結段落之間保留空行 | OK | INVALID | 全部看得到 |

   - 只在 marked 成立的變形（同一個根因，micromark 照樣渲染成表格、內容看得到）：
     - U4：分隔列含 tab（`| a |` 加 `|<tab>-|`）。檢查器的 `DELIMITER_ROW` 接受 tab，marked 的分隔列只接受空格。
     - U6：表頭含 U+2028（`| a<U+2028>b |`）。marked 的表頭比對在 U+2028 停住。
     - HEAD 都判 OK，marked 藏住後面全部章節，`46e09a5` 都判 INVALID。
   - 差異掃描：
     - 隨機產生以 `|` 開頭的表頭與分隔列，挑出 HEAD 的 `starts_table()` 判為表格的組合，再交給兩個渲染器。腳本在 `<tmp>/review7/fuzz/`。
     - 第一組字元集（`|`、空白、反斜線、反引號、`:`、`-`、`\|` 等）：13863 組裡，兩個渲染器不當表格的只有表頭 `|` 一種。
     - 第二組字元集多加 tab、NBSP、U+3000、U+2028、U+200B 與全形字：micromark 仍只有表頭 `|` 不一致；marked 另外在分隔列含 tab、表頭含 JS 視為空白的字元或 U+2028 時不當表格。
     - 真表格之後以 `|` 開頭的行：7174 種寫法，兩個渲染器都照樣當成同一張表的列，和檢查器一致。
   - 影響：
     - 這是本 issue 新引入的缺陷。2.5 讓 `## 現況` 成為記帳章節，`46e09a5` 對 U1、U1b、U1c 判 INVALID，HEAD 判 OK。`20d0847` 也判 OK，所以是上一輪 MUST FIX 1 沒有修完整。
     - 藏住的是 README 剩下的全部內容：設計邊界、Gherkin 驗收劇本、核准紀錄與 metadata。PASS 照樣沿用。
     - 前提和上一輪的 T2s 相同：審查版本的 `## 現況` 有一段前面空一行、含 HTML 標籤 code span 的非表格段落。
       - 這違反 `docs/AGENTS.md:139` 的撰寫規範（`## 現況` 的內容不含 `<`）。
       - 本機 680 份不重複的 issue README 中，3 份有 `## 現況`，0 份符合前提。
     - 同樣的寫法在 Timeline、待確認事項、Gate 豁免紀錄也成立，但 v4.9.0 就判 OK，列在「v4.9.0 起就有的同類缺口」V5。
   - 建議：
     - `cells()` 在兩種情況回傳 None（照段落處理，凍結得較多）：
       - 該行含空格以外的空白字元（`[^\S ]`，再加 U+FEFF）；
       - 去掉頭尾的 `|` 後只剩空格。
     - reviewer 在 `<tmp>/review7/verify-fix.py` 試改約 3 行，結果：
       - 差異掃描在兩組字元集、四個亂數種子下都是 0 筆不一致。
       - U1～U6 全部判 INVALID，U1d 仍判 OK。
       - `test-evidence.py` 224 項全過。
       - 前六輪 195 次案例執行的判定都和 HEAD 相同。
       - 本 repo 歷來的記帳提交判定不變。S13 兩個重跑 fixture 的記帳提交仍判 OK。
       - 下游 2614 張表格（issue README 所有章節）的表格判定 0 張改變。
     - 補上表頭 `|` 與分隔列含 tab 的負向案例。
     - `review-evidence.md:51`、`CHANGELOG.md:35` 的表格條件要跟著補。GitHub #5 正文寫「V1（假表格）已在 #3 一併修正」，也要更新。

### SHOULD FIX

1. **`rule-verification-status.md:327` 寫「六輪審查留下的對抗案例中攻擊寫法全部 INVALID」，誇大了結果**
   - 第六輪的 T5（V3）、T6（V4）是攻擊寫法，HEAD 都判 OK。
   - `implementation-plan.md:246` 有寫「除登記為 #5 的 V3、V4 外」，驗證狀態表少了這個例外。
   - 同一格還並列「本機 683 份」與 2026-11-11 重新掃描 680 份才得到的「37 份 50 段」，兩個數字出自不同掃描。
   - 建議：補上「除登記為 #5 的 V3、V4 外」。MUST FIX 1 修好前，也不能寫成全部 INVALID。

2. **下游筆數仍然無法照寫明的分類方式重現（上一輪 NICE 3 沒有完成）**
   - 位置：`CHANGELOG.md:62`、`implementation-plan.md:248`、`rule-verification-status.md:327`。
   - 記載：「以分隔線開頭的檔尾 metadata 段落 381 行；其餘 37 份 50 段 423 行；表頭與分隔列一併凍結的表格有 31 份 40 張」。
   - reviewer 用 HEAD 的 `analyse()` 重掃同一份 680 份清單（2026-11-11）：
     - 因段落整段凍結而新凍結的行，總數 804 行，和 381＋423 相符。
     - 照「段落第一行是 `---`」分類：metadata 362 段 398 行；其餘 27 份 39 段 406 行。
     - 另外試了五種分類：段落含 `---`、段落結尾、是否為檔案最後一段、限 Timeline、含 `**建立日期**` 或粗體欄位。都得不到 37 份 50 段 423 行。
     - 表格：31 份相符，但不同的表格是 32 張。40 是凍結列的數目，每一列各記一次表頭。
   - 建議：照實際定義更正筆數，或把掃描用的分類條件寫清楚，讓人能重現。

### NICE TO HAVE

1. **變異測試有 1 個存活**（7 個變異，6 個被抓到；腳本在 `<tmp>/review7/mut/`）：
   - M19：凍結時只記表頭、不記分隔列，224 項仍全過。
     - 沒有安全上的差別：分隔列減欄會讓欄數不符，照段落處理而判 INVALID。只改對齊冒號則只影響版面。
     - 可以補一個「表格含凍結列時改分隔列對齊」的案例。
   - 被抓到的 6 個是 M11（拿掉欄數比對）、M13（表格可從段落中間開始）、M16（不凍結表頭）、M17（不處理 `\|`）、M18（改回 `strip('|')`）、M20（表頭凍結條件永遠不成立）。
   - `implementation-plan.md:245` 寫 M11 有 4 個、M13 有 1 個失敗，是以單一測試類別計算。reviewer 的同名變異在 BookkeepingTests 與 CurrentStateTests 合計 8 個與 2 個失敗，兩種算法一致。
2. **`docs/AGENTS.md:139` 沒有提到改表頭會判需重審**：
   - 這一行只寫「空行或標題之後開始的表格逐列判定，可以直接補列」。
   - 表格含 `<` 的列時，表頭與分隔列一併凍結，改表頭會判需重審。這條只寫在 `review-evidence.md:51`。
   - 下游 31 份共 32 張表格屬於這種情況。審查後改表頭的機會很少，所以不急。
3. **`implementation-plan.md:246` 寫「第六輪 17 個案例」**：reviewer 在 review6 的兩支腳本裡數到 16 個（`cases-r6.py` 14 個、`cases-r6b.py` 2 個）。

### v4.9.0 起就有的同類缺口

以下案例 `46e09a5` 的檢查器也判 OK。依使用者決定另開 issue 處理，不阻擋本 issue。兩項的影響都比 #5 登記的大，所以列出來。腳本在 `<tmp>/review7/adv/`（`cases-r7.py`、`cases-r7b.py`、`cases-r7c.py`、`w1.py`）。

| 編號 | 寫法 | 前提 | 渲染結果 | 下游分布（本機 680 份） |
|---|---|---|---|---|
| V5（V1 的殘留） | 在 Timeline、待確認事項或 Gate 豁免紀錄，用 `\|` 加 `\|-\|` 開一張假表格接在凍結段落前，並刪掉空行（U2、U3）。只在 marked 成立的還有分隔列含 tab、表頭含 U+2028 兩種 | 這三節有一段前面空一行、含 HTML 標籤 code span 的非表格段落 | 之後的內容收進關閉的 details；在 Timeline 時藏住 metadata | 2 份 3 段（和上一輪 V1 的非表格段落數相同）。#5 正文寫 V1 已修正，實際仍有這個殘留 |
| V6（V4 的擴大） | 記帳欄位的值在任何章節都不列入比對：<br>• W2：凍結章節（例如設計邊界）段落裡的 `**狀態**` 值改成以落單反引號結尾<br>• W1：`**核准 commit**` 由 `待提交` 回填成 `` `SHA ``（只有開頭一個反引號）。`SHA` 正則 `` ^`?…`?$ `` 允許不成對的反引號（`verify-artifact.py:40`） | 欄位和後面含 HTML 標籤 code span 的行在同一段落。W1 另外要求核准 commit 仍是 `待提交` | W2 藏住 Gherkin 與 metadata；W1 藏住核准來源與之後所有內容 | `**狀態**`：0 份。`**核准 commit**`：3 份清單項目接續行有這種形狀，但都已回填，0 份還是 `待提交`。範本的核准欄位是清單項目，每項是獨立段落，照範本寫不受影響 |

- 修法方向：
  - V5 由 MUST FIX 1 的修法一併關掉（reviewer 試改後確認過）。
  - V6：記帳欄位的值不能含反引號、`[`、`!` 這類會跨行配對的字元；`SHA` 正則要求反引號成對。可以和 #5 的 V4 一起處理。
- 已登記、不重報：
  - V3（T5，真表格後刪空行）與 V4（T6，metadata 的 `**狀態**`）已在 #5 與 `CHANGELOG.md:36`。
  - 假表格接 `---`（T3）是已知限制。

### 需決策

無。MUST FIX 1 的修法是多凍結，符合 TBD-3、TBD-6 的方向。V5、V6 依使用者既有決定歸入另開的 issue（建議補進 #5）。

## 已查核維度

### 上一輪發現的處理

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：欄數算法和 GFM 不同 | `cells()` 改成頭尾各去一個 `\|`，表頭含 `\|` 時回傳 None（`verify-artifact.py:124-135`）。T1、T1t、T1h、T1g、T1s、T2、T2n、T2s、T3 改判 INVALID（`20d0847` 都判 OK）。新增測試：`test-evidence.py:624-659` | 原案例都已處理；同一類的表頭 `\|` 仍有漏洞（MUST FIX 1） |
| SHOULD FIX 1：縮減欄數（T4） | 表格含凍結列時，把表頭與分隔列記成凍結項目（`:208-211`、`:234-238`、`describe()` `:251-252`）。T4 改判 INVALID | 完成 |
| NICE 1：存活變異 M11、M13 | `test-evidence.py:639-659` 補上表頭含 `\|`、分隔列欄數不符、表格緊接段落三個案例。reviewer 重跑這兩個變異，都被抓到 | 完成 |
| NICE 2：`docs/AGENTS.md` 的表格條件 | `:139` 改為「空行或標題之後開始的表格逐列判定，可以直接補列」 | 完成；表頭凍結沒寫進去（NICE 2） |
| NICE 3：下游筆數的分類方式 | 補上「以分隔線開頭的檔尾 metadata 段落」，筆數也重算了 | 照寫明的分類仍無法重現（SHOULD FIX 2） |
| V1～V4 | V1、V2 由上兩項處理。V3、V4 登記在 #5 與 `CHANGELOG.md:36` | V2 完成；V1 有殘留（V5）；V3、V4 登記正確 |

前六輪的案例全部重跑（`<tmp>/review7/prev/`；review2～review6 的腳本共 195 次執行）：
- HEAD 與 `20d0847` 只差在第六輪的 10 個案例：T1、T1t、T1h、T1g、T1s、T2、T2n、T2s、T3、T4，都改判 INVALID。
- 判 OK 的 28 次是：
  - 前五輪：C0、FP7、FP8（各兩次），以及 K6、N1、N1b、N1c、N2～N5、N4b、N4c、X1、X7、A2c、F4～F7。
  - 第六輪：對照組 T0、T2c、T6c，以及已登記的 T5（V3）、T6（V4）。
- 這和 `implementation-plan.md:246` 的記載相符（案例數見 NICE 3）。

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 S13 的 fixture，兩份的 `## 現況` 都建在 `## 概述` 之後（第 7 行）：<br>• wf28b（`33786a1`→`d5a15d1`）判 OK，變更含 Timeline、待確認事項、現況、現行 review<br>• wf31（`f7ef757`→`9a2b6fd`）判 OK，變更含現況、現行 review<br>兩份用 MUST FIX 1 的試改版也判 OK | 通過 |
| SCN-002 | S13 的紅燈可以重現：HEAD 的測試檔配 `20d0847` 的檢查器跑 224 項，10 個子測試失敗，失敗名稱和 `s13-red.txt` 完全相同。HEAD 224 項全過 | 有缺口：MUST FIX 1 |
| SCN-003 | 2.4 的案例全過。U1-2.4、T1s-2.4 在 2.4 下都判 INVALID（`## 現況` 凍結），正確 | 通過 |
| SCN-004 | 見 SCN-001 | 通過 |
| SCN-005～008 | 本輪沒有修改，沿用前幾輪的判定 | 同 review-20d0847 |

其他證據查核：
- **判準先於重跑**：
  - `expected.md:141`「第六輪審查後重跑」和修正一起在 `eea9ac8`（14:34:23）提交。
  - 兩份 s13-rerun 證據都記錄 kit HEAD `eea9ac8`。
  - fixture 的回合提交都比判準晚：wf28b `d5a15d1` 14:36:06，wf31 `9a2b6fd` 14:37:37。結果在 `4d7ba1f`（14:38:50）提交。
  - 結論：判準確實先於重跑。
- **記載一致性**：
  - 以下幾處都寫「各一輪、新檢查器 OK、沒有重審」，彼此一致，和 fixture 實際內容相符：
    - `implementation-plan.md` S13 列（`:38`）與 S13 證據（`:238-255`）
    - `workflow-results/2026-11-10.md:96-98`
    - README Timeline 最後一列
  - 誇大或無法重現的地方見 SHOULD FIX 1、2 與 NICE 3。
  - wf28b 的 agent 另外指出 fixture 的測試數寫錯（4 對 3），屬於 fixture 內容，不影響這次的判準。
- **紅綠燈與變異**：紅燈 10 個失敗可以重現。M11、M13 的失敗數照單一類別計算後相符（NICE 1）。
- **既有記帳提交**（HEAD 檢查器），和 `implementation-plan.md:247` 的記載相符：
  - `d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306`、`b4e8708` 判 OK。
  - `18f0e64` 判 INVALID：TBD-6 的凍結列。錯誤訊息現在先指到 Timeline 的表頭項目，判定不變。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 假表格：表頭頭尾多 `\|`、表頭含 `\|` | T1、T1t、T1g、T2n、T2s | INVALID | 全部 INVALID |
| 假表格：表頭只有 `\|` | U1～U1c（`## 現況`）、U2、U3 | INVALID | OK，藏住後面內容（MUST FIX 1、V5） |
| 假表格：分隔列含 tab、表頭含 U+2028 | U4、U6 | INVALID | OK；marked 藏住，micromark 看得到（MUST FIX 1） |
| 表格欄數縮減、表頭改寫 | T4、T1h | INVALID | INVALID |
| 真表格之後以 `\|` 開頭的行 | 差異掃描 7174 種寫法 | 和渲染器一致 | 一致 |
| 凍結列前後補列（正當） | T0、`test-evidence.py:611-622` | OK | OK |
| 表格緊接在段落後（正當） | `test-evidence.py:639-659` 最後一案 | 照段落處理，有寫在文件 | 正確；`review-evidence.md:51`、`CHANGELOG.md:35` 有寫 |
| 正當記帳被誤判 INVALID | 下游 2614 張表格：S12 與 S13 的表格判定 0 張不同；凍結項目除了新增的表頭項目以外 0 份不同 | 只在改表頭時多重審 | 新增的重審只在 31 份 32 張含凍結列的表格改表頭時發生（NICE 2）。沒有找到文件沒寫的其他誤判 |
| 記帳欄位的值 | W1、W2、T6 | INVALID | OK（V4、V6，v4.9.0 起就有） |
| 真表格後刪空行 | T5、T2c | 依文件 | OK（V3，已登記） |
| 契約閘門 | 2.4、2.5 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - 以下幾處對表格條件、表頭凍結與段落凍結的描述彼此一致：
    - `review-evidence.md:51`
    - `CHANGELOG.md:35-36`
    - `docs/AGENTS.md:139`
    - `verify-artifact.py` 的 docstring
  - 落差只有 NICE 2，以及 MUST FIX 1 修好後要補的條件。
  - 本輪沒有修改 `rules/` 與 `skills/*/SKILL.md`。check-kit 的雙語章節檢查通過。
- **CHANGELOG 的下游影響與已知限制**：
  - `:36` 登記 V3、V4 的寫法正確。
  - `:35`「欄數照 GFM 計算」在 MUST FIX 1 修好前不完全成立。
  - `:62` 的筆數見 SHOULD FIX 2。
  - V5、V6 還沒登記。
- **核准範圍**：
  - 用 HEAD 的 `analyse()` 比對 `fe43877` 與 `4d7ba1f` 的 README：記帳章節以外的 135 個凍結項目完全相同。
  - 差異只有：新增的 `## 現況`、`**核准 commit**`（待提交 → `fe43877`）、`**狀態**`，以及 Timeline 新增的列和它的表頭項目。
  - Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：
  - 檢查器仍然唯讀。
  - 上一輪的 T1～T4 已經關掉。
  - 本 issue 新引入、需要前提的路徑還有一條：`## 現況` 用 `|` 表頭開假表格（MUST FIX 1）。
- **code-simplify**：
  - S13 只多了一個 `head` 狀態與一種 `table` 項目，結構清楚。
  - 每一列凍結列各記一次表頭，比對時會重複，但不影響正確性。
  - MUST FIX 1 的修法在 `cells()` 內就能完成，不需要新結構。
- **資訊衛生**：
  - 本輪新增 1003 行、全範圍新增 11511 行。搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`、`scratchpad`、`~/`，以及帳號名與信箱前綴。
    - 本輪新增內容沒有任何命中。
    - 全範圍只命中前幾輪報告裡列出這些搜尋字樣的行，沒有實際路徑。
  - 用本機 115 個專案目錄的名稱另外搜尋一次。只命中一般英文單字 `notes`（fixture 證據裡的檔名），沒有其他專案的名稱。
  - 本輪新增的 URL 只有本 repo 的 #5 與 `https://…` 佔位字。
  - s13-rerun 證據的路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`。
  - 28 個提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。
  - 本報告提到的下游掃描只寫筆數，不寫專案名稱。
- **五項檢查**（reviewer 於 2026-11-11 在 `4d7ba1f` 自行執行，工作樹乾淨）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：224 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4、TBD-6 已解決，TBD-5 不影響本次交付，由 #4 追蹤。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs9/`）。
- 渲染限制：
  - 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 或 cmark-gfm 實際渲染。
  - U1 在 GitHub 上的結果是推論：micromark 依 GFM 規格實作，兩個渲染器都不把 `|` 當表頭。
  - U4、U6 只在 marked 成立。
- 差異掃描是以有限字元集隨機產生，不是窮舉。
- 下游掃描在 2026-11-11 執行：
  - 前幾輪的路徑清單現存的 README 去重後是 680 份。
  - 重新搜尋得到 686 份，各項筆數相同。
- 對抗、變異、差異掃描與修正試改的腳本都在 `<tmp>/review7/`，都沒有進版控：
  - `adv/`（`cases-r7*.py`、`w1.py`）
  - `prev/`（前六輪案例重跑；`out-head.txt`、`out-20d0847.txt`、`out-main.txt`、`out-fix.txt`）
  - `fuzz/`（差異掃描）
  - `mut/`（變異與紅燈重現）
  - `verify-fix.py`、`fixcheck/`（MUST FIX 1 的試改）
  - `scan7*.py`、`scan_field.py`（下游掃描，只輸出筆數）
- 已揭露、不構成缺失的限制：wf32 不穩定；WF-28b、wf31 各只跑一輪；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
