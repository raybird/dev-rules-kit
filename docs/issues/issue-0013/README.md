# Issue 13 - 下游部署內容瘦身 (Small)

## 概述

來源：[GitHub #13](https://github.com/raybird/dev-rules-kit/issues/13)。2026-11-20 下游調查中，一個沒有使用 kit issue 流程的專案回報，它的 issue 只在平台上追蹤，沒有 docs/issues。初始化後，部署下來的內容大多沒有資訊量：

1. **不用 issue 流程也整套部署**：docs/agents/ 底下的 acceptance、document-types、issue-checklist、readme-templates、review-evidence、verification 共約 570 行，該專案從沒建過 issue 目錄。人打開 docs/ 會以為要照做，而且版本會落後。INSTALL.md 第 3 步雖然寫了「使用 issue 流程時才執行」，但只想用 project.md 的專案沒有別的做法。create-commit 與 project-worktrees 會讀 project.md，不讀核心文件。
2. **下游 docs/AGENTS.md 帶著 kit 自己的修訂紀錄**：檔尾的修訂紀錄有 16 列、約 6.4KB，記的是 kit 的設計歷程，內容與 kit 的 CHANGELOG 重複。沒有腳本或技能讀取這張表，check-kit 只讀 `**流程契約**` 那一行。
3. **project.md 範本開頭的管理說明**：第一句「本檔由專案維護，初始化只在不存在時建立，更新上游時保留」講的是 kit 怎麼管理這個檔，docs/AGENTS.md「客製邊界與同步策略」已經寫過。第二句「規劃與交付前讀取；未填內容從 repo 的設定、現有文件與命令取得，不為填表猜測」是給 agent 的行為指示。

本 issue 只改部署內容與文字，不改變 agent 的 issue 流程行為，流程契約維持 2.7。

## 涉及檔案

- `docs/AGENTS.md` - 移除檔尾修訂紀錄表，改成一行指向 kit CHANGELOG；文件版本 2.15 → 2.16
- `docs/agents/project.md` - 刪掉開頭第一句
- `scripts/init-project.py` - `PAST_TEMPLATES` 加入修改前的範本雜湊
- `INSTALL.md` - 第 3 步補上不用 issue 流程時只建立 project.md 的做法，以及已整套部署的專案可以移除哪些檔
- `CHANGELOG.md`、`docs/rule-verification-status.md`

## 驗收條件

1. **AC-1**：`docs/AGENTS.md` 檔尾的修訂紀錄表移除。保留 `**文件版本**`（改為 2.16）、`**流程契約**`（2.7 不變）與 `**最後更新**` 三行，另加一行說明各版異動見 kit 的 CHANGELOG，附 GitHub 網址，因為下游 repo 用相對連結找不到。舊紀錄留在 Git 歷史與 CHANGELOG。 — 檢查方式：check-kit 讀得到流程契約並通過；check-links 通過；`grep -n '修訂紀錄' docs/AGENTS.md` 沒有輸出；暫存專案先以 main 的 kit 初始化，再用本分支執行 `--update`：docs/AGENTS.md 被更新、沒有衝突，之後 `--check` 輸出 OK
   - 失敗路徑：check-kit 讀不到流程契約，或未客製的下游執行 `--update` 時判衝突
2. **AC-2**：`docs/agents/project.md` 範本刪掉第一句，保留第二句；修改前的範本雜湊加入 `init-project.py` 的 `PAST_TEMPLATES`。 — 檢查方式：test-install 的歷代範本雜湊測試通過；暫存專案以 main 的 kit 初始化（project.md 是舊範本原文）後，用本分支執行 `--update` 與 `--check`：project.md 保持原樣，仍印出「project.md 仍是初始化範本原文」
   - 失敗路徑：舊範本原文的 project.md 不再被認出，或 `--update` 改到既有 project.md
3. **AC-3**：INSTALL.md 第 3 步補上兩件事。
   - 不用 issue 流程、但要讓 create-commit 與 project-worktrees 讀到專案慣例時：只在 `<project>/docs/agents/project.md` 不存在時，複製 `<kit>/docs/agents/project.md`，不執行 init-project。之後要用 issue 流程，照常執行 init-project，既有 project.md 會保留。
   - 專案已整套部署、確定不用 issue 流程時，可以移除 `docs/AGENTS.md`、`docs/agents/` 底下 project.md 以外的檔案，以及 `docs/.dev-rules-kit.json`。前提是 `docs/issues/` 不存在或沒有 issue 目錄；有的話不移除，並先告知使用者。是否移除由使用者決定。
   — 檢查方式：靜態核對文字；暫存專案照 INSTALL.md 的輕量步驟只建立 project.md，之後執行 `init-project.py --dry-run`，輸出「既有 project.md 保持原樣」，正式執行後 `--check` 輸出 OK
   - 失敗路徑：輕量步驟會覆蓋既有 project.md；移除說明沒有寫出「有 issue 目錄時不移除」的前提；之後補完整初始化時判衝突
4. **AC-4**：agent 的 issue 流程行為不變：skills/ 與 rules/ 不動，流程契約維持 2.7。 — 檢查方式：`git diff --stat main` 不含 skills/、rules/；五項檢查通過
   - 失敗路徑：skills/ 或 rules/ 有變更，或流程契約改變

- **核准日期**: 待核准
- **核准來源**: 2026-11-23 使用者在逐題確認中選擇：輕量模式選「INSTALL.md 說明，不改安裝器（建議）」；修訂紀錄選「只留版本行加 CHANGELOG 連結（建議）」；project.md 選「刪第一句，留第二句（建議）」。AC-1～AC-4 的細節（版本號、移除清單與前提、驗證方式）待核准
- **核准 commit**: 待提交

## 風險與首要驗證

- **最大風險**：INSTALL.md 是給 agent 照著執行的。移除說明寫得不嚴，agent 可能在有使用 issue 流程的專案刪掉核心文件；輕量步驟寫得不嚴，可能覆蓋既有 project.md
- **風險等級與理由**：Medium。刪檔與覆蓋都發生在下游 repo，雖然都在 Git 裡可以復原，但會讓 issue 流程失去核心文件
- **首要驗證**：AC-3 的暫存專案驗證，加上核對移除說明的前提條件寫在步驟本身，不只寫在註解
- **選擇理由**：直接檢查最容易造成下游損失的兩個動作
- **完成證據**：暫存專案的命令輸出與 INSTALL.md 的對應段落

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | INSTALL.md 的輕量步驟算不算改變 agent 行為、要不要在發布前於下游試用 | 待確認 | 決定發版前是否需要下游試用；AC-3 |

## 實作與驗證步驟

1. 📝 **AC-1：移除修訂紀錄** — 驗證方式：同 AC-1 的檢查方式
   - 完成證據：執行時回寫
2. 📝 **AC-2：project.md 範本與 PAST_TEMPLATES** — 驗證方式：同 AC-2 的檢查方式
   - 完成證據：執行時回寫
3. 📝 **AC-3：INSTALL.md 輕量步驟與移除說明** — 驗證方式：同 AC-3 的檢查方式
   - 完成證據：執行時回寫
4. 📝 **AC-4：CHANGELOG、rule-verification-status 與整體檢查** — 驗證方式：同 AC-4 的檢查方式
   - 完成證據：執行時回寫

## Timeline

| 日期 | 異動 |
|------|------|
| 2026-11-23 | 建立 |

---
**建立日期**: 2026-11-23  
**分級**: Small  
**風險**: Medium\
**狀態**: 待核准
