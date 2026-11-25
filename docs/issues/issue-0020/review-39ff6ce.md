# 審查報告
- 範圍：決策審查（增量覆審）
- Reviewed BASE SHA：e5204a4ad56cf88028801d3e61595f0f8077ee0e
- Reviewed HEAD SHA：39ff6ce8248a246f5311584555fb715f332c099f
- Reviewed patch-id：4e2d9a24afc12428e3caf22436fbbf2787d2cfe5
- 獨立 reviewer：Claude Code general-purpose subagent（未參與 README 撰寫與本輪修正）
- 增量覆審：上一份 review-ba669c7.md，增量範圍 `ba669c7..39ff6ce`，處理建議後的增量覆審

## 問題與風險

- MUST FIX：無。
- SHOULD FIX：無。
- NICE TO HAVE：README「決策紀錄」殘餘影響的最後一句「後兩項是差點出事的情況」，把 rebase 改寫 SHA 也歸成差點出事。上一份報告把它列為已經發生的額外工夫（成本），只有過時數值那一例是差點出事。調查表第一列寫的是「差點出事與額外工夫見上節殘餘影響」，與這句不一致。建議改成「rebase 一項是已經發生的額外工夫，過時數值一項差點出事；兩項都沒有造成錯誤結論，沒有達到重新評估的門檻」。本輪新寫的句子才有這個問題。
- NICE TO HAVE：同一段新增了兩處細節，「下游要另加註對照」與「讀者改從其他來源查證」。上一份報告記的摘要只寫到「報告檔名與 Reviewed SHA 指向主幹上不存在的 commit」與「沒有因此做錯的紀錄」，reviewer 拿不到原始回覆，無法查證這兩處。請協調者對照下游原始回覆確認；回覆裡沒有的話，刪掉這兩個子句，結論不受影響。
- NICE TO HAVE：TBD-2 的狀態欄有結論（加在本分支、與 TBD-1 一起送增量覆審）與日期，但沒寫理由。docs/AGENTS.md「待確認事項」規定 `已解決` 要有結論、理由與日期。可補一句理由，例如「日後再有同類提案時，從維護指引就能找到本決策」。TBD-1 的理由是處理審查建議、決策不變，可以接受。狀態值本身合法，不影響 verify-artifact 與懸置掃描的判定，所以列 NICE TO HAVE。
- 流程提醒（不列等級）：保存本報告時，把 `## 現況` 的 `**現行 review**` 改成 review-39ff6ce.md，Timeline 補一列本次覆審（記帳區段）。GitHub #20 仍是 OPEN，合併時要關閉並附上 README 連結。

## 已查核維度

- 範圍核對：HEAD 是 `39ff6ce8248a246f5311584555fb715f332c099f`；`git diff e5204a4 39ff6ce | git patch-id --stable` 得 `4e2d9a24afc12428e3caf22436fbbf2787d2cfe5`，與指定值相同。`ba669c7..39ff6ce` 改了三個檔：AGENTS.md（+1 列）、issue README、新增 review-ba669c7.md。c003a17 只改 README 5 行並保存報告，屬記帳提交。增量沒有夾帶建議以外的修改，適用「處理建議後的增量覆審」。
- 逐項確認上一份報告的 6 項建議：
  1. SHOULD FIX 1（連結數）：已修好。README 改寫成「報告以外有 18 個 Markdown 檔以相對連結指向 issue 報告（其中 3 個在 issue 目錄外），刪掉全部 63 份後 check-links 回報 109 個斷連結」，並註明這是移出主幹要處理的代價，原提案設計點 3 已列出。`gh issue view 20` 的「要設計的點」第 3 點確實要求合併後引用仍查得到、check-links 不能失敗。數字由本輪重跑確認，見下方「重跑」。
  2. SHOULD FIX 2（漏揭露的不利證據）：三項都補上。rebase 改寫 SHA、過時數值兩項寫進殘餘影響，「成本只有一項」改成「三項」。誤引用案例改成上一份報告建議的持平寫法：起因是沒分辨推論與實測；報告不在工作樹時這次誤引用不會發生，但同一批報告的正確引用也會失去，且已由下一輪審查更正。理由裡的「或多花工夫」刪了，與新承認的額外工夫不衝突。分類用語與新增細節見 NICE TO HAVE 第 1、2 項。
  3. NICE TO HAVE 1（前提說太滿）：已修好。概述改成「大部分報告合併後確實沒人讀，但事先無法知道哪一份會被引用……」，調查表補「約 55 份中約 50 份沒被任何文件引用」。
  4. NICE TO HAVE 2（合併方式）：已修好。(a) 調查表與理由都改成「主要不開 PR／MR」；(b) 改成「明確保留已合併遠端分支的只有兩個專案」，並寫出其餘的情況。squash 後原始分支不存在的那個專案寫在上一列「報告的其他副本」，沒有遺漏。
  5. NICE TO HAVE 3（地雷升級概括過度）：已修好。改成「部分下游已用……；也有專案的遺留項目只寫在報告」，結論維持「本 issue 不另行處理」。
  6. NICE TO HAVE 4（需決策）：使用者選 (a)，在本分支 AGENTS.md「刻意不管」表加一列。改的是凍結內容，所以本次增量覆審要涵蓋它，處理方式正確。
- AGENTS.md 新增的列：三欄格式與其他列一致。「不管什麼」寫 kit 不做的事，「去處」寫報告留在主幹，用法和「文件的 HTML 閱讀版／不做」相同。重新評估條件與 README 決策紀錄的寫法逐字一致，也和「對抗刻意造假」列的「下游實際出現一次……的案例」句型一致。新列放在「平台操作、跨專案彙總」之前，表格沒有斷開。連結 `docs/issues/issue-0020/README.md` 存在，check-links 回傳 0。這是根目錄 AGENTS.md 第一個指向 docs/issues/ 的連結；`.gitattributes` 讓 release 壓縮檔排除 docs/issues/，所以壓縮檔裡這個連結會斷。不過 docs/workflow-results/ 已有 3 個檔案同樣連到 issue 報告，壓縮檔也只是安裝來源，根目錄 AGENTS.md 不會部署到下游，影響可以忽略，不列為問題。
- README 其他受影響之處：`## 現況` 放在 `## 概述` 之後，只有一行 `**現行 review**`，符合 document-types.md。待確認事項照範本的四欄表格書寫，編號 TBD-1、TBD-2，狀態都以合法值 `已解決` 開頭，含日期。影響欄只寫未確認時的影響（這個 issue 沒有驗收編號）。整節沒有 `<`，行首沒有粗體或 `[`。使用者對需決策的答案記在待確認事項，符合 review-evidence.md。`**分級**` 改成「決策紀錄；另在根目錄 AGENTS.md『刻意不管』表加一列，無規則或程式變更」，與概述一致；工具不解析這個值。Timeline 補了兩列，日期都是本次系統日期 2026-11-25。
- 不修復的必要紀錄：`**狀態**: 不修復` 不變。判定來源（2026-11-25 逐題確認）、理由、殘餘影響（現在列三項成本）、追蹤（無，附重新評估條件，並指到 AGENTS.md）都還在。docs/AGENTS.md「有特殊意義的狀態值」對 `不修復` 要求的三項記錄都齊全。
- 下游專案名稱：README 與 AGENTS.md 新增的文字都沒有下游專案名稱，只用「一個專案」「兩個專案」「部分下游」這類說法。
- 重跑：
  - 把 ba669c7 與 39ff6ce 的全部追蹤檔，用 `git ls-tree` 加 `git show` 寫進 scratchpad 的副本，repo 本身沒動。刪除前 `python3 -I scripts/check-links.py` 兩份都回傳 0。
  - ba669c7 刪除 63 份 `docs/issues/issue-*/review-*.md` 後回傳 1，共 109 個 FAIL，分布在 18 個檔案；issue 目錄外的是 `docs/workflow-results/2026-10-18.md`、`2026-11-03.md`、`2026-11-10.md`，共 3 個。
  - 39ff6ce 有 64 份報告（多了 review-ba669c7），全部刪除後同樣是 109 個 FAIL、18 個檔案、3 個在 issue 目錄外，輸出與 ba669c7 完全相同。README 的 18／3／109 正確；「63 份」是調查當時的數量，與殘餘影響「本 repo 63 份」的時間點一致。
  - repo 現況：`python3 scripts/check-kit.py`、`python3 scripts/check-links.py` 都回傳 0。
- 其餘維度沿用 review-ba669c7.md。
- 限制：本輪新增的兩處下游細節（rebase 後「另加註對照」、過時數值「改從其他來源查證」）沒有原始回覆可以對照，見 NICE TO HAVE 第 2 項。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
