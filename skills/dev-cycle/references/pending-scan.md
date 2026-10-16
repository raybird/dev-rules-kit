# 懸置掃描

dev-cycle 在查狀態而未指定 issue 時讀本檔。本檔定義偵測規則、專案掃描命令的輸出格式與回報版面；全程唯讀，不改文件、狀態或 Git。

## 輸入

從 project.md 取得（未登記者照括號內處理）：

- **issue 目錄**（預設 `docs/issues/`）。
- **掃描起點**：issue 編號或日期（未登記則全部展開）。起點前的 issue 依平台狀態處理：`closed` 只計入總數；`open` 照常判定；`unknown` 也只計數，但摘要另列其筆數並說明登記平台查詢後才能區分仍 open 者。
- **掃描命令**：專案提供的唯讀命令，輸出下方 JSON（未登記則由 agent 依本檔規則逐一讀 README 取得同樣事實，並在摘要註明「agent 掃描」）。
- **平台 issue 查詢命令**：須含已關閉的 issue（未登記則平台狀態一律為 `unknown`，摘要註明無法區分）。
- **合併判定方式**（未登記時依序：平台 PR／MR 的 merged 狀態 → Git merge commit，後者標「推測」）。合併的提交只改 issue 目錄內的計畫、進度或證據紀錄時，不足以證明已交付；核准產出本身是文件時，該文件的變更即為交付。

## 偵測規則

每個 issue 依下列規則判定，一個 issue 可命中多類；沒有命中任何一類的 issue（包括正常進行中的 issue）不列出：

| 類型 | 條件 |
|---|---|
| 缺少狀態欄 | README 沒有 `**狀態**` 欄 |
| 已合併未結案 | 狀態不是 `已完成`／`不修復`，但依合併判定已合併 |
| 窗口到期 | `等待外部驗收窗` 的日期已過或事件已發生；無法判斷事件時照列並註明 |
| 結案後仍有待觀察 | `已完成`，但驗證表、Proof 表或任務清單中有未豁免的 AC／SCN 為 `未執行`，或步驟仍為 📝／⏳ |
| 待確認未結 | 待確認事項為 `待確認` |
| 缺追蹤 | 待確認事項為 `不影響本次交付`，結論沒有「追蹤：」 |
| 平台已關閉、README 未結案 | 平台 closed，狀態不是 `已完成`／`不修復` |
| README 終態、平台仍 open | 狀態為 `已完成`／`不修復`，平台 open |
| 平台 open、沒有 README | 平台 open，issue 目錄沒有對應文件 |

「未執行」只看帶驗收編號（AC／SCN）的列；限制揭露、敘述文字與非交付腳本不算。豁免以 README `## Gate 豁免紀錄` 明列者為準。

## 掃描命令輸出格式

```json
{
  "scanned": 262,
  "scope_start": "issue-0300",
  "platform": "available",
  "merge_basis": "GitLab MR merged",
  "issues": [
    {
      "id": "0330",
      "readme": "docs/issues/issue-0330/README.md",
      "status_raw": "待真人驗收",
      "platform_state": "open",
      "merged": "true",
      "merged_basis": "!412 merged 2026-10-02",
      "unexecuted": [{"ref": "SCN-004", "location": "README.md:281", "waived": false}],
      "open_steps": [{"step": "5", "symbol": "📝", "location": "implementation-plan.md:140"}],
      "tbd": [{"id": "TBD-2", "status": "不影響本次交付", "tracking": null, "location": "README.md:61"}],
      "window": {"kind": "event", "text": "下一次正式發版", "reached": "unknown"}
    }
  ],
  "platform_only": [{"id": "0398", "title": "…", "state": "open"}]
}
```

- `merged`、`reached` 為 `"true"`、`"false"`、`"inferred"`（僅 `merged`）或 `"unknown"`；`platform_state` 為 `open`、`closed`、`unknown`。
- 欄位缺漏視為 `unknown`；agent 依偵測規則分類，不改寫命令輸出的事實。命令失敗或格式不符時回報錯誤並改走 agent 掃描。

## 回報版面

1. 一行摘要：掃描數、起點、平台資料有無、合併判定依據、掃描方式（命令／agent）；起點前有平台狀態 `unknown` 的 issue 時，附「起點前 N 個平台狀態未知，未判定」。
2. 依「平台 open 或 unknown」→「平台已關閉」分兩段，各段再依類型分組並附筆數。
3. 每項列 issue、類型、狀態原文（前 30 字）、依據位置、建議下一步，並標「使用者決定」或「可補紀錄」。窗口類依日期排序，其餘依 issue 編號。
4. 起點前只計數的 issue 分 `closed`、`unknown` 兩組，各附筆數與最常見的狀態原文；需要時建議另開一次性校正 issue。

全部範圍內的 issue 都判定過才算完成。沒有項目時，整則回覆只有一行：已檢查的 issue 數與「沒有懸置項目」。
