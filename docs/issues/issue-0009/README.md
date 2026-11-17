# Issue 9 - 不需 clone 即可安裝與更新 kit

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #9](https://github.com/raybird/dev-rules-kit/issues/9)。目前要安裝或更新 kit，都得先 `git clone`，之後靠 `git pull` 更新。clone 不會自己更新：2026-11-03 查到本機另一份 clone 停在 v4.5.1、從來沒 fetch 過，2026-11-17 再查仍停在 v4.9.0；2026-11 的使用負擔調查也有專案用舊 clone 安裝。2026-11-17 維護者要求比照常見的 GitHub 開源工具，不 clone 也能安裝與更新。

連帶的兩個缺口：

1. INSTALL.md 第 2 步判斷「同名技能是不是 kit 版本」時，靠 `git rev-list` 查 kit 的 Git 歷史，沒有 clone 就做不了。`install.sh` 本身一律覆蓋，使用者改過的技能沒有保護。
2. 沒有指令可以查目前裝的是哪一版、有沒有新版。

收錄依據（AGENTS.md「範圍」）：下游實際用了沒更新的舊 clone 安裝。不涉及 plugin／marketplace 散布，`install.sh` 仍是唯一的安裝程式。

## 現況

| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |
|---|---|---|---|
| GitHub #9 | gh issue view 9 --json state -q .state | OPEN | 2026-11-17 |

## 快速導覽

### 當前流程

`git clone` → `bash <clone>/scripts/install.sh` 直接覆蓋各平台的同名技能 → `python3 <clone>/scripts/init-project.py`。更新要先在 clone 裡 `git pull`。

### 重構後流程

`curl -fsSL https://raw.githubusercontent.com/raybird/dev-rules-kit/main/scripts/get.sh | bash`：下載 release 壓縮檔，解壓到 `~/.local/share/dev-rules-kit/<版本>/`，再執行該版的 `install.sh`，成功後把 `current` 指向該版。`install.sh` 依歷代雜湊清單判斷同名技能：屬於某一版 kit 的直接覆蓋，不屬於任何一版的先備份再覆蓋。之後重跑同一行指令就是更新，`get.sh --check` 唯讀查版本。clone 的用法照舊。

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| 取得 kit | `git clone`，更新靠 `git pull` | 一行 `curl … get.sh \| bash`，重跑即更新；clone 仍可用 |
| kit 位置 | 使用者自選的 clone 目錄 | `~/.local/share/dev-rules-kit/<版本>/`，`current` 指向目前版本 |
| 同名技能 | `install.sh` 一律覆蓋；INSTALL.md 靠 Git 歷史人工判斷 | `install.sh` 依歷代雜湊清單判斷，使用者改過的先備份 |
| 查版本 | `git describe` | `get.sh --check` |

## 涉及檔案

### 安裝

- `scripts/get.sh` - 新增：解析版本、下載解壓、執行 install.sh、切換 `current`、`--check`
- `scripts/install.sh` - 覆蓋前依雜湊清單判斷並備份；`--check` 列出各平台技能的版本
- `scripts/skill-hashes.txt` - 新增：各技能檔歷代版本的 sha256 與所屬版本
- `scripts/build-skill-hashes.py` - 新增：從 Git 歷史產生雜湊清單
- `scripts/skill_state.py` - 新增：判斷平台技能屬於哪一版 kit 或本地修改，install.sh 與 check-kit 共用
- `scripts/check-kit.py` - 驗證目前每個技能檔的雜湊都在清單裡
- `.gitattributes` - 新增：`docs/issues/` 等維護紀錄不進壓縮檔

### 測試

- `scripts/test-install.py` - get.sh 與備份、`--check` 的案例（以本機壓縮檔與 `file://` 來源，不連網）

### 文件

- `README.md`、`README.en.md`、`INSTALL.md`、`docs/usage.md`、`skills/README.md`、`CHANGELOG.md`、`docs/rule-verification-status.md`；`rules/README.md` 檢查後不需要改

## Gherkin 驗收劇本

```gherkin
Feature: 不需 clone 即可安裝與更新 kit

  @SCN-001
  Scenario: 第一次用 get.sh 安裝
    Given 一個沒有 kit 的暫存 HOME，偵測得到至少一個平台
    When 執行 get.sh --version v{X}
    Then kit 解壓在 ~/.local/share/dev-rules-kit/v{X}/
    And current 指向 v{X}
    And 各平台的技能與該版 kit 的 skills/ 完全相同
    And 用 current 路徑執行 init-project.py 可以初始化專案

  @SCN-002
  Scenario: 重跑 get.sh 更新到新版
    Given 已用 get.sh 安裝舊版，技能檔都是某一版 kit 的原文
    When 以新版重跑 get.sh
    Then 各平台技能更新為新版，沒有產生備份
    And current 改指新版，舊版目錄保留

  @SCN-003
  Scenario: 使用者改過的技能先備份再覆蓋
    Given 某平台的一個技能檔內容不屬於任何一版 kit
    When 執行安裝或更新
    Then 該技能整個目錄先備份到技能目錄之外，再覆蓋成新版
    And 輸出列出備份位置
    And 內容屬於某一版 kit 的其他技能不備份

  @SCN-004
  Scenario: 指定版本與 dry-run
    Given 任一安裝狀態
    When 執行 get.sh --dry-run（可加 --version）
    Then 列出會下載的版本、會更新與會備份的技能
    And ~/.local/share/dev-rules-kit/ 與各平台技能目錄都沒有任何寫入

  @SCN-005
  Scenario: 檢查版本
    Given 已用 get.sh 安裝
    When 執行 get.sh --check
    Then 印出 current 的版本與最新 release 的版本
    And 列出各平台每個技能是哪一版 kit，或「本地修改」
    And 沒有任何寫入；取不到最新 release 時照實說明，其餘照常列出

  @SCN-006
  Scenario: 雜湊清單涵蓋目前版本
    Given kit 的 skills/ 有任一檔案被修改
    When 執行 check-kit.py，且清單沒有重新產生
    Then check-kit 失敗並指出缺少雜湊的檔案
    And 以 build-skill-hashes.py 重新產生後，check-kit 通過

  @SCN-007
  Scenario: clone 用戶直接執行 install.sh 也受保護
    Given 以 clone 的 kit 直接執行 install.sh，某平台有使用者改過的技能
    When 執行 install.sh
    Then 行為與 SCN-003 相同：先備份再覆蓋並列出備份位置

  @SCN-008
  Scenario: 壓縮檔不含維護紀錄
    Given 以 git archive 產生 release 壓縮檔
    When 檢視壓縮檔內容
    Then 不含 docs/issues/
    And 解壓後的 kit 照樣可以 check-kit、install.sh 與 init-project.py

  @SCN-009
  Scenario: 安裝文件並列 get.sh 與 clone 兩種方式
    Given 本 issue 的分支
    When 檢視 README.md、INSTALL.md、docs/usage.md
    Then 安裝與更新都並列 get.sh 與 clone 兩種方式，各自寫出 init-project.py 的路徑（get.sh 用 current）
    And 三份文件的指令一致

  @SCN-010
  Scenario: INSTALL.md 第 2 步改看 install.sh 列出的備份
    Given 本 issue 的分支
    When 檢視 INSTALL.md 第 2 步
    Then 不再要求以 git rev-list 查 kit 的 Git 歷史
    And 改為執行 install.sh --dry-run，把會備份的技能列給使用者確認
```

## Gherkin 核准紀錄
- **核准 commit**: a57e109
- **核准來源**: 使用者於 2026-11-17 對話要求「讓安裝方式可以參照一般 github 常用的開源工具一樣，不需要 clone 就能安裝或更新版本」，並逐題確認：存放位置選「~/.local/share 依版本分目錄」（SCN-001、002）；下載來源選「release tag 的原始碼壓縮檔」，含 releases/latest 轉址與 `.gitattributes` 排除維護紀錄（SCN-001、008）；保護機制選「kit 附歷代檔案雜湊清單」（SCN-003、006）；發現修改時選「自動備份後覆蓋」（SCN-003）；選「要，get.sh --check」（SCN-005）。SCN-004 的 `--version`、`--dry-run` 出自同日採用的方案說明。同日 TBD-1 選「要，保護放在 install.sh」（SCN-007）；TBD-2 選「兩種並列」（SCN-009）；TBD-4 回覆「好這樣改」（SCN-010）

| Scenario | 核准日期 | 狀態 |
|----------|---------|------|
| SCN-001 | 2026-11-17 | 已核准 |
| SCN-002 | 2026-11-17 | 已核准 |
| SCN-003 | 2026-11-17 | 已核准 |
| SCN-004 | 2026-11-17 | 已核准 |
| SCN-005 | 2026-11-17 | 已核准 |
| SCN-006 | 2026-11-17 | 已核准 |
| SCN-007 | 2026-11-17 | 已核准 |
| SCN-008 | 2026-11-17 | 已核准 |
| SCN-009 | 2026-11-17 | 已核准 |
| SCN-010 | 2026-11-17 | 已核准 |

## 重構步驟概要

任務與證據見 [implementation-plan.md](implementation-plan.md#實作步驟)。

## 風險與首要驗證

- **最大風險**：判斷錯誤時，使用者改過的技能沒備份就被覆蓋；或 get.sh 在下載、解壓中途失敗時，留下半套的 kit 或錯誤的 `current`
- **風險等級與理由**：High。安裝會寫入使用者全域的平台設定目錄，被覆蓋的修改沒有其他地方可以找回；`curl | bash` 會在使用者機器上直接執行
- **首要驗證**：S1 先寫 test-install 案例（SCN-003、007 的備份判斷、下載或解壓失敗時 `current` 與平台目錄不變），確認失敗後才實作
- **選擇理由**：直接量測資料會不會遺失與中途失敗的狀態，都能在暫存 HOME 重現
- **完成證據**：上述案例先紅後綠；備份內容與覆蓋前逐位元組相同；中途失敗的案例中，平台目錄與 `current` 都與執行前相同

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | SCN-007：clone 用戶直接執行 install.sh 時，也用雜湊清單判斷並備份 | 已解決：2026-11-17 使用者選「要，保護放在 install.sh」；兩種安裝方式共用同一段邏輯 | SCN-007、S3 |
| TBD-2 | SCN-009：安裝文件以 get.sh 為主或兩種並列 | 已解決：2026-11-17 使用者選「兩種並列」 | SCN-009、S6 |
| TBD-4 | SCN-010：install.sh 已內建備份（TBD-1），INSTALL.md 第 2 步的 `git rev-list` 人工判斷改為看 `install.sh --dry-run` 列出的備份 | 已解決：2026-11-17 使用者回覆「好這樣改」 | SCN-010、S6 |
| TBD-3 | 版本號 | 已解決：2026-11-17 使用者選 Major（v5.0.0）；安裝方式與 install.sh 的覆蓋行為都改變 | 發布 |

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-17 | 建立 GitHub #9 與本 issue；使用者逐題確認設計，SCN-001～006、008 核准 | 使用者／Claude Code |
| 2026-11-17 | 使用者逐題確認 TBD-1～3：SCN-007、009 核准，文件兩種方式並列，版本 v5.0.0；SCN-010 待核准（TBD-4）；規劃文件提交到 main（`85cc332`） | 使用者／Claude Code |
| 2026-11-17 | 使用者核准 SCN-010（TBD-4），開始實作 | 使用者／Claude Code |
| 2026-11-17 | S1～S6 完成，五項檢查通過；待送審（S7） | Claude Code |
| 2026-11-17 | 第一輪審查 RETURN（MUST FIX 2）；使用者決定 get.sh 拒絕 v5.0.0 以前的版本；S8 修正完成，待第二輪審查 | 使用者／Claude Code |
| 2026-11-17 | 第二輪審查 PASS（`484924d`），SHOULD FIX 1；使用者選「修正後重審」，S10 修正完成，待第三輪審查 | 使用者／Claude Code |
| 2026-11-17 | 第三輪審查 PASS（`ccb5abd`），SHOULD FIX 1；使用者選「修正後重審」，S12 修正完成，待第四輪審查 | 使用者／Claude Code |

---
**建立日期**: 2026-11-17  
**分級**: Medium — 新增安裝腳本與雜湊清單，修改 install.sh、check-kit、測試與安裝文件；不需 Phase／Task 拆解  
**風險**: High\
**狀態**: 實作中
