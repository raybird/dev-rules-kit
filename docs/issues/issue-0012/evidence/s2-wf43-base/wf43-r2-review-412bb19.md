# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：4f9778b64863723dbb7a6cdb756fb1783a5f1a93
- Reviewed HEAD SHA：412bb1925826d5caf1371898fdde33cab83db7a0
- Reviewed patch-id：7009e08f632df4e4cca2a2c2485a1283dd0a22ce（`git diff 4f9778b 412bb19 | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者）
- Review artifact：本檔
- 增量覆審：上一份報告 review-d232d03.md（完整範圍，PASS）；增量範圍 `d232d03..412bb19`。前提皆成立：d232d03 是 HEAD 的祖先、中間無 merge 與改寫歷史；`git merge-base main HEAD` 仍為 4f9778b；流程契約 2.7

## 問題與風險
- MUST FIX：無
- SHOULD FIX 1（需決策）：`docs/issues/issue-3601/implementation-plan.md:11` S3 的重構證據不足。verification.md「不改變可觀察行為的任務」要求純重構記錄變更前、後執行同一組測試的命令與全綠輸出；S3 只寫變更後「4 項全數通過」，沒有變更前的執行、輸出與被測提交，也未標為不改變可觀察行為。內容本身無誤：本次 reviewer 已重現兩次執行（d232d03 的 todo.py 配 HEAD 測試 4/4 通過、HEAD 4/4 通過），驗收覆蓋完整，故不阻擋判定。待決問題：S3 的證據要不要回填到計畫檔？做法 A：回 execute-task 在 S3 補兩次執行的命令、輸出與被測 SHA（implementation-plan.md 屬凍結內容，需再覆審一輪）。做法 B：不改 S3，以本報告記錄的重現結果作為等價證據，PR 的 Proof of Test 引用本報告。reviewer 建議 B。
- NICE TO HAVE：無
- 提醒（範圍外，沿用上一份結論）：S1、S2（`implementation-plan.md:9-10`）同樣只有「全數通過」文字，沒有紅綠重構四段證據；增量未改到，沿用上一份報告結論，僅揭露。

## 已查核維度
- 驗收與證據：SCN-001 由 `test_render_shows_due`（`test_due.py:7-9`）與 `test_render_without_due`（`test_due.py:18-20`）覆蓋；SCN-002 由 `test_overdue` 覆蓋。HEAD 412bb19 執行 `python3 -m unittest -v`：Ran 4 tests，OK（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 全部 ok）
- 上一份報告建議的修正確認：
  - SHOULD FIX 1（補沒有到期日的 render 測試）：已修好。期望值 `"[ ] 2. 寫週報"` 為手寫字面值，非同義反覆；把 `todo.py:52` 的 `if due:` 改成 `if True:` 的變異下此測試失敗。更正：`test_todo.py:7-9` 的 `test_render_marks_done` 原本就涵蓋沒有到期日的 render，上一份報告的缺口前提不完全正確；新測試重複但無害
  - NICE TO HAVE 1（抽出 short_date）：已修好，屬純重構。`todo.py:37-39` 的運算式與原本相同；d232d03 的 todo.py 配 HEAD 測試 4/4 通過（新測試可作 characterization test）；`2026-11-20`、`2026-01-05`、`2026-12-31`、空字串下 short_date 與原運算式一致；四組 render 輸入在 d232d03 與 HEAD 輸出相同；拿掉 `.replace` 的變異下 `test_render_shows_due` 失敗
- 增量範圍各檔：
  - `todo.py`：通過，新增 short_date，render 改呼叫（:53），`if due:` 仍在呼叫前，無行為變更
  - `test_due.py`：通過，新增 test_render_without_due
  - `docs/issues/issue-3601/README.md`：通過；`## 現況` 位於 `## 概述` 之後；TBD-1 格式、`已解決` 狀態、日期與決策來源符合規範
  - `docs/issues/issue-3601/implementation-plan.md`：見 SHOULD FIX 1
- 相關失敗面：
  - 有到期日 2026-11-20 → 行尾「（到期 11/20）」；test_render_shows_due 與變異測試覆蓋；通過
  - 沒有 due 鍵 → 不加括號；test_render_without_due、test_render_marks_done 與變異測試覆蓋；通過
  - due 為空字串 → 不加括號；無測試，以 d232d03 與 HEAD 輸出一致確認；行為未變，非新風險
  - 重構前後行為相同 → 同一組測試在 d232d03 程式與 HEAD 皆綠；通過
- 需求、架構、安全、品質：改動仍侷限於 todo.py 與測試檔，無安全面；short_date 只由 render 呼叫，無跨 Task 重複或過度設計
- 增量覆審時重新查核的項目與理由：render 的呼叫處（只有 `todo.py:64` 的 main，輸出不變）；short_date 的呼叫處（只有 render，空字串被 `if due` 擋住）；test_render_shows_due 與 test_render_marks_done（經過被修改的 render，重跑通過）；上一份報告「沒有到期日時不加括號」的結論（重新驗證，現有兩個測試覆蓋）
- 沿用的結論：overdue、due_of 與 test_overdue 未變動，SCN-002、已完成待辦略過、ISO 字串比較順序的結論沿用；根目錄 README.md 的使用說明在 d232d03 前已審，沿用；需求、安全、架構結論沿用
- 豁免、待確認與限制：無 Gate 豁免；TBD-1 已解決，交付影響已覆核。限制：等價與變異檢查由 reviewer 以 repo 外的暫存腳本在記憶體中執行，未保存於 repo

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
