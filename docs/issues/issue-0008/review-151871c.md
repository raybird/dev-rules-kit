# 審查報告
- 範圍：完整 PR（差異覆審，本輪只審 ee77c12..151871c，其餘沿用 review-ee77c12 的查核）
- Reviewed BASE SHA：c0c7e9f17cbc14a96bd8f28425b910a27be2d3f9
- Reviewed HEAD SHA：151871c1c0011e731eca31edb9476b1d3e4237a8
- Reviewed patch-id：a8d974ae5fcff75a084a307f9a8d50f97aae9963（以 `git diff c0c7e9f 151871c | git patch-id --stable` 重算，結果相同）
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0008/review-151871c.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE：無

## 已查核維度
- **驗收與證據**：
  - **CHANGELOG.md:37（SCN-005 的附帶步驟）**：新寫法是「把 document-types.md 換成本版 kit 的原文後執行 `--update`」。我在 scratchpad 重跑實測，路徑是 實作 session 的 scratchpad（review8b 子目錄），準備了兩種基線：
    - 舊基線：用 v4.12.0 之前的 ab1e901 初始化。
    - v4.12.0 基線：用 c0c7e9f 初始化，含 `_templates` 條目。

    兩者都先改寫 document-types.md。改寫後 `--update` 都判為衝突（rc=1）；照新步驟換成本版原文後，`--update` 回 0，`--check` 也回 0。
    - 括號裡的說明「換回舊版原文只在部署基線剛好是那一版時可行」，和上一輪實測的結果一致。
    - 這個步驟不受部署基線版本影響，正確可行。
  - **docs/usage.md:13**：刪掉「範本」之後，句子變成「核心規範、`docs/agents/project.md` 與部署基線」。這和 `scripts/init-project.py` 的實際部署內容一致：部署 `docs/AGENTS.md` 與 `docs/agents/*.md`，並寫入 `docs/.dev-rules-kit.json`。
    - usage.md 其他提到「範本」的地方：第 21 行的「project.md 仍是範本原文」指的是 project.md 初始化範本，第 88 行的「README 範本」連到 `agents/readme-templates.md`。兩處都正確，沒有同類殘留。
    - 全檔 grep `_templates` 沒有結果。
- **相關失敗面**：
  - 衝突處理步驟：兩種基線（v4.12.0、更舊版本）都已實測。
  - 其他核心檔也有本地修改的情況，原本就屬於既有的衝突規則（整批停止、人工合併），不在本條目範圍內。
  - 本輪沒有改腳本或測試，init-project.py 的各種舊基線形狀沿用 review-ee77c12 的實測結果。
- **記帳性質（本輪其他變更）**：
  - 28b2f59 只新增 review-ee77c12.md，並在 README `## 現況` 加上 `**現行 review**: review-ee77c12.md`。報告內容與上一輪交回的版本相符（SHA、兩項 SHOULD FIX、PASS 段）。
  - 151871c 改動 README 與 implementation-plan 共 9 行，內容如下：
    - README：TBD-4 一列、Timeline 兩列、狀態行。
    - implementation-plan.md：S5 的狀態欄。
  - Gherkin、核准紀錄、S1～S4 證據與 evidence 檔都沒有變動，沒有改到已審查的規格或證據。
  - 保存本報告時，`**現行 review**` 要改成 review-151871c.md。
- **根目錄五項檢查**（在 HEAD 151871c、工作樹乾淨的狀態下執行）：
  - check-kit：OK
  - check-links：OK
  - `bash -n scripts/install.sh`：OK
  - test-install：16 項 OK
  - test-evidence：296 項 OK
- **需求、架構、安全、品質**：兩處修正都是最小改動，沒有新增重複內容，也沒有過度設計。CHANGELOG 括號裡的說明解釋了為什麼不能換回舊版，對下游有用，不算贅述。

## 豁免、待確認與限制
- 無豁免。TBD-4 已由使用者決定，並照決定修正完成。TBD-3（發布前下游試用）在審查之後進行，不在本輪範圍。
- 工具呼叫用量：本輪 4 次，未超過 30 次上限，必查清單 1～4 項都已查完。
- 暫存專案都只建在 scratchpad，沒有碰任何真實下游專案。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
