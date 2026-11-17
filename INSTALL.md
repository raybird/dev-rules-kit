# dev-rules-kit 安裝與更新指引（給 AI agent）

本檔寫給 AI agent 照步驟執行。使用者只需要對 agent 說：

> 請依照 https://github.com/raybird/dev-rules-kit/blob/main/INSTALL.md 安裝 dev-rules-kit，並初始化目前這個專案。

## 執行原則

- 有 `--dry-run` 的指令先跑 dry-run；手動複製或編輯檔案前先列出要動的檔案。把會新增、更新或覆蓋的內容告訴使用者，確認後才正式執行。
- 腳本回報衝突或停止時，照實回報給使用者並停在該步；由使用者決定後續，保留腳本的保護機制。
- 每一步達到完成判準才進下一步。
- 以下 `<kit>` 代表 kit 的本機路徑，`<project>` 代表要初始化的專案根目錄。下載安裝需要 `curl`、`tar`、`bash`、`python3`；clone 需要 `git`、`bash`、`python3`。

## 1. 選擇安裝方式

兩種方式裝出來的技能相同，依序判斷：

- 使用者指定了方式或 kit 位置：照使用者的。
- `~/.local/share/dev-rules-kit/current` 已存在：**下載安裝**，`<kit>` 是該路徑。
- `~/Tools/dev-rules-kit` 已存在：**clone**，在該處執行 `git pull --ff-only`。
- 都沒有：說明兩種方式，問使用者選哪一種。下載安裝不需 clone，重跑同一行指令就是更新；clone 適合要看 Git 歷史或維護 kit 的人。clone 時執行 `git clone https://github.com/raybird/dev-rules-kit.git ~/Tools/dev-rules-kit`。

完成判準：已決定方式。clone 時 `python3 <kit>/scripts/check-kit.py` 輸出 `OK`，並記下 `git -C <kit> describe --tags --dirty` 的版本（結尾 `-dirty` 代表 kit 有未提交的修改，回報時一併說明）。下載安裝的 kit 在第 2 步下載。

## 2. 安裝技能

1. 先跑 dry-run：下載安裝用 `curl -fsSL https://raw.githubusercontent.com/raybird/dev-rules-kit/main/scripts/get.sh | bash -s -- --dry-run`，clone 用 `bash <kit>/scripts/install.sh --dry-run`。告訴使用者會裝哪一版（下載安裝的第一行）與偵測到哪些平台。沒偵測到時，用 `bash <kit>/scripts/install.sh --list`（下載安裝尚未有 `<kit>` 時改看 `<kit>/skills/README.md` 的安裝表格）查路徑，問使用者要裝哪個平台，之後兩種方式都在參數加上平台名稱。
2. dry-run 輸出中的「會備份 <技能>（本地修改：…）」是平台上被改過、內容不屬於任何一版 kit 的同名技能，列給使用者確認。正式執行時腳本會把整個技能目錄備份到技能目錄之外（`<平台設定目錄>/skill-backups/`）再覆蓋；使用者不想覆蓋某個技能時停在本步，由使用者決定。
3. 使用者確認後去掉 `--dry-run` 執行：下載安裝為 `curl -fsSL https://raw.githubusercontent.com/raybird/dev-rules-kit/main/scripts/get.sh | bash`（完成後 `<kit>` 是 `~/.local/share/dev-rules-kit/current`），clone 為 `bash <kit>/scripts/install.sh`。

完成判準：每個目標平台的每個技能都與 kit 相同，`diff -rq <kit>/skills/<name> <平台技能目錄>/<name>` 沒有輸出；輸出中的每個「備份：」位置都已記下。安裝只新增與覆蓋檔案、不刪除舊檔，若只剩「Only in <平台技能目錄>」的多餘檔案，列給使用者決定是否刪除。

## 3. 初始化或更新專案文件

使用者要在某個專案使用 issue 流程（new-issue、dev-cycle 等）時執行；只安裝技能時略過本步並告知使用者。

- `<project>/docs/.dev-rules-kit.json` 不存在：首次初始化，執行 `python3 <kit>/scripts/init-project.py <project> --dry-run`，確認後去掉 `--dry-run`。
- 已存在：更新，執行 `python3 <kit>/scripts/init-project.py <project> --update --dry-run`，確認後去掉 `--dry-run`。
- 腳本因本地修改、缺少基線或路徑衝突而整批停止時，把它列出的檔案回報給使用者並停在本步。舊版專案首次遷移依 `<kit>/docs/AGENTS.md` 的「客製邊界與同步策略」，由使用者決定如何合併。

完成判準：`python3 <kit>/scripts/init-project.py <project> --check` 輸出 `OK`。專案是 Git repo 時，告訴使用者異動的檔案；要提交到哪個分支由使用者決定。

`docs/agents/project.md` 是專案自己的客製檔，初始化只在不存在時建立、更新時保留；提醒使用者可在其中記錄測試命令、專案邊界、已知地雷，以及合併、部署、平台狀態的查證命令（既有 project.md 更新時不會自動補上這項），agent 不需要為填表猜測內容。`--check` 印出「project.md 仍是初始化範本原文」時照實轉告，不算失敗；印出「落後本 kit」時執行 `--update`，印出「衝突」才需要人工合併。

## 4. 通用規則（選用，先問使用者）

規則檔是 agent 的通用行為原則（`<kit>/rules/AGENTS.zh-TW.md`，英文版為 `AGENTS.md`）。先問使用者要不要裝、裝全域還是專案層；各平台位置見 `<kit>/rules/README.md` 的「安裝方式」。

- **全域（Codex、OpenCode、Antigravity）**：`bash <kit>/scripts/install.sh --with-rules --dry-run`。目標檔已存在且內容不同時，腳本會備份後覆蓋；檔案裡有使用者自己加的章節時先告知，由使用者選擇整份覆蓋或只合併變動的段落。
- **Claude Code**：把規則檔複製為 `<project>/AGENTS.md`。專案已有 `CLAUDE.md` 時，在它開頭加一行獨立的 `@AGENTS.md`（不包在反引號或程式碼區塊內），否則 Claude Code 不會讀 `AGENTS.md`；沒有 `CLAUDE.md` 時不必新建。
- **Cursor**：沒有檔案層級的全域規則，請使用者在 Settings → Rules → User Rules 貼上內容。
- **已有規則副本時（首次安裝與更新都要檢查）**：找出專案或全域已有的規則副本，包括專案根的 `AGENTS.md`、`CLAUDE.md` 用 `@` 引用的檔案，以及直接內嵌在 `CLAUDE.md` 的規則段落。把與 kit 目前版本不同的段落列給使用者，由使用者決定是否同步；新舊兩份同時載入會互相矛盾時特別指出。`init-project.py` 不處理這些副本。

完成判準：使用者選擇的每個位置都已安裝或同步，或使用者明確表示不需要。只完成一部分時（例如複製了 `AGENTS.md` 但使用者不讓改 `CLAUDE.md`），回報規則尚未生效以及還缺哪一步。

## 5. 回報

用一段簡短回報列出：

- 安裝方式、kit 路徑與版本（clone 用 `git describe --tags --dirty`，下載安裝用 `readlink ~/.local/share/dev-rules-kit/current`）；更新時列出新舊版本之間 `<kit>/CHANGELOG.md` 的重點，Major 版本特別標出。
- 已安裝技能的平台，以及安裝輸出列出的技能備份位置。
- 專案初始化或更新的結果與異動檔案，或略過的原因。
- 規則檔的處理結果。
- 尚未完成、需要使用者決定的事項。

最後提醒使用者：新開的 agent session 才會載入新版技能；日常用法見 `<kit>/README.md` 的「日常怎麼用」。
