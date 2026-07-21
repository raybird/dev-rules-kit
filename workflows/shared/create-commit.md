---
description: 根據 git staged 的異動生成符合 Conventional Commits 規範的中文 commit 訊息。已 git add 待提交檔案、需要撰寫提交訊息時使用。
---

1. 看 git status 的 staged 檔案列表
2. 查看所有列表中檔案異動的內容
3. 統整異動內容生成符合 commit convention 1.0.0 規範精簡版條列訊息
4. 訊息中若提及檔案路徑，一律使用**相對於 repo root 的路徑**（如 `src/auth/login.ts`），不得使用絕對路徑（如 `/home/user/project/src/...`）或 `~` 開頭的路徑
5. 使用中文將訊息放到 code block 以便複製，不要直接提交