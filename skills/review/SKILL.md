---
name: review
description: 由獨立 reviewer 審查變更或不修復決策，核對驗收、測試、風險與架構並持久化報告；PR 審查或指定 diff review 時使用。
---

> 本 skill 需要 `docs/AGENTS.md` **流程契約 2.0**；相容性依該檔「核心層齊備性檢查」。

## 輸入與範圍

讀 agents/project.md、acceptance.md、verification.md、review-evidence.md。由協調者傳入固定 BASE／HEAD；獨立呼叫依 review-evidence.md 取得範圍。相容 COMMIT_COUNT，但局部審查不自動代表整個 PR。需求不足時標明推斷來源，不能補造核准。

## 審查

1. 取得固定範圍的完整 diff、異動清單、核准規格與測試證據。產生檔可簡述來源；lockfile 涉依賴或供應鏈變更時仍查核，不能一律排除。
2. Superpowers requesting-code-review 可用時使用；否則派給宿主獨立 subagent／task，傳入同一組範圍、規格與證據。原實作者不兼任獨立 reviewer；能力缺漏或豁免依 review-evidence.md 回報。
3. 核對規格修訂與核准來源、完整驗收覆蓋、正確性、相關安全／權限／依賴失敗面、架構邊界與測試真偽。依風險提出具體邊界案例，各重要失敗面都有覆蓋結論，無固定數量。
4. 區分 MUST FIX 與改善建議；依 verification.md 將證據持久力、限制揭露與假綠燈分開判定。待確認事項維持原狀態，覆核其交付影響；豁免只適用紀錄明列項目。
5. 依 review-evidence.md 保存完整報告，並檢查被審查版本與 artifact 有效性。本機報告可由協調者新增只含該報告的提交，通過「本機 artifact 提交後的有效性」全部檢查才沿用原 PASS。執行本 skill 目錄下的 `scripts/verify-artifact.py --repo <專案> --reviewed <SHA> --head <SHA> --artifact <repo-relative 路徑>` 驗證提交例外；指令為唯讀，成功只代表版本有效，審查結論仍須讀報告。

不修復／等待窗口時改審查其決策與當下可完成工作，不要求尚未到期的外部結果，也不輸出程式驗收 PASS。

## 報告

```markdown
# 審查報告
- 範圍：完整 PR／局部 diff／決策審查
- Reviewed BASE SHA：...
- Reviewed HEAD SHA：...
- Reviewed patch-id：...（無程式 diff 的決策審查可記不適用與理由）
- 獨立 reviewer：...
- Review artifact：...

## 問題與風險
- MUST FIX／SHOULD FIX／NICE TO HAVE：具體位置、影響與建議；無則寫無

## 已查核維度
- 驗收與證據：編號、證據位置及結論
- 相關失敗面：輸入／狀態、預期、現有覆蓋與判定
- 需求、架構、安全、品質：結論；不適用則寫理由
- 豁免、待確認與限制：有則揭露

## 流程判定
PASS／RETURN TO execute-task／UNPERSISTED（依 review-evidence.md）
```

只有報告已持久化、獨立審查有效、必要維度查核完整且沒有 MUST FIX 才可 PASS。輸出報告連結與主要發現；路徑使用 repo-relative，位置附行號。
