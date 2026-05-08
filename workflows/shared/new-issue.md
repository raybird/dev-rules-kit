---
description: 分析需求並建立 issue 文件
---

請僅根據目前 workspace 中的程式碼、設定與文件進行分析。

禁止：
- 憑空補需求
- 提前實作
- 修改正式程式碼
- 自行重構架構
- 忽略既有 coding style

請先：

1. 分析需求與現況
- 使用者流程
- 新舊行為差異
- 模糊與衝突點
- 相關模組與資料流

2. 定義變更邊界
- 可修改區域
- 禁止修改區域
- 可能風險

3. 依照 `docs/AGENTS.md`
建立或更新：

`docs/issues/issue-{編號}/`

至少包含：
- README.md
- requirement-analysis.md
- technical-analysis.md
- implementation-plan.md

所有文件格式、狀態、timeline、changelog、日期格式與維護方式，
全部遵守 `docs/AGENTS.md`。

若需求資訊不足：
- 不得自行腦補
- 必須明確記錄未知事項與阻塞點

對話中只輸出：
- 分析摘要
- 已建立/更新檔案
- 阻塞問題
- 待確認事項