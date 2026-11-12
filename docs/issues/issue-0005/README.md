# Issue 5 - 記帳判定記下凍結段落前接的內容 (Small)

## 概述

來源：[GitHub #5](https://github.com/raybird/dev-rules-kit/issues/5)。issue #3 第六輪覆審（[review-20d0847](../issue-0003/review-20d0847.md)）列出的 V3：記帳章節裡，表格後面接著含凍結內容的段落（例如檔尾的 `**分級**`），審查之後的提交刪掉兩者之間的空行，GFM 會把凍結段落渲染成表格的一列，`verify-artifact.py` 卻判有效。原因是檢查器記下段落怎麼結束（空行、下一個標題或檔尾），沒有記下段落前面接的是什麼。

2026-11-12 依 [#6](https://github.com/raybird/dev-rules-kit/issues/6) 的界線重新分類後，#5 只剩 V3：照撰寫規範寫的人編輯時也可能不小心刪到空行，屬缺陷。V4、V6、V7、R9-1～R9-3 改列已知限制，不在本 issue 範圍。

2026-11-12 以 marked 與 micromark 重現（拋棄式輸入，不進 repo）：

| 情況 | 渲染結果 | 目前檢查器 |
|---|---|---|
| 表格、空行、`**分級**: Small` | 表格之後是段落 | — |
| 同上，刪掉空行 | 兩個渲染器都把 `**分級**: Small` 渲染成表格第二列 | 凍結內容與原版相同，判不出 |
| 表格、空行、`---`、檔尾欄位（範本寫法） | 表格、分隔線、段落 | — |
| 同上，刪掉空行 | 與原版相同：`---` 是分隔線，會結束表格 | 凍結內容相同 |

不在範圍：V4、V6、V7、R9 系列（已知限制）；凍結章節（記帳章節以外）的空行本來就逐行比對，不受影響。

## 涉及檔案

- `skills/review/scripts/verify-artifact.py` - 記帳章節含凍結內容的段落，記下段落前接的內容；前接表格列時凍結該表格的表頭與分隔列
- `scripts/test-evidence.py` - 正負向案例
- `docs/agents/review-evidence.md` - 「審查之後的提交」補一句：段落前接的內容也列入比對
- `CHANGELOG.md`、`docs/rule-verification-status.md` - 併入 4.10.0；已知限制刪掉 V3

## 驗收條件

1. **AC-1**：記帳章節裡含凍結內容的段落，除了段落怎麼結束，也記下前接的是空行、標題、表格列，還是章節的第一行；前接的內容改變時判需重審，錯誤訊息指出是哪個章節的哪一段。 — 檢查方式：`python3 scripts/test-evidence.py` 新增案例先紅後綠：刪掉表格與凍結段落之間的空行判 INVALID；在表格與緊接的凍結段落之間補空行判 INVALID；範本的 `---` 檔尾刪掉前面的空行也判 INVALID（從嚴，渲染相同但不另外辨認）
   - 失敗路徑：任何一個案例判 OK
2. **AC-2**：不含凍結內容的段落、表格補列、Timeline 與待確認事項的一般記帳提交，判定結果不變。 — 檢查方式：既有 244 項全部通過；新增案例：表格補列後接範本檔尾判 OK。另以本分支的檢查器重判最近實跑留下的 agent 記帳提交（issue #4 的 wf28b3、issue #3 最後一輪的 wf31），都仍判 OK
   - 失敗路徑：既有案例失敗，或重判出現 INVALID
3. **AC-3**：統計下游 README 裡「表格之後沒有空行、直接接著含凍結內容的段落」的數量，寫進證據；這些文件之後在該處補空行會判需重審。 — 檢查方式：以 issue #3 的 `scan_downstream.py` 同一份 README 清單重跑擴充後的統計
   - 失敗路徑：沒有統計就交付

- **核准日期**: 2026-11-12
- **核准來源**: 2026-11-12 使用者要求「#5 是否可以等的時間也一起處理」；修法採 #5 的待決定選項之一「記下段落前接的是表格、標題還是空行」；同日使用者回覆「核准」，適用 AC-1～AC-3
- **核准 commit**: c8165cb

## 風險與首要驗證

- **最大風險**：從嚴之後，下游常見的記帳寫法被誤判需重審，又回到 #2 要解決的重審負擔
- **風險等級與理由**：Medium。只改一個判定，但它是 PASS 能否沿用的 gate，誤判的成本是整輪重審
- **首要驗證**：AC-2 的既有案例與實跑記帳提交重判，先於 AC-3 統計與文件定稿
- **選擇理由**：直接量測一般記帳會不會被誤判
- **完成證據**：測試輸出與重判結果

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | review-8d4f21a MUST FIX 1 `需決策`：錯誤訊息沒有指出是哪一段，要補上段落內容，還是把 AC-1 改成只指出章節 | 已確認：2026-11-12 使用者選「訊息加上段落內容」，AC-1 不變 | AC-1 |
| TBD-2 | review-8d4f21a SHOULD FIX 1 `需決策`：被審查版本已是表格直接接凍結段落時，縮減表頭能藏住段落裡 `|` 之後的文字，要修還是列為已知限制 | 已確認：2026-11-12 使用者選「修」，這種排法沒有明確違反撰寫規範 | AC-1 |

## 實作與驗證步驟

1. ✅ **AC-1、AC-2：檢查器與測試** — 先寫紅燈案例，再實作；跑五項檢查並重判實跑留下的記帳提交
   - 完成證據：2026-11-12。
     - 紅燈：[s1-red.txt](evidence/s1-red.txt)，新增的 `test_blank_line_before_frozen_paragraph_compared` 3 個子案例（刪空行、補空行、範本檔尾刪空行）都判 OK 而失敗；`test_row_appended_before_template_footer_valid` 通過（行為本來就對，作為不變的保障）。
     - 實作：`analyse()` 記下段落開始時前接的是檔頭、標題、空行還是表格列，含凍結內容的段落在結尾之後加一項 `start`；排在段落內容與結尾之後，內容或結尾不同時錯誤訊息仍先指出它們。第一版把 `start` 排在最前面，35 個既有子案例因錯誤訊息改指 `start` 而失敗，調整順序後全部通過。
     - 綠燈：[s1-green.txt](evidence/s1-green.txt)，252 項通過（新增 2 個測試方法，四個測試類別各繼承一次）。check-kit、check-links、`bash -n`、test-install（14）OK。
     - AC-2 重判：本分支的 `verify-artifact.py` 對 issue #4 的 wf28b3（`--reviewed 84a544b`）與 issue #3 最後一輪的 wf31（`--reviewed b2bfb79`）保留的 fixture 都判 OK，變更區段與先前相同。
     - 依 [review-8d4f21a](review-8d4f21a.md) 修正（2026-11-12，TBD-1、TBD-2）：紅燈 [s3-red.txt](evidence/s3-red.txt)，錯誤訊息沒有指出是哪一段、表格直接接凍結段落時縮減表頭判 OK，2 個測試失敗；實作後 `start` 項目帶出該段觸發凍結的行，前接表格列時一併凍結表頭與分隔列；綠燈 [s3-green.txt](evidence/s3-green.txt) 260 項通過。修正後重判的命令與輸出存在 [s1-rejudge.md](evidence/s1-rejudge.md)，兩個都仍 OK。
2. ✅ **AC-3：下游統計** — 擴充 `scan_downstream.py` 或另寫唯讀統計，記錄數量（相依：1）
   - 完成證據：2026-11-12 以 [scan_start.py](evidence/scan_start.py) 讀 issue #3 同一份 README 清單，結果在 [s2-scan.txt](evidence/s2-scan.txt)：不重複的 683 份中，含凍結內容的段落前接空行 402 份 477 段、前接標題 6 份 6 段、前接表格列 1 份 1 段。這 1 份是 Timeline 表格後面直接接檔尾欄位（沒有 `---`），檔尾欄位在 GFM 已經渲染成表格列；之後在那裡補空行、或修改那張表格的表頭，會判需重審。修正後重跑，數字不變。
3. ⏳ **收尾** — review-evidence.md、CHANGELOG 4.10.0、rule-verification-status；送獨立審查（相依：2）
   - 完成證據：2026-11-12 已更新 review-evidence.md「審查之後的提交」、CHANGELOG 4.10.0（變更、已知限制改寫、252 項）、rule-verification-status。獨立審查 [review-8d4f21a](review-8d4f21a.md) RETURN（MUST FIX 1、SHOULD FIX 2、NICE TO HAVE 2），已全數修正，待差異覆審

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-12 | 建立；以 marked 與 micromark 重現 V3 | Claude Code |
| 2026-11-12 | 使用者核准 AC-1～AC-3 | 使用者 |
| 2026-11-12 | 獨立審查 review-8d4f21a RETURN；使用者決定錯誤訊息加上段落內容、表格直接接凍結段落時凍結表頭（TBD-1、TBD-2） | 使用者／Claude Code |

---
**建立日期**: 2026-11-12  
**分級**: Small  
**風險**: Medium\
**狀態**: 實作中
