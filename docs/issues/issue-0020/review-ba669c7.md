# 審查報告
- 範圍：決策審查（issue #20「不修復」決策；沒有程式或規則變更，本報告不代表任何程式變更通過）
- Reviewed BASE SHA：e5204a4ad56cf88028801d3e61595f0f8077ee0e
- Reviewed HEAD SHA：ba669c7f89430d17024f7a0c627bb1b31fa6959d
- Reviewed patch-id：4fe28ba202d57a99979eb9ce7ff7ac6b35eef110
- 獨立 reviewer：Claude Code general-purpose subagent（未參與 README 撰寫）

## 問題與風險

- SHOULD FIX：README 第 28 行「issue 目錄外有 34 個 Markdown 檔以相對連結指向報告」的描述與計法不一致。原作者的命令只排除報告檔本身（`docs/issues/issue-N/review-*.md`），沒有排除 issue 目錄。重跑後 34 個檔案裡 29 個在 `docs/issues/issue-*/` 內（README、implementation-plan、evidence、fixtures），在 issue 目錄外的只有 5 個（`docs/workflow-results/` 3 個、`docs/reviews/` 2 個）。這 34 個也包含指向 evidence 內回歸產物或 `docs/reviews/` 的連結，不全是指向 issue 報告。實際刪掉 63 份報告後，check-links 回報 109 個斷連結，分布在 18 個檔案，其中 issue 目錄外的只有 `docs/workflow-results/` 的 3 個。「移除後 check-links 會失敗」成立，結論不受影響，只是「issue 目錄外 34 個」高估了跨目錄依賴。建議改成「報告以外有 18 個 Markdown 檔以相對連結指向報告（其中 3 個在 issue 目錄外），移除後 check-links 會失敗」，或寫成「報告檔以外有 34 個檔案含指向 review 檔的連結」並附上計法。另外，原提案「要設計的點 3」已把 check-links 失敗列為要處理的設計點，所以這一項比較適合寫成移出主幹的代價，不宜當成反駁提案的證據。
- SHOULD FIX：調查摘要漏掉三項不利或中性的證據（第 12～13、22 行），殘餘影響也寫得太窄。
  1. 第 13 行寫「調查中提到的成本只有一項」，但有一個下游專案回報 rebase 改 SHA 造成額外工夫：報告檔名與 Reviewed SHA 指向主幹上不存在的 commit。這和報告長期留在主幹有關，README 沒寫，也沒說明為何不算。
  2. 有一個下游專案回報舊報告寫的數值已經過時（報告寫 30 天，實際已改為 90 天），沒有因此做錯的紀錄。這正好是重新評估條件（第 14 行）要觀察的「舊報告留在工作樹造成錯誤結論」差一點就發生的情況，應揭露為差點出事的案例或潛在風險，讓之後重新評估的人知道已經有過一次。第 22 行「6／6 沒有因報告位置造成的紀錄」字面上仍成立。
  3. 第 12 行說唯一一起誤引用「與報告放在哪裡無關」，這說法只對了一半。起因確實是引用時沒分辨「推論，讀程式」與實測，報告改從 Git 歷史讀取也會發生同樣的錯。但如果報告不在工作樹，後續審查大概不會讀到它，這次誤引用也不會出現。比較持平的寫法是：「起因是引用時沒分辨推論與實測；報告不在工作樹時這次誤引用不會發生，但同一批報告的正確引用也會一併失去，且已由下一輪審查更正」。

  這三項都沒有達到「下游實際因報告位置做出錯誤結論」的門檻，不推翻不修復判定，所以列 SHOULD FIX，不列 MUST FIX。
- NICE TO HAVE：第 7 行「提案的前提不成立」說得太滿。提案的前提是「合併後幾乎沒有人回頭看」。調查顯示六個專案都有回頭引用，但有一個專案約 55 份中有 50 份沒被引用。比較精確的說法是：大部分報告合併後沒人讀，但事先無法知道哪一份會被引用，而被引用的那幾份是交接、地雷與程式註解的證據來源。這樣理由反而更完整。
- NICE TO HAVE：第 25～26 行的合併方式摘要有兩處和回覆不完全一致。(a)「四個專案不開 PR／MR」：其中一個專案是「主要 --ff-only，少數平台 squash」，寫成「四個專案主要不開 PR／MR」較精確。(b)「多數合併後不刪遠端分支」：回覆中明確不刪的只有兩個專案；一個遠端沒有 issue 分支，一個 squash 後原始分支已不存在，一個遠端多數 issue 分支已刪，一個只在本機合併。「多數不刪」這說法站不住，而且實際情況（報告常常只剩主幹一份）比 README 寫的更支持本決策。
- NICE TO HAVE：第 30 行「下游已用 document-types.md『地雷紀錄』把需要常駐的內容升級出來」概括過度。有一個專案的遺留項目只寫在報告，沒有升級成待確認事項或新 issue。建議改為「部分下游已用……」，維持本 issue 不另行處理的結論。
- NICE TO HAVE（`需決策`）：本 kit 根目錄 AGENTS.md「範圍」的「刻意不管」表可以加一列：「審查報告合併後移出主幹 ｜ 報告留在主幹（issue #20） ｜ 下游出現一次舊報告留在工作樹而造成錯誤結論或搜尋干擾」。這樣日後有人再提類似提案，維護指引就會直接指到本 issue，不必翻 issue 目錄。可選做法：(a) 加一列，改的是 README 記帳區段與報告以外的檔案，會讓本 PASS 失效，要重審或另開分支；(b) 不加，只靠本 issue README 留紀錄。reviewer 建議 (b)：AGENTS.md「範圍」本來就要求有下游實際問題才新增規則，這個 issue 的紀錄已經夠用；如果要加，等合併後另外提交。
- 流程提醒（不列等級）：GitHub #20 目前是 OPEN，合併後懸置掃描會把它判為「README 終態、平台仍 open」，合併時記得關閉平台 issue 並附 README 連結。保存本報告時，可依 document-types.md 在 README 加 `## 現況` 與 `**現行 review**: review-ba669c7.md`（流程契約 2.5 起可選，屬記帳區段）。

## 已查核維度

- 決策來源、理由、殘餘影響、追蹤：三項必要紀錄都有（第 11～14 行）。判定來源是 2026-11-25 使用者逐題確認選「不修復」，之前先選「先問下游再決定」，Timeline 依序記這兩個事件。理由有下游調查支持：六個專案都沒有因報告位置做出錯誤結論的實際案例；回頭引用遍及交接、地雷、程式註解與測試、後續 issue 和懸置掃描；多數下游合併後報告沒有其他副本。理由也符合根目錄 AGENTS.md「範圍」的門檻：沒有下游實際問題，就不新增規則、gate 或檢查。殘餘影響寫了報告累積，以及多份報告要讀完才知最終結論（已由 `**現行 review**` 處理），但漏了 rebase 改 SHA 與過時數值兩項，見 SHOULD FIX。「追蹤：無」的理由具體，和交付範圍相關（不改任何規則、技能或檢查工具）。重新評估條件「下游實際出現一次舊報告留在工作樹而造成錯誤結論或搜尋干擾」可以觀察，寫法和本 kit「刻意不管」表的重新評估條件一致。
- 證據核對：
  - `git diff --stat e5204a4 ba669c7`：只新增 `docs/issues/issue-0020/README.md`（43 行）；`git diff e5204a4 ba669c7 | git patch-id --stable` 為 `4fe28ba202d57a99979eb9ce7ff7ac6b35eef110`，與範圍相符。
  - 報告數：`git ls-tree -r --name-only ba669c7 | grep -cE '^docs/issues/issue-[0-9]+/review-[0-9a-f]{7}\.md$'` 得 63，與 README 相同（BASE 也是 63）。若把 evidence 內同樣命名的回歸產物算進去是 73，README 的 63 是只算 issue 目錄第一層的報告，計法合理。
  - 連結數：原作者的命令重跑得 34。依目錄分組後，29 個在 `docs/issues/issue-*/` 內，5 個在 issue 目錄外（`docs/workflow-results/2026-10-18.md`、`2026-11-03.md`、`2026-11-10.md`，`docs/reviews/review-0bda828.md`、`review-ef4f18d.md`）。
  - 移除模擬：把 ba669c7 的全部追蹤檔逐一寫進 scratchpad（`git archive` 會因 `.gitattributes` 的 `docs/issues/ export-ignore` 漏掉 issue 目錄，所以改用 `git show`），刪除前 `python3 scripts/check-links.py` 回傳 0。刪除 63 份報告後回傳 1，共 109 個 FAIL，分布在 18 個檔案，issue 目錄外的是 `docs/workflow-results/` 的 3 個。
  - 文字引用：`rule-verification-status.md`、`docs/AGENTS.md`、`docs/workflow-regression.md`、`CHANGELOG.md` 等也以純文字引用 `review-xxxxxxx`。check-links 抓不到這些，但移出主幹後它們同樣找不到原文，這是 README 沒寫的額外依賴，方向上支持本決策。
  - 本 repo 現況：`python3 scripts/check-kit.py`、`python3 scripts/check-links.py` 都回傳 0。
  - 下游調查：對照協調者提供的六份回覆摘要，見 SHOULD FIX 第二項與兩則 NICE TO HAVE。
- 格式與流程欄位：`**狀態**: 不修復` 寫在開頭，括號內沒有多餘內容，dev-cycle 狀態表與懸置掃描都能辨認為終態。metadata 有建立日期、分級、風險、狀態。`**分級**` 後附「— 決策紀錄，無規則或程式變更」，fixtures 有同樣的先例，工具不解析這個值。`**風險**: Low\` 與範本一致。日期都是本次系統日期 2026-11-25，Timeline 只記建立與決策兩個語意事件，沒有虛構完成日期。Small 範本的驗收條件、實作步驟與核准欄位在不修復時不適用，省略可以接受。沒有待確認事項，整節省略符合規定。README 沒有下游專案名稱或可識別資訊，只用「六個下游專案」「有專案」「四個專案」這類說法。沒有會讓 verify-artifact、dev-cycle 或懸置掃描判斷錯誤的寫法。
- 限制：下游調查的原始回覆不在 repo，依使用者規定也不能寫入 repo。reviewer 只能對照協調者轉述的摘要，無法查證「都是 agent 在工作樹以搜尋或相對連結找到」這類細節，也無法查證各專案的報告數。本審查沒有在下游專案重跑任何東西。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
