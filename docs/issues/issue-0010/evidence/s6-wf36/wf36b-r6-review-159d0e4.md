# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：39045ddd5d3458dcf1b32a66f990983c56e2ef07
- Reviewed HEAD SHA：159d0e45fe56316fae8976637cf1f8cc90c6bf16
- Reviewed patch-id：00b4c942e8cea54157a5b267ca71d80464365d12
- 獨立 reviewer：獨立 subagent（非原實作者）
- Review artifact：本檔
- 增量覆審：上一份報告 review-547810e.md（PASS，H1=547810e，完整範圍）；增量範圍 547810e..159d0e4。H1 是 HEAD 的祖先、之後沒有改寫歷史與 merge；main 仍為 39045dd，merge-base 等於原 Reviewed BASE

## 問題與風險
- MUST FIX：無
- SHOULD FIX 1（需決策）：`docs/issues/issue-3601/implementation-plan.md` 第 9–10 行，S1／S2 只記「3 項全數通過」，缺 verification.md「紅綠重構證據」的紅燈與重構後全綠紀錄。這是 547810e 就有、上一份報告未指出的缺口。變異測試確認測試能抓到目標行為錯誤，不是假綠燈，也沒有驗收覆蓋缺口，所以不阻擋 PASS。待決問題：補記證據，還是接受只有綠燈紀錄？可選做法：(a) 補記 S1／S2 的紅綠證據，例如在 bcbe2cb 跑新測試的紅燈命令與輸出，加上重構 no-op 理由；implementation-plan.md 不屬記帳區段，提交後本 PASS 失效、需再覆審。(b) 接受現狀，結論記入 README 待確認事項。reviewer 建議 (a)
- NICE TO HAVE 1：`test_due.py` 第 18–20 行的 `test_render_without_due` 與 `test_todo.py` 第 7–9 行的 `test_render_marks_done` 重疊；後者已用字面值驗證沒有到期日的 render。上一份 SHOULD FIX 1「沒有這類測試」的前提不完全成立。新測試把情境掛在 SCN-001 下，有可讀性價值，不必刪
- NICE TO HAVE 2：`implementation-plan.md` 第 11 行 S3 只補測試、不改 production code，所以不會有紅燈；建議註明「只補測試、不改變可觀察行為」並記被測 commit

## 已查核維度
- 驗收與證據：SCN-001 由 `test_render_shows_due` 覆蓋，沒有到期日的情況另有 `test_render_without_due`；SCN-002 由 `test_overdue` 覆蓋。在 HEAD 159d0e4 重跑 `python3 -m unittest -v`：Ran 4 tests，OK（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 皆 ok）
- 相關失敗面：沒有到期日的待辦——`render` 不加括號（現由兩個字面值斷言覆蓋）、`overdue` 略過；已完成的待辦——`overdue` 略過；`overdue` 以 ISO 字串比較，字串順序與日期順序一致
- 需求、架構、安全、品質：改動侷限於 todo.py 與測試，無安全面；`render` 與 `overdue` 共用 `due_of`，無過度設計；跨檔測試重複見 NICE TO HAVE 1。常青文件：根目錄 README.md 已記到期日顯示；`overdue` 不是 CLI 指令，不需寫入使用說明
- 增量覆審時重新查核的項目與理由：
  - test_due.py（159d0e4）：期望值為字面值；變異測試（從 HEAD 取出程式在記憶體中變異）顯示無到期日也加括號時 `test_render_without_due` 與 `test_render_marks_done` 失敗，`due_of` 預設改為非空時三項測試失敗。SHOULD FIX 1 已修好
  - implementation-plan.md（159d0e4）：S3 證據屬實，重跑 4 項全過
  - issue README.md（0cbf70f、159d0e4）：只動記帳區段（`## 現況`、整節新增且只有表格的 `## 待確認事項`、Timeline 一列、`**狀態**`）；`## 現況` 位於 `## 概述` 之後；`git diff bcbe2cb HEAD` 顯示 Gherkin 區塊未變，SCN-001、SCN-002 核准仍有效
  - review-547810e.md（0cbf70f）：綁定 H1、完整範圍的持久化報告，可作增量依據
- 沿用的結論：todo.py 與根目錄 README.md 在增量範圍內未變動，上一份報告對實作正確性、失敗面、安全與架構的結論確認不受影響，沿用
- 豁免、待確認與限制：TBD-1 已解決（修正後覆審），本次確認已修；無 Gate 豁免

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
