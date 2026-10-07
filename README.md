# dev-rules-kit

讓 AI coding agent 照一套可驗證的流程做事：先把需求講清楚、用真實測試證明完成、交給獨立 reviewer 審查，每一步都留下證據。支援 **Codex**、**Claude Code**、**OpenCode**、**Antigravity**、**Cursor**。

## 它能幫你做什麼

- **需求先講清楚**：一句話的需求會被整理成可核准的驗收條件；agent 只問會影響結果的問題，一次一題並附建議答案，回「照建議」就能往下走；你已經說清楚的不會重問。
- **「做完了」要有證據**：行為變更先有失敗的測試、再修到通過，沒有真實測試輸出不能標成完成。
- **獨立審查**：由沒參與實作的 reviewer 審 PR，報告存檔，沒有獨立 reviewer 能力時如實回報，不假裝通過。
- **跨 session 接續**：進度記在 issue 文件與 Git，下次說「繼續 issue 101」就從停下的地方往下做。
- **小事不走流程**：一般修改直接做，只有需要追蹤的 issue 才走完整流程；趕時間可以明說豁免，agent 會照做並留下紀錄。
- **更新不蓋掉客製**：專案自己的設定放在 `docs/agents/project.md`，更新 kit 時保留。

## 快速開始

### 讓 AI agent 幫你裝（推薦）

在要使用的專案裡打開 agent，貼上：

```text
請依照 https://github.com/raybird/dev-rules-kit/blob/main/INSTALL.md 安裝 dev-rules-kit，並初始化目前這個專案。
```

agent 會照 [INSTALL.md](INSTALL.md) 取得 kit、安裝技能、初始化專案文件，每一步先給你看 dry-run 結果再執行。agent 無法連網時，先自己 clone 到 `~/Tools/dev-rules-kit`，再請它讀該目錄下的 `INSTALL.md`。

### 手動安裝

需要 `git`、`bash`、`python3`：

```bash
git clone https://github.com/raybird/dev-rules-kit.git ~/Tools/dev-rules-kit
bash ~/Tools/dev-rules-kit/scripts/install.sh                          # 安裝技能到偵測到的平台
python3 ~/Tools/dev-rules-kit/scripts/init-project.py /path/to/project  # 初始化專案文件
```

兩個指令都可以先加 `--dry-run` 看會做什麼。通用行為規則是選用的，安裝方式見 [rules/README.md](rules/README.md#安裝方式)。

## 日常怎麼用

安裝後新開一個 agent session，直接用對話驅動：

| 你想做的事 | 對 agent 說 |
|---|---|
| 開一個新需求 | `/new-issue issue:101 主題:修正空字串驗證 內容:空字串應顯示必填錯誤` |
| 讓它自動往下做 | `/dev-cycle 101` 或「繼續處理 issue 101」 |
| 只查進度（不會動任何檔案） | 「issue 101 到哪了」 |
| 審查目前的變更 | `/review` |
| 回答 agent 的提問 | 「照建議」，或「一起問」一次看完所有獨立的題目 |
| 這次想快一點 | 「這次不用寫 Gherkin」「不用先寫測試」 |

`dev-cycle` 會串起完整流程，遇到需要你決定的事、等待合併或外部驗收時停下回報：

```text
new-issue → decompose（Large 才需要）
          → execute-task（測試、實作、精煉）
          → create-commit → create-pr → review
                                          └─ 退回時回到 execute-task 修正後重審
```

每個技能都能單獨使用。完整示範與各技能說明見 [使用指南](docs/usage.md)。

## 更新

對 agent 說「請依照 INSTALL.md 更新 dev-rules-kit」即可；它會拉新版、更新技能與專案文件，並整理 [CHANGELOG](CHANGELOG.md) 的重點。手動更新：

```bash
git -C ~/Tools/dev-rules-kit pull
bash ~/Tools/dev-rules-kit/scripts/install.sh
python3 ~/Tools/dev-rules-kit/scripts/init-project.py /path/to/project --update
```

更新只覆蓋沒被你改過的核心文件；有本地修改時整批停止並列出衝突，不會部分寫入。已複製到專案或全域的規則檔不在自動更新範圍，Major 版本請先看 CHANGELOG。

## 深入了解

| 想了解 | 看這裡 |
|---|---|
| 完整流程、查詢與等待、PR 與 review | [docs/usage.md](docs/usage.md) |
| 規則檔安裝、Claude Code 掛載方式 | [rules/README.md](rules/README.md) |
| 技能清單與各平台安裝路徑 | [skills/README.md](skills/README.md) |
| 搭配工具：推薦 Serena、GitNexus；Superpowers 選用（預設不使用） | [docs/setup/tools.md](docs/setup/tools.md) |
| 下游文件規範（分級、核准、驗證、審查） | [docs/AGENTS.md](docs/AGENTS.md) |
| 維護本 kit | [AGENTS.md](AGENTS.md) |

## 授權

MIT © Raybird
