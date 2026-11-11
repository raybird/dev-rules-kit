# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state）。第十輪覆審。**本輪只審第九輪之後的差異 `c6eb117..b36de31`**（`1bffda1` 保存第九輪報告、`7f8d1e1` 修正、`b36de31` 重跑紀錄，14 個檔案，+1483／−10）。第九輪 review-c6eb117 判 PASS，使用者決定修正該輪的 SHOULD FIX 與 NICE 後再送審。更早的範圍不重審，只重跑第九輪的對抗案例與五項檢查。
- 工具呼叫上限：30 次（使用者要求）。實際用了 24 次（含寫本報告與回報）。固定清單 7 項都查完，沒有做清單以外的開放式找漏洞。
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：b36de31ba0183b130483ca2206ab499338bd17e3
- Reviewed patch-id：6ac6089d8f417b55f97803d06cceeacce82dd209（2026-11-11 以 `git diff 46e09a5 b36de31 | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-b36de31.md
- 審查日期：2026-11-11
- 審查依據：
  - README `## 待確認事項` TBD-2～TBD-7 的使用者決定。
    - TBD-6：記帳章節含 `<` 的行一律凍結，不模擬 CommonMark。
    - TBD-7：新找到的藏內容寫法，前提是被審查版本已違反撰寫規範（`docs/AGENTS.md:139`），而且下游 0 份符合時，不列 MUST FIX，登記到 #5。
    - TBD-5 由 GitHub #4 處理，不在本 issue 範圍。
  - 已登記在 #5 的 V3～V7、R9-1～R9-3，以及 CHANGELOG 4.10.0「已知限制」不重報。

## 問題與風險

### MUST FIX

無。`7f8d1e1` 的修改只放寬一處（`<!-->`、`<!--->`、`<?>` 視為同一行關閉），三種渲染規則下這三種寫法也都在同一行關閉，沒有新的藏住寫法（理由見「`CLOSER_FROM` 與錯誤訊息」）。

### SHOULD FIX

無。

### NICE TO HAVE

1. **錯誤訊息的兩個小瑕疵**（`skills/review/scripts/verify-artifact.py:246`、`:276-278`）：
   - `opener` 只在開頭行設定。未關閉區塊的續行先關閉、再開一個新的（A6t：`<!-- 甲`、下一行 `乙 --> 丙 <?x 丁`），訊息仍寫「「<!-- 甲」的 HTML 開頭未關閉，到 `?>` 為止」，指的是已經關閉的那一行。判定正確，只是指錯行。可以在續行的 `unclosed()` 回傳新的結束字串時，把 `opener` 改成該行。
   - `'open'` 的訊息對空行寫「「」」，其他種類寫「空行」（D1～D5 的「被審查版本為章節「設計邊界」的「」」）。
2. **CHANGELOG「下游更新」沒有提到凍結章節的未關閉開頭**（`CHANGELOG.md:58-63`）：
   - review-c6eb117 SHOULD FIX 1 建議在 `review-evidence.md:51` 與 CHANGELOG「下游更新」補一句。實作補在 `review-evidence.md:51` 與 CHANGELOG 4.10.0 的變更條目（`:31`），「下游更新」那一條只列記帳章節的寫法。
   - 下游只看「下游更新」時，不會知道設計邊界寫 `` `<?php` `` 也會讓後面的記帳判需重審。資訊已在同一個版本條目裡，所以列 NICE。
   - 另外，這條建議只寫在 review 階段載入的 `review-evidence.md`。撰寫 README 的 new-issue 階段看不到，但錯誤訊息已會指出原因，影響有限。
3. **S16 的證據沒有記完成判準的兩項**（`implementation-plan.md` S16 列與「S16 證據」）：
   - 判準寫「前九輪的對抗案例判定不回退；本 repo 歷來的記帳提交判定不變」。S15 證據有「對抗案例」「歷來記帳提交」兩列，S16 沒有。
   - reviewer 本輪已自行驗證這兩項（見下方「前幾輪案例重跑」「驗收與證據」），結果相符。
4. **`rule-verification-status.md:327` 沒有提到 S16 的 WF-28b 不通過**：
   - 該列仍寫「WF-28b、wf31 依新文字各重跑一輪，記帳提交都沒有 `<`、檢查器 OK」。S16 的 WF-28b 第一個記帳提交判 INVALID（原因是改了計畫，見檢查項 5）。
   - 最後一個記帳提交 `0e1235d` 判 OK，所以這句話本身沒有錯。可以補一句指向 `implementation-plan.md` 的 S16 證據。

### 登記到 #5 的寫法

本輪沒有新的。第九輪的 R9-1（A10）、R9-2（B1～B3）、R9-3（C1、C2）在 HEAD 判定不變（都判 OK），已在 #5 的 2026-11-11T08:15:46Z 留言登記。

### 需決策

無。實作照第九輪的建議只補文件與訊息，不縮小追蹤範圍（只在行首追蹤會和 TBD-6 的不模擬 CommonMark 衝突），不需要決策。

## 已查核維度

### 1. 上一輪發現的處理

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| SHOULD FIX 1：凍結章節 code span 裡未關閉的 `<?php`、`<!DOCTYPE html` 讓之後全部凍結，文件沒寫、訊息誤導 | • 文件：`review-evidence.md:51` 與 `CHANGELOG.md:31` 補上「這四種開頭在任何章節都追蹤…錯誤訊息會指出開頭所在的行；凍結章節要提到時寫成文字，或寫完整」<br>• 訊息：未關閉區塊裡的行改成 `'open'` 項目，記下開頭行與結束字串（`verify-artifact.py:195`、`:246`、`:276-278`）。D1～D5 的訊息都改成「「檔案以 `<?php` 開頭。」的 HTML 開頭未關閉，到 `?>` 為止的內容一律凍結，其後的標題不另分章節」<br>• 追蹤範圍不改（S16 證據寫明理由）<br>• CHANGELOG「下游更新」沒有補（NICE 2） | 完成 |
| NICE 1：「同一行關閉後又開新的」沒有測試擋住 | 新增 `test_reopened_block_across_blank_lines_stays_frozen`（`test-evidence.py:592-603`，`<!--` 與 `<?x` 兩個子測試），CurrentStateTests 繼承，也涵蓋 `## 現況`。reviewer 在 `<tmp>/review10/m/` 重做第九輪的變異（`pos, closer = end + len(closer), None` 改成 `return None`）：4 個子測試失敗，變異被擋住 | 完成 |
| NICE 2：`<!-->`、`<!--->`、`<?>` 被當成未關閉 | `CLOSER_FROM = {'<!--': 2, '<?': 1}`，結束字串改從開頭字串中間開始找（`verify-artifact.py:113`、`:129`）。A7～A9（現況、Timeline）由 INVALID 改為 OK，渲染看得到內容。新測試 `test_comment_and_processing_closed_on_same_line` | 完成 |
| NICE 3：docstring 沒有跟著改 | `verify-artifact.py:10-11` 改為「未在同一行關閉的註解、處理指令、宣告與 CDATA 到結束字串為止整段凍結（任何章節都追蹤）」 | 完成 |
| NICE 4：S15 的對抗案例描述不精確 | `implementation-plan.md` S15 證據改為「Z2～Z4 系列（含 Z2c、Z2m、Z2r）INVALID…Z1-2.4、Z5-2.4 在流程契約 2.4 下判 INVALID」，並註明由 review-c6eb117 指出。和第九輪重跑 21 個案例的結果相符 | 完成 |

### 2. `CLOSER_FROM` 與錯誤訊息

- **程式讀查**：
  - 放寬只有一處：`<!--` 從第 2 個字元、`<?` 從第 1 個字元開始找結束字串。只有 `<!-->`、`<!--->`、`<?>` 會因此在同一行關閉，其他寫法的判定不變。
  - 比對沒有變鬆：`'open'` 項目是 `(section, 'open', line, opener, comment)`，比原本的 `(section, 'html', line)` 多兩個欄位，兩版都用同一種，`compare_readme()` 用整個 tuple 比對（`:316-321`），只會更嚴。沒有其他地方依賴 `'html'` 種類（`grep` 只剩 `:244` 與 `describe()`）。
  - 渲染器：三種寫法在行首時，micromark（CommonMark 0.31）與 marked 都在同一行關閉；cmark-gfm 的 HTML 區塊結束條件從該行第一個非空白字元開始掃描，含開頭字串本身，所以也在同一行關閉（依原始碼推論，沒有在 GitHub 實測）。不在行首時不會開 HTML 區塊。
- **實測**（`<tmp>/review10/adv9/cases-r10.py`，拋棄式 Git repo，HEAD 檢查器，marked 與 micromark 渲染）：

  | 案例 | 寫法 | HEAD | 判定是否正確 |
  |---|---|---|---|
  | E1 | 設計邊界 `` `<!-->` ``，Timeline 補一列 | OK | 正確 |
  | E2 | 設計邊界 `` `<!--->` `` 與 `` `<?>` `` | OK | 正確 |
  | E3 | 設計邊界 `` `<!---->` `` 與 `` `<!-- -->` `` | OK | 正確 |
  | E4 | 同一行 `<!--a-->`、`<?b?>`、`<!X c>`、`<![CDATA[d]]>` 都關閉 | OK | 正確 |
  | E5 | 同一行 `<!--a-->` 之後 `<?b` 沒關 | INVALID，訊息指出這一行、結束字串 `?>` | 正確（文件寫明的代價） |
  | E6 | Timeline 同一行 `<!--->` 後開 `<?x`，空行後刪 `?>`（攻擊） | INVALID | 正確 |
  | E7 | 設計邊界 `<!--` 在下一行關閉，Timeline 補一列 | OK | 正確 |
  | E8 | `## 現況` 的 `<?>` 後同行開 `<!--`，空行後刪 `-->`（攻擊，兩個渲染器都藏住之後全部內容） | INVALID | 正確 |

- **訊息指出開頭所在的行**：D1～D5、E5、A1t、A2t、A3t、A11t、A12t 都指出開頭行的文字。A6t 指錯行（NICE 1）。訊息寫的是行的內容，不是行號；同一行文字重複出現時會不好找，影響小，不另列。

### 3. 第九輪案例重跑

`<tmp>/review9/adv/` 複製到 `<tmp>/review10/adv9/` 後執行（沒有寫入第九輪的目錄），HEAD 檢查器跑 `cases-r9.py`（36 個）與 `cases-r9b.py`（5 個）：

| 類別 | 案例 | HEAD | 和第九輪比較 |
|---|---|---|---|
| SHOULD FIX 1 的重現案例 | D1～D5 | INVALID，訊息改為指出開頭行 | 判定相同（照文件是已接受的代價），訊息改善 |
| 同一行先關後開、跨行再開 | A1、A1t、A3、A3t、A6、A6t | INVALID | 相同 |
| 巢狀 | A4、A4t、A5、A5t | OK，渲染看得到 | 相同 |
| 立即關閉 | A7～A9、A7t～A9t | OK，渲染看得到 | INVALID → OK（NICE 2 的修正） |
| `<!X` 結束字串是引用標記 | A11、A11t | INVALID | 相同 |
| code span 裡的 `<?php` | A12、A12t | INVALID | 相同 |
| 已登記 #5 | A10（R9-1）、B1～B3（R9-2）、C1、C2（R9-3） | OK | 相同 |

除了 A7～A9 照預期改變，其他判定都和第九輪相同。

### 4. 文件和程式的一致性

- `review-evidence.md:51` 與 `CHANGELOG.md:31`：新增的句子逐字相同，和程式一致（四種開頭任何章節都追蹤、訊息指出開頭行、三種立即關閉）。例句只舉 `<?` 與 `<!` 接字母，`<!--` 與 CDATA 由前一句「這四種開頭」涵蓋（D4 實測也會觸發），不另列。
- `CHANGELOG.md:51`：244 項。和 `s16-green.txt`（Ran 244、OK）及 reviewer 自行執行的結果相同。計數：新增 3 個測試方法，被 4 個類別繼承，232 + 12 = 244。
- 紅燈：`s16-red.txt` 244 項、8 個失敗，全部是新案例：`test_comment_and_processing_closed_on_same_line` 3 個子測試與 `test_unclosed_opener_in_frozen_section_named_in_message` 1 個，各在 BookkeepingTests 與 CurrentStateTests。和計畫的記載相符；`test_reopened…` 改前已通過，也和計畫的說明相符。
- `rule-verification-status.md:327`：「S16 8 個」與「九輪審查」正確；WF-28b 的記載見 NICE 4。
- `implementation-plan.md`：S15 列改 ✅ 並指向 S16；S16 列與證據和實際提交相符，缺兩項判準的證據列（NICE 3）。
- README Timeline 新增三列（第九輪 PASS、使用者決定送第十輪、S16 重跑），和計畫、`workflow-results/2026-11-10.md:108-113` 一致。`**現行 review**` 改為 `review-c6eb117.md`。
- docstring：已更新（見檢查項 1）。

### 5. 行為證據 `evidence/s16-rerun/`

- **判準先於重跑**：
  - `expected.md`「第九輪審查後重跑」和修正一起在 `7f8d1e1`（2026-11-11 16:22:07 +0800）提交。
  - 兩份證據都記錄 kit HEAD `7f8d1e1`。
  - WF-28b 的回合提交 `20ecc94` 在 16:24:18，之後是 `4b52522`、`53f61f3`、`0e1235d`（16:30:57）。結果在 `b36de31`（16:32:48）提交。
  - 結論：判準確實先於重跑。
- **WF-28b「不通過」的分析屬實**（reviewer 唯讀檢查 `<tmp>/runs12/rerun28/wf28b`）：
  - fixture 的 `5dc22e8:implementation-plan.md` 寫「4 個測試」，`5dc22e8:test_todo.py` 只有 3 個 `def test`。
  - agent 在 `20ecc94`（記錄需決策結論）一併把計畫改成 3 個。reviewer 用 HEAD 檢查器重跑 `5dc22e8`→`20ecc94`：「INVALID：被審查提交之後變更了 docs/issues/issue-2802/implementation-plan.md（M），不屬於記帳區段」，判定正確。
  - 之後完整重審：`4b52522` RETURN、`53f61f3` 補 CLI 層測試、`0e1235d` 保存 PASS 報告。reviewer 重跑 `53f61f3`→`0e1235d`：OK，變更含狀態、Timeline、現況、現行 review。
  - agent 的最終輸出照實說明舊 PASS 不能沿用的原因。
- **wf31**：reviewer 重跑 `b2bfb79`→`ceab087`（`<tmp>/runs12/cand/wf31`）：OK，變更含現況與現行 review，和證據相符。
- **對交付判定的影響：不影響。** 理由：
  - 判 INVALID 的原因是改了非記帳檔案，走的是檔案層的檢查，和 S16 修改的 HTML 開頭追蹤無關。檢查器與 agent 的後續動作都符合規則。
  - WF-28b 要證明的「2.5 下記帳提交沿用 PASS」：S15 的重跑已通過，本輪最後的記帳提交 `0e1235d` 也判 OK，沒有反證。
  - 「沒有重審」這條判準確實沒有達成，證據照實記成不通過，沒有為了通過而加跑，符合「不能豁免誠實回報」。
  - fixture 的誤記從前幾輪就存在。前幾輪的 WF-28b 判準不依賴測試數，所以不影響前幾輪的判定。fixture 的修正與重判已記在 #4（2026-11-11T08:33:13Z 留言）。

### 6. 公開 repo 衛生

- 搜尋 `c6eb117..b36de31` 新增的 1475 行，字樣包括 `/home/`、`/tmp/`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`、`~/`、帳號名與信箱網域：
  - `review-c6eb117.md` 列出搜尋字樣的那一行。
  - `s16-rerun/wf31.md` 的工具動作有一處 `ls ~/.claude/skills/review/scripts`（fixture 裡的 agent 下的命令）。這是通用的家目錄相對路徑，不含帳號或本機專屬資訊，不列缺失。
  - 沒有本機實際的絕對路徑。暫存路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`、`<scratchpad>`、`<tmp>`。
- 用本機一個專案目錄下的 60 個專案名稱搜尋新增內容，沒有命中。
- 新增的 URL 只有本 repo 的 #4、#5 與 `https://…` 佔位字。
- GitHub 新留言：#4 的 2026-11-11T08:33:13Z、#5 的 2026-11-11T08:15:46Z，用同一組字樣與專案名稱搜尋都沒有命中；#5 的下游筆數只寫筆數。
- 3 個新提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。

### 7. 五項檢查

reviewer 於 2026-11-11 在 `b36de31` 自行執行，執行前後工作樹都是乾淨的：

- `check-kit.py`：OK
- `check-links.py`：OK
- `bash -n scripts/install.sh`：rc 0
- `test-install.py`：14 項 OK
- `test-evidence.py`：244 項 OK

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001、SCN-004 | wf31 `ceab087` 與 WF-28b `0e1235d` 的記帳提交以 HEAD 檢查器判 OK，`## 現況` 的變更被列為記帳 | 通過 |
| SCN-002 | S16 紅燈 8 個、綠燈 244 項全過；reviewer 自行執行 244 項 OK | 通過 |
| SCN-003 | 本輪沒有修改契約閘門；2.4 類別的測試全過 | 同 review-c6eb117 |
| SCN-005～008 | 本輪沒有修改，依 TBD-7 不重審 | 同 review-73202f8 |

- 歷來記帳提交（HEAD 檢查器）：`d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306`、`b4e8708`、`853db0c`、`1b59d52` 與本輪的 `1bffda1` 判 OK；`18f0e64` 照 TBD-6 判 INVALID。判定不變。
- 報告保存：`1bffda1` 新增 `review-c6eb117.md`，同一提交把 `**現行 review**` 改為該報告，並在 Timeline 補一列。

### 需求、架構、安全、品質

- 檢查器仍然唯讀；本輪唯一的放寬已確認不會藏住內容。
- `rules/`、`skills/*/SKILL.md`、`docs/AGENTS.md` 本輪沒有修改；`expected.md` 寫明撰寫規範不變。
- code-simplify：`CLOSER_FROM` 一行查表、`opener` 一個變數，改動小，和既有寫法一致。

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4、TBD-6、TBD-7 已解決；TBD-5 由 #4 追蹤。
- 依使用者要求只審 `c6eb117..b36de31`。更早的範圍只重跑第九輪的 41 個案例與歷來記帳提交，沒有重跑第二～八輪的 206 次案例、隨機比對與下游 README 掃描。
- 工具呼叫上限 30 次，清單 7 項都查完，沒有因上限而略過的項目。
- 沒有實跑宿主 agent；行為面只核對已提交的證據，並唯讀檢查同一 session 暫存區的 fixture（`runs12/`）。
- 渲染以 marked 與 micromark 為準，沒有在 GitHub 或 cmark-gfm 實際渲染；cmark-gfm 的結論是依原始碼推論。
- 專案名稱只用一個專案目錄下的 60 個名稱，比第九輪的 115 個少。
- 腳本都在 `<tmp>/review10/`，都沒有進版控：
  - `adv9/`：第九輪案例的複本、`cases-r10.py`、`out-b36.txt`、`out-b36b.txt`、`out-r10.txt`
  - `m/`：變異測試
  - `added.txt`、`names.txt`、`gh4.txt`、`gh5.txt`：衛生搜尋

## 流程判定
PASS
