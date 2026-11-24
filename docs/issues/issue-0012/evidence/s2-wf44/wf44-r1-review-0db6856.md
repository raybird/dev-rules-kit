# 審查報告
- 範圍：完整交付範圍（`main..issue-3601-due`）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf（main，亦為 merge-base）
- Reviewed HEAD SHA：0db6856e3853e4694b56d084538e763e04615cfb
- Reviewed patch-id：d17d1b24f53650fa49e6726287e283d20a696b95（`git diff 70f4ada 0db6856 | git patch-id --stable`）
- 獨立 reviewer：Claude Code 宿主隔離 subagent（general-purpose，agentId a05801b473009eed4），非原實作者；協調者複核關鍵事實
- 審查日期：2026-11-24

## 問題與風險

1. **MUST FIX：SCN-001／SCN-002 缺紅綠重構證據**（`docs/issues/issue-3601/implementation-plan.md:9-10`）
   - verification.md「紅綠重構證據」要求四段：外迴圈紅燈、單元紅燈、最小實作後全綠、重構後全綠，每段記驗收編號、命令、exit code／結果摘要與原因。
   - S1、S2 證據欄只有「✅ 2026-11-17；`python3 -m unittest -v` 3 項全數通過」與「同上」：無紅燈、無被測提交、無重構段或 no-op 理由、未說明單迴圈合併理由。依 verification.md 第 20 行，只有「測試已通過」的文字不構成證據。
   - reviewer 推論紅燈可取得（BASE 的 `todo.py` 沒有 `overdue` → AttributeError；render 少「（到期 11/20）」→ 斷言失敗），但推論不能代替實作者紀錄。
   - 建議：回 execute-task，在暫存目錄取出 BASE 的 `todo.py` 搭配新測試取得真實紅燈，逐段記錄命令、輸出與原因；重構若為 no-op 寫明理由。

2. **MUST FIX：S1 證據紀錄與實作歷史不符（不實回報疑慮）**（`docs/issues/issue-3601/implementation-plan.md:9`、`docs/issues/issue-3601/README.md:55`）
   - 兩處都寫「完成 S1，測試 3 項通過」。3 項包含 S2 的 `test_overdue`；若 S1 先於 S2 完成，當下只會有 2 項或 `test_overdue` 為紅燈。
   - `main..HEAD` 只有 30ddef5（文件）與 0db6856（S1、S2 與文件回填同一提交），沒有可佐證「S1 完成、S2 未完成」的狀態。
   - 建議：依實際順序分別記 S1、S2 證據；若實際是一起實作，照實寫成同一次證據並註明兩個 SCN 各自對應的測試。

3. **SHOULD FIX `需決策`：功能沒有使用者入口**（`todo.py:18-21`、`todo.py:37-39`、`todo.py:53-59`）
   - `add()` 不接受 due，CLI 沒有設定到期日或列出逾期的子命令；`overdue()` 在 production 程式中無呼叫者。使用者只能手改 `todo.json` 才看得到到期日，`overdue` 無法從 CLI 使用。
   - 已核准 Gherkin 寫的是「執行 render」「呼叫 overdue」的函式層級，實作未超出或違反核准範圍，故不列 MUST FIX；但 acceptance.md 第 36 行要求 Scenario 描述外部行為，規格本身有缺口。
   - 待決問題：本 issue 是否要提供 CLI 入口設定 due（例如 `add 標題 --due YYYY-MM-DD`）並列出逾期（例如 `todo.py overdue`，today 取系統日期）？
   - 可選做法：(a) 維持函式層級交付，另開 issue 追蹤 CLI；(b) 本 issue 補 CLI，新增／修訂 Scenario 並重新核准。
   - reviewer 建議：(a)，對核准範圍影響最小；若使用者期待直接可用則選 (b)。

4. **SHOULD FIX：Timeline 記了任務完成事件**（`docs/issues/issue-3601/README.md:55-56`）
   - docs/AGENTS.md「Agent 工作流程與時序保留」第 3 項：Timeline 只記建立、核准、規格修訂等語意事件，任務狀態寫在任務來源。「完成 S1…」「完成 S2」應移除。格式問題，依 review-evidence.md 第 80 行列 SHOULD FIX。

5. **SHOULD FIX：到期日格式未驗證，非 ISO 格式輸出錯誤**（`todo.py:47-48`、`todo.py:39`）
   - `render` 以 `due[5:]` 切字串，實測：`"11-20"` →「（到期 ）」；`"2026-11-20T09:00"` →「（到期 11/20T09:00）」。`overdue` 以字串比較，只在固定 `YYYY-MM-DD` 下等於日期比較。
   - 目前沒有寫入路徑，風險只來自手改 JSON。若第 3 項選 (b)，須在輸入端驗證格式並補失敗路徑 Scenario。

6. **NICE TO HAVE：`due_of` 抽象可移除**（`todo.py:32-34`、`todo.py:39`、`todo.py:46`）
   - 只包一層 `item.get("due", "")`，且 `overdue` 對同一項呼叫兩次。可簡化為 `[i for i in items if not i["done"] and i.get("due") and i["due"] < today]`，`render` 直接用 `i.get("due")`。
   - docstring 寫「沒有到期日時回傳空字串」，但 `due: null` 時實際回傳 None（行為無害，說明不準）。

7. **NICE TO HAVE：證據持久力**（`test_due.py:7-16`）
   - 非假綠燈：期望值為手寫字面值，非同義反覆或硬編碼答案。
   - 未覆蓋的邊界：到期日等於今天（`<` 改成 `<=` 擋不住）、done 項目 render 顯示到期日、`due` 為 None／空字串維持原輸出。建議補斷言。

8. **NICE TO HAVE：小項**
   - `docs/issues/issue-3601/README.md:5`：概述含「測試全數通過，等待審查」等現況敘述，宜交給 `**狀態**`／`## 現況`。
   - `docs/issues/issue-3601/README.md:13`：涉及檔案未列根目錄 `README.md`。
   - `README.md:10`：常青文件描述使用者無從設定的行為；選 (a) 時補一句「到期日目前需手動寫入 todo.json 的 `due`（YYYY-MM-DD）」，選 (b) 時寫入新指令與 overdue 用法。

## 已查核維度

- 驗收與證據：
  - 核准 commit `30ddef5`（非 `待提交`）；`git diff 30ddef5 0db6856 -- docs/issues/issue-3601/README.md` 只動核准 commit 回填、Timeline 兩列與狀態，Gherkin 未變，原核准有效。依 acceptance.md 推導命令得到 30ddef527b20780fe65cbe42380201c676422cc3，與回填值一致。
  - 核准來源「2026-11-16 使用者回覆『核准』」，全部 Scenario 同日核准；TBD-1 已解決並有日期。
  - SCN-001 → `test_due.py:7`；SCN-002 → `test_due.py:11`。HEAD 執行 `python3 -m unittest -v`：Ran 3 tests，OK（協調者與 reviewer 各跑一次）。
  - 紅燈與重構紀錄缺失、S1 紀錄與歷史不符：見第 1、2 項。
  - 提交訊息為 `type: 摘要` 帶 `Refs: #3601`，缺 project.md 要求的 `(scope)`，屬格式小項。
- 相關失敗面（reviewer 在 HEAD 實際呼叫 `todo.render`／`todo.overdue`）：

  | 失敗面 | 輸入 | 預期 | 覆蓋 | 結論 |
  |---|---|---|---|---|
  | 無 due 欄位（TBD-1） | 項目無 `due` 鍵 | 維持原輸出 | `test_todo.py` 未改且通過；`test_overdue` id 4 | 正確 |
  | due 為 None／空字串 | `due: None`、`due: ""` | 不加後綴、overdue 排除 | 實測正確；無測試 | 正確，見第 7 項 |
  | 到期日等於今天 | due 與 today 皆 2026-11-19 | 不算逾期（規格「早於」） | 實測不回傳；無測試 | 正確，見第 7 項 |
  | 已完成項目 overdue | done=True 且已過期 | 排除 | `test_overdue` id 3 | 正確 |
  | 已完成項目 render | done=True 且有 due | 規格未定 | 實測顯示到期日 | 可接受 |
  | 非 YYYY-MM-DD 格式 | `"11-20"` 等 | 規格未定義 | 無測試 | 輸出錯誤，見第 5 項 |
  | overdue／add 入口 | 無 CLI | 規格只要求函式 | 無 | `需決策`，見第 3 項 |
  | done 保留 due | `done()` 只改 done | 保留 | 程式碼確認 | 正確 |
  | 空清單 | `render([])` | `''` | 實測同原行為 | 正確 |

- 需求、架構、安全、品質（含跨 Task 重複與過度設計）：
  - 架構：單檔 CLI，新增純函式，無邊界違反。
  - 安全：不適用，無新外部輸入、權限、網路或路徑處理。
  - 依賴：不適用，只用標準函式庫，無 lockfile 變更。
  - 重複與過度設計：`due_of` 見第 6 項；S1、S2 間無其他重複邏輯。
  - 常青文件：見第 8 項。
- 豁免、待確認與限制：
  - 無 `## Gate 豁免紀錄`，無豁免。TBD-1 已解決，結論與實作相符。
  - 限制：無法從歷史還原 S1／S2 實際順序，只能依現有紀錄推論；BASE 上的紅燈為推論，未實際執行。

## 流程判定

RETURN TO execute-task

理由：SCN-001／SCN-002 缺紅綠重構證據（第 1 項）、S1 證據紀錄與提交歷史不符（第 2 項），皆為 MUST FIX。第 3 項 `需決策` 由協調者依 acceptance.md「逐題確認」向使用者取得決定。
