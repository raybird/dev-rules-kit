# 使用指南

一般局部修改可直接描述目標與檢查方式，agent 依通用規則完成。需要跨 session 追蹤 issue、分批規劃與 PR 審查時使用以下閉環。

## 初始化與更新

先安裝[規則](../rules/README.md#安裝方式)與[技能](../skills/README.md#安裝方式)，再從 kit 根目錄執行：

```bash
python3 scripts/init-project.py /path/to/project
```

專案目錄須已存在。首次部署建立核心規範、範本、`docs/agents/project.md` 與部署基線；把專案驗證命令、邊界與本地 gate 放 project.md。

```bash
python3 scripts/init-project.py /path/to/project --update --dry-run
python3 scripts/init-project.py /path/to/project --update
python3 scripts/init-project.py /path/to/project --check
```

更新保留既有 project.md，只更新與上次部署基線一致的核心。核心有本地修改、缺少可信基線或 symlink／hardlink 衝突時，整批停止。`--check` 驗證核心與 kit 一致及客製檔存在，不驗證客製語意。初次從舊版遷移依 [AGENTS.md](AGENTS.md#客製邊界與同步策略) 人工分離客製內容。

文件版本描述編輯歷程，流程契約描述技能相容性。同 major、專案 minor 不低於技能需求即可；純文字更新不要求所有技能同步跳號。升級前仍查 [CHANGELOG](../CHANGELOG.md)。

## 日常推進

```text
/new-issue issue:101 主題:修正空字串驗證 內容:空字串應顯示必填錯誤，有值時維持原行為。
/dev-cycle 101
```

已明確提供的結果與範圍可作核准來源；缺少會影響結果的決策才詢問，不固定提出多個方案。Small 以 README 的 AC 與步驟記錄；Medium 增加 implementation-plan；Large 在同一計畫細化 Phase／Task，分析文件依實際調查或取捨需要建立。

```text
new-issue → decompose（Large，在原計畫細化）
          → execute-task（包含 code-simplify 與驗證）
          → create-commit → create-pr → review
                              ↑           │
                              └──修正後───┘
```

dev-cycle 自動選下一個已核准、相依滿足的 Task；分批核准或重新核准不阻塞無相依的已核准項目。Large 新核准的 Scenario 會先補拆，再實作。PR 前現存驗收須全部已核准或逐項豁免。

完成任務時，證據保存在原任務或 artifact，對話只回報結果與位置。不同測試層級保留各自紅綠燈；同層重複保障可合併，不受 Small／Medium／Large 限制。純重構比較前後同組測試，文件用適用的靜態或人工驗證。

## 查詢與等待

```text
issue 101 到哪了
繼續處理 issue 101，並回報進度
```

第一句只查詢、不補寫 metadata。第二句是推進，會沿用已有授權；不是看到「進度」就停止執行。

等待外部驗收窗時，先完成當下能做的工作，再記預定窗口與判準，回報後結束本次調用。等待合併同樣回報後結束，不輪詢空轉、不自動合併。重新呼叫時從文件、Git／PR 與持久化證據恢復。

決定不修復時保留該終態、理由、殘餘影響及決策審查／豁免；不會要求做完被放棄的實作，也不會製造 merge 日期。

## PR 與 review

協調者把同一組固定 BASE／HEAD 傳給 PR 與 review，避免 commit 數量推算不同範圍。`/review 5` 仍可審查最近五個 commit，但若未覆蓋完整 PR，只算局部審查。

PR 的 Proof of Test 採逐驗收編號表格，連到固定版本規格與命令／輸出證據。多個條件可共用證據；被測內容、環境與時效一致時沿用，發生相關變動才重跑。未執行項與豁免照實揭露。

獨立 reviewer 按實際風險檢查失敗面，不湊固定案例數。報告保存到平台，或 issue 目錄中的本機 artifact。若本機後續提交只新增本次報告且通過 review 技能內附檢查器，原審查有效；其他變更重新審查。patch-id 只是輔助識別，不能單憑它相等放行新 HEAD。

## 技能快速參考

| 技能 | 使用方式與結果 |
|---|---|
| new-issue | 建立／修訂需求與驗收；先使用現有資訊，只問必要缺項 |
| decompose | 細化 Large 的原計畫；舊 issue 沿用已指定的獨立 Decomposition |
| execute-task | 指定或依順序選一個可執行 Task，驗證、精煉一次並回寫狀態 |
| code-simplify | 可單獨精煉指定變更；已由 execute-task 處理者不再重複 |
| create-commit | 依 staged diff 與專案格式產生訊息；明確要求提交時直接執行 |
| create-pr | 撰寫 Proof 表；已要求建立／更新 PR 時直接操作平台 |
| review | 對固定範圍獨立審查並保存 artifact；無能力時如實回報 |
| dev-cycle | 查詢唯讀；推進自動派送已授權工作，遇等待或阻塞結束本次調用 |
| git-squash | 使用與 create-commit 相同的專案格式，提供符合專案策略的合併命令 |
| writing-rules | 修改 agent 規範前使用；檢查觸發、位置、完成判準與實跑效果 |

Superpowers 為選用的階段引擎；已有共識不因載入 brainstorming 重問，缺套件時使用本地等價流程。[外部工具設定](setup/tools.md) 不屬必要前置。

## 格式與驗證

issue 格式參考 [README 範本](agents/readme-templates.md) 與 [建檔清單](agents/issue-checklist.md)。使用者可明確要求豁免個別 gate，agent 記錄來源及殘餘風險，其他 gate 繼續適用；誠實回報始終保留。

本 kit 的自動測試覆蓋安裝、Git 證據及契約檢查。宿主中的技能觸發、詢問與狀態推進另依 [流程回歸](workflow-regression.md) 實跑，不能以 Python 測試成功代替。
