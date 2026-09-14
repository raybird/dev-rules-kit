---
name: create-commit
description: 根據 staged diff 撰寫提交訊息；使用者要求提交時執行 commit，僅要求訊息時提供可複製內容。
---

1. 讀專案提交規範與 `docs/agents/project.md`（若存在），未定義時用 `type(scope): 中文摘要`，issue 編號放 footer `Refs: #ID`。
2. 讀 `git status` 與完整 staged diff，確認只包含本次授權的提交範圍；混入其他工作時先釐清歸屬，不把它一起提交。
3. 用問題與結果整理精簡訊息；僅保留幫助理解的細節，檔案路徑採 repo-relative。
4. 只要求訊息時放 code block；明確要求提交或由 dev-cycle 傳入提交授權時直接 commit，回報 SHA。必要輸入不足則具體列出，不重問已取得的授權。

完成判準：訊息描述 staged 的實際變更；執行提交時確認成功且回報真實 SHA。
