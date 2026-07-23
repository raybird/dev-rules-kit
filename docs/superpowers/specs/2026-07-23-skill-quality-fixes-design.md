# Skill 品質修正設計

**日期**：2026-07-23
**狀態**：已實作

## 背景

依 `writing-great-skills` 的可預測性原則檢視現有 skills 後，本次修正六項會影響契約安全、文件一致性、任務完成判定或輸出可信度的問題：

1. `code-simplify` 的強制簡化規則可能破壞公開契約。
2. `new-issue` 引用的 `docs/AGENTS.md` 分級規則、README 範本與 Agent 工作時序互相衝突。
3. `execute-task` 完成後沒有更新權威任務狀態。
4. `decompose` 的 Task 缺少完成判準、驗證方式與完整覆蓋檢查。
5. `git-squash` 將動態訊息直接放進 Shell 雙引號，可能發生非預期展開。
6. `create-pr` 要求輸出無法由現有資料來源證實的背景、決策與測試結果。

## 設計原則

- 採局部改寫，不全面重寫 skills，也不變更未選取的既有行為。
- 每個流程明確區分輸入證據、執行動作、完成 gate 與輸出。
- `docs/AGENTS.md` 是 issue 文件分級、格式與維護方式的單一真相來源。
- 無法取得證據時明確標示未知、未執行或阻塞，不以合理推測補齊。
- 公開行為與契約安全優先於簡化幅度。

## 行為設計

### code-simplify

將「行為與契約不變」設為所有簡化規則的最高優先 gate。只有同時確認下列條件時，才能移除抽象、參數或泛型：

- 不屬於公開 API 或跨模組契約。
- 不參與 DI、反射、序列化、override 或 callback 簽章。
- 沒有仍在使用的引用。
- 可透過專案既有驗證證明行為不變。

找不到可證明安全且能提升清晰度的簡化時，允許保持原狀並說明原因。

### docs/AGENTS.md 與 new-issue

`docs/AGENTS.md` 的 README 範本與 Agent 工作時序依分級分流：

- Small：只建立 `README.md`。
- Medium：建立 `README.md` 與 `implementation-plan.md`；README 只連結實際存在的文件。
- Large：建立完整四件套。

`new-issue` 不再重述完整分級表、模板欄位與風險決策細節，只負責：

1. 驗證 issue ID 與核心目標等必要輸入。
2. 讀取 `docs/AGENTS.md` 的權威規範。
3. 分別判定規模與風險。
4. 建立該分級要求的文件。
5. 核對實際文件集合、metadata、任務清單與驗證證據符合權威規範。

### execute-task

完成指定步驟或 Task 前，必須確認其完成判準全部成立並執行所有適用驗證。成功後直接更新：

- 原任務清單中的完成狀態。
- 原任務項目的驗證證據。
- README Timeline。
- 受本次實作影響文件的 Changelog。

不再建立未指定檔名的獨立實作報告，也不在 issue 文件複製完整程式碼。對話輸出只保留摘要、修改檔案、驗證證據與文件更新結果。任一完成判準或必要驗證未通過時，不得標記 Task 完成。

### decompose

每個 Task 必須包含：

- 任務說明。
- 預期產出。
- 相關檔案或模組。
- 可觀察的完成判準。
- 可重複執行的驗證方式。

輸出前執行完整覆蓋 gate：Implementation Plan 中的需求、交付成果與風險證據都必須映射到明確 Task；不得有未映射項目，也不得由多個 Task 承擔同一責任而沒有清楚邊界。

### git-squash

保留三個獨立 code block 與 `git commit -m` 輸出形式。所有動態 Shell 參數使用 POSIX shell 單引號引用；遇到參數內容中的單引號時，先結束引用、以反斜線引用該字元，再重新開始引用，例如 `foo'bar` 轉成 `'foo'\''bar'`。這可避免 `$()`、backtick、變數與雙引號發生 Shell 展開。

輸出前必須檢查分支名稱、subject 與 body 均已安全引用。說明文字只宣告兩個 `-m` 分別承載 subject 與 body，不再把它描述成保留 `#` 的必要手段。

### create-pr

產生 PR 內容前蒐集：

- 指定 commit 範圍與 commit 訊息。
- 該範圍的淨 diff 與檔案清單。
- 可取得的 issue、需求或任務文件。
- 實際執行的測試與驗證紀錄。

Why、How、變更清單與測試敘述都必須可追溯至上述來源。沒有測試證據時，保留測試區塊並明列未執行項目、原因與殘餘風險；不得產生測試場景占位符或暗示已通過。選用區塊沒有實質內容時直接省略。

## 修改範圍

直接修改：

- `docs/AGENTS.md`
- `skills/code-simplify/SKILL.md`
- `skills/new-issue/SKILL.md`
- `skills/execute-task/SKILL.md`
- `skills/decompose/SKILL.md`
- `skills/git-squash/SKILL.md`
- `skills/create-pr/SKILL.md`

由同步腳本產生：

- 上述六個 skill 對應的 `workflows/shared/*.md`

不主動修改 `docs/usage.md`、未選取的 skill 或歷史 spec／plan。若驗證發現這些文件因本次契約變更而產生直接矛盾，應先回報，不擴張修改範圍。

## 驗證與完成條件

1. 執行 `python3 scripts/sync-skills.py`，不得手動修改配對 workflow。
2. 執行 `python3 scripts/sync-skills.py --check` 並取得成功結果。
3. 所有 `SKILL.md` frontmatter 仍只有 `description`，且 `workflows/README.md` 描述與 description 第一句一致。
4. Small、Medium、Large 的文件集合、README 連結與 Agent 工作時序一致。
5. 六項問題都有明確、可檢查的完成 gate，不依賴主觀宣稱。
6. 人工確認 Shell 範例中的所有動態值均使用安全單引號引用，並涵蓋內容含單引號的處理方式。
7. 不宣稱執行本 repo 不存在的 build、test 或 lint。

## 非目標

- 不處理本次未選取的 `dev-cycle`、`review` 或 `create-commit` 問題。
- 不重新設計全部 issue 開發閉環。
- 不新增執行期程式碼、自動化測試框架或平台特定 workflow。
