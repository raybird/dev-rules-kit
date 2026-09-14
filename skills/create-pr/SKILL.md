---
name: create-pr
description: 依固定交付範圍與有效測試證據撰寫或更新 PR 說明；變更已提交、準備交付審查時使用。
---

> 本 skill 需要 `docs/AGENTS.md` **流程契約 2.0**；相容性依該檔「核心層齊備性檢查」。

## 輸入與證據

讀 agents/project.md、acceptance.md、verification.md 與 review-evidence.md。協調者傳入固定 BASE／HEAD；獨立使用時先查現有 PR／專案設定，範圍無法辨認才問。

1. 取得淨 diff、commit、核准規格與原任務證據，確認工作區沒有漏提交的交付內容。Why 來自需求或可辨認的提交意圖，How 與變更來自淨 diff；無來源的理由省略或標明缺少背景。
2. 依 acceptance.md 核對每項現存驗收已核准或有明列豁免；未核准的新行為先回規劃。
3. 依 review-evidence.md 逐驗收編號建立 Proof 表，引用固定版本規格與持久化測試證據。共享測試只保存一份；證據與交付內容、環境或時效不符才重跑。Superpowers verification-before-completion 可用時協助核對相同 gate。
4. 揭露 README 的豁免、待確認事項及交付影響；確認 project.md 觸發的常青文件已更新。

## 輸出格式

```markdown
## 變更
描述具體問題、改變後行為及必要的實作理由。

## 驗證
- 交付範圍：BASE..HEAD

| 驗收編號 | 結果摘要 | 固定版本規格 | 測試／等價證據 | 結果 |
|---|---|---|---|---|
| AC-1 | 可觀察行為 | commit:path 與編號，或永久連結 | 命令／輸出紀錄連結 | PASS／未執行 |

## 限制與待確認
有豁免或未解決事項時列原狀態、原因與殘餘影響；無則省略。
```

只有核准集合、Proof 集合、實際交付範圍與有效證據一致，才視為可交付說明。未執行項目照實記錄；缺少必要證據且未豁免時保留為草稿並回報缺項，不宣稱可驗收。

單獨要求撰寫時輸出可複製 Markdown；使用者已要求建立／更新 PR 或 dev-cycle 推進已授權時，直接操作平台。不因切換 skill 重複詢問既有授權。
