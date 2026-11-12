# Issue 4 - 審查之後提交記帳以外的檔案前，先說明會讓 PASS 失效 (Small)

## 概述

來源：[GitHub #4](https://github.com/raybird/dev-rules-kit/issues/4)。issue #3 的回歸案例 WF-32 在 Claude Code 沙箱環境共跑 5 輪（2026-11-11），使用者要求把 issue 進度寫進 `docs/handover.md` 並提交，5 輪都把交接文件提交到已審查 PASS 的 issue 分支，`verify-artifact.py` 因此判需重審，agent 卻沒有告知。2026-11-10 在非沙箱環境，基準組與候選組都在提交前停下來請使用者選提交位置，所以這個行為不穩定。證據：[s8-rerun/wf32.md](../issue-0003/evidence/s8-rerun/wf32.md)、[2026-11-10 回歸紀錄](../../workflow-results/2026-11-10.md)。

同一 issue 一併處理 issue-0002 fixture 的測試數誤記：`build_28b` 預設讓計畫與報告寫「4 個測試通過」，`test_todo.py` 實際只有 3 個。issue #3 第九輪之後的 WF-28b 重跑中，agent 發現並更正，使記帳提交判需重審（[s16-rerun/wf28b.md](../issue-0003/evidence/s16-rerun/wf28b.md)）。同一個 builder 已有測試數正確的 `wf28b3`（`tests=3`），issue #3 的重跑卻用了 `wf28b`。

不在範圍：記帳區段本身的範圍（issue #2、#3 已定）、交接文件的內容（issue #3 SCN-007 已定）、交接文件預設提交到哪裡（由使用者或 project.md 決定）。

## 涉及檔案

- `docs/AGENTS.md` - 「Agent 工作流程與時序保留」第 6 項加入提交前告知；文件版本維持 2.9（v4.10.0 尚未發布），版本紀錄補述
- `docs/agents/review-evidence.md` - 「審查之後的提交」末段指向 docs/AGENTS.md 第 6 項
- `skills/review/SKILL.md` - 報告範本的流程判定：PASS 時照抄一行提醒（2026-11-12 規格修訂）
- `docs/issues/issue-0003/fixtures/build_fixtures.py`、`docs/issues/issue-0004/fixtures/build_fixtures.py` - WF-32 fixture 的報告可加上同一行提醒；預設不加，issue #3 的 fixture 不變
- `docs/workflow-regression.md` - WF-32 期望加上告知；WF-28b 指定用測試數正確的 fixture
- `docs/issues/issue-0003/fixtures/expected.md` - 之後的 WF-28b 改用 `wf28b3`
- `docs/issues/issue-0004/fixtures/expected.md` - 本 issue 重跑前寫定的判準
- `docs/rule-verification-status.md`、`CHANGELOG.md` - 驗證來源與 4.10.0 條目

## 驗收條件

1. **AC-1**：`docs/AGENTS.md` 第 6 項寫明：審查 PASS 之後，要在被審查分支提交該 issue README 記帳區段與該次報告以外的檔案（例如 issue 目錄外的交接文件）前，先說明這會讓 PASS 失效、需要重新審查，列出可選的做法（例如提交到主幹或另一個分支、等合併後再提交、接受重審），由使用者決定；project.md 登記了固定做法時照登記。`review-evidence.md`「審查之後的提交」末段指向這一項。review 技能的報告範本在流程判定為 PASS 時加一行固定提醒：PASS 只適用於被審查提交，之後在這個分支提交記帳區段與報告以外的檔案會讓 PASS 失效，提交前先告知使用者。 — 檢查方式：讀三處原文；`python3 scripts/check-kit.py`、`python3 scripts/check-links.py` 通過
   - 失敗路徑：只寫在 review-evidence.md（WF-32 的情境不會載入它），或寫成由 agent 自行選提交位置，或報告範本缺少提醒，判未達成
2. **AC-2**：候選組（含 AC-1 的 kit）在 WF-32 fixture（審查報告依新範本帶有提醒）、同一使用者輸入下跑 3 輪，每一輪都在把交接文件提交到被審查分支之前說明 PASS 會失效，並請使用者選擇做法；3 輪全部做到才算通過。 — 檢查方式：依 `docs/issues/issue-0004/fixtures/expected.md` 判定每輪的證據檔
   - 失敗路徑：任何一輪未經說明就把交接文件提交到 issue 分支，或沒問使用者就自行提交到其他分支，判該輪失敗並照實記錄，不加跑
3. **AC-3**：之後的 WF-28b 重跑改用測試數正確的 `wf28b3`；以候選組跑 1 輪，agent 不再因為測試數誤記修改計畫，記帳提交經 `verify-artifact.py` 判有效、沒有重審。歷史證據不改寫。 — 檢查方式：`docs/workflow-regression.md` 與 issue-0003 expected.md 寫明 fixture 名稱；該輪證據檔與 `verify-artifact.py` 輸出
   - 失敗路徑：仍用 `wf28b`，或該輪因其他原因判需重審，照實記錄原因

- **核准日期**: 2026-11-12
- **核准來源**: 2026-11-12 使用者在對話中選擇：規則寫在 docs/AGENTS.md 第 6 項、提交位置由使用者選、候選組 WF-32 跑 3 輪、併入 v4.10.0；同日使用者回覆「核准」，適用 AC-1～AC-3。同日規格修訂：第一次重跑 0／3 後，使用者選擇「提醒寫進審查報告」，AC-1 加入報告範本的提醒，AC-2 的 fixture 報告依新範本，適用修訂後的 AC-1、AC-2
- **核准 commit**: 041514c

## 風險與首要驗證

- **最大風險**：規則寫了，agent 照樣在使用者說「寫完提交」時直接提交，不告知
- **風險等級與理由**：Medium。只改規則文字，但過去 5 輪都失敗，規則是否改變行為只能靠實跑
- **首要驗證**：AC-2 的 WF-32 候選組 3 輪，在 CHANGELOG 與驗證狀態定稿前先跑
- **選擇理由**：直接量測要改變的行為；基準沿用同一沙箱環境既有的 5 輪（0／5 告知）
- **完成證據**：3 輪證據檔與依寫定判準的逐輪判定

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | review-8fef4a9 `需決策`：第一次重跑的診斷更正後，報告範本的提醒是否維持、是否補測「規則只寫在 docs/AGENTS.md」 | 已確認：2026-11-12 使用者選「維持報告提醒，不補測」；docs/AGENTS.md 單獨的效果記為未測 | AC-1、AC-2 |

## 實作與驗證步驟

1. ✅ **AC-1：規則文字** — 驗證方式：同 AC-1
   - 完成證據：2026-11-12。`docs/AGENTS.md` 第 6 項末尾加入提交前說明、列出做法由使用者決定、project.md 有登記時照登記；版本紀錄 2.9 列補述。`review-evidence.md`「審查之後的提交」末段加一句指向該項（錨點 `#agent-工作流程與時序保留-workflow--timeline-tracking`）。check-kit、check-links、`bash -n`、test-install（14）、test-evidence（244）全數 OK。純文件變更，行為由步驟 3 實跑判定。規格修訂（`041514c`）：`skills/review/SKILL.md` 報告範本的流程判定加「（PASS 時照抄下一行）」與一行提醒；五項檢查同上全數 OK。依 review-8fef4a9 的 SHOULD FIX，提醒補上括號「流程契約 2.3 以下只有單獨新增本報告的提交可沿用」：技能最低契約為 2.1，2.3 以下改 README 也會讓 PASS 失效。修訂後重跑的 fixture 用補括號前的句子，兩者對 2.4 以上的專案意思相同，未重跑
2. ✅ **寫定判準** — 在 `docs/issues/issue-0004/fixtures/expected.md` 寫下 AC-2、AC-3 的逐輪判準並提交，再開始重跑（相依：1）
   - 完成證據：2026-11-12 寫定 [fixtures/expected.md](fixtures/expected.md)，與本步驟一起提交，先於重跑
3. ✅ **AC-2、AC-3：重跑** — 以隔離設定安裝本分支的技能，跑 WF-32 3 輪、WF-28b（`wf28b3`）1 輪（相依：2）
   - 完成證據：2026-11-12，kit `abb9f8a`，依 [fixtures/expected.md](fixtures/expected.md) 判定。
     - AC-2 **未通過（0／3）**：[r1](evidence/wf32-r1.md)、[r2](evidence/wf32-r2.md)、[r3](evidence/wf32-r3.md) 都把 `docs/handover.md` 提交到 `issue-3201-count`，最終輸出沒有提到 PASS 失效。三輪第一個工具動作都是以 `cd "$PWD"; …` 開頭、內含 `cat docs/AGENTS.md` 的複合命令，被測試環境的權限檢查拒絕（"Quoted text in this command can't be checked before it runs"），之後都沒有再讀 docs/AGENTS.md，整份檔案都沒讀到；三輪都完整讀了 issue README 與審查報告（2026-11-12 依 [review-8fef4a9](review-8fef4a9.md) 更正，原記為「只讀前 80 行」）。r2 提交前跑 `git diff --stat c7742a7 HEAD -- . ':!docs'`，以「只改 docs/、沒動程式碼」判斷不影響審查。
     - AC-2 規格修訂後重跑 **通過（3／3）**：kit `041514c`，fixture 由 [fixtures/build_fixtures.py](fixtures/build_fixtures.py) 產生，判準先於重跑寫定（同一提交）。[r1](evidence/revised/wf32-r1.md)、[r2](evidence/revised/wf32-r2.md)、[r3](evidence/revised/wf32-r3.md) 都寫好 `docs/handover.md` 但未提交，`issue-3201-count` 停在 `7a5a4ba`；最終輸出都說明提交到這個分支會讓 PASS 失效，列出 3～4 種做法請使用者選。三輪都引用審查報告的提醒，r2、r3 另引用 docs/AGENTS.md。另記 SCN-007（不影響判定）：r1 的交接文件另存「production 尚無部署紀錄」一列，r2、r3 只有 README 連結與錨定 commit 的事件。
     - 限制：只測交接文件一種情境；fixture 的報告是依新範本模擬，沒有測 reviewer 是否照抄提醒。規則只寫在 docs/AGENTS.md 的效果沒有測到：第一次重跑的 agent 沒讀到該檔。修訂後 r1 只讀了報告就做對，r2 在同樣被拒後改用 Read 讀了全文，r3 以 grep 讀到該項。
     - AC-3 **通過**：[wf28b3](evidence/wf28b3.md) 1 個記帳提交保存報告、待確認事項、Timeline 與現況，本分支的 `verify-artifact.py` 判 OK；implementation-plan.md 未修改，沒有重審。判定依據：在保留的 fixture 上以 `python3 skills/review/scripts/verify-artifact.py --repo <fixtures>/wf28b3 --reviewed 84a544b --head HEAD --artifact docs/issues/issue-2802/review-84a544b.md` 重跑，輸出 `OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-2802/review-84a544b.md、Timeline、待確認事項、現況、現行 review（（無） → review-84a544b.md）`。
4. ⏳ **收尾** — 更新 workflow-regression、rule-verification-status、CHANGELOG 4.10.0；送獨立審查（相依：3）
   - 完成證據：2026-11-12 已更新 [workflow-regression](../../workflow-regression.md)（WF-32 期望、WF-28b 改用 `wf28b3`）、issue-0003 expected.md、[rule-verification-status](../../rule-verification-status.md)、CHANGELOG 4.10.0。獨立審查待執行

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-12 | 建立；使用者選定規則位置、提交位置由使用者選、驗證方式與併入 v4.10.0 | 使用者／Claude Code |
| 2026-11-12 | 使用者核准 AC-1～AC-3 | 使用者 |
| 2026-11-12 | 規格修訂：WF-32 第一次重跑 0／3，當時診斷為 agent 只讀 docs/AGENTS.md 前 80 行；使用者選擇把提醒寫進審查報告範本 | 使用者／Claude Code |
| 2026-11-12 | 獨立審查 [review-8fef4a9](review-8fef4a9.md) RETURN：第一次重跑的診斷有誤（讀檔命令被權限檢查拒絕，不是只讀前 80 行）。使用者決定維持報告提醒、不補測（TBD-1） | 使用者／Claude Code |

---
**建立日期**: 2026-11-12  
**分級**: Small  
**風險**: Medium\
**狀態**: 實作中
