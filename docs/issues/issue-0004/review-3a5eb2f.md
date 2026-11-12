# 審查報告
- 範圍：差異覆審（8fef4a9..3a5eb2f；完整範圍 main..issue-0004-post-pass-commit）
- Reviewed BASE SHA：3185a223e5e16e099de11e636de2baa9f1c670fb
- Reviewed HEAD SHA：3a5eb2f6eb25910b9c57818fce959db6257361b8
- Reviewed patch-id：f7343de9a5b55936d8e5074afa2e1e8df87f2a47
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0004/review-3a5eb2f.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE：docs/issues/issue-0004/fixtures/expected.md:44 與 fixtures/build_fixtures.py:19-20 會從當下 kit 的 `skills/review/SKILL.md` 取出提醒行。
  - 影響：用 HEAD 的 kit 重新產生 fixture，報告會帶新的括號，和實跑時用的 `7a5a4ba` 不同。
  - 現有揭露：README 步驟 1 已說明修訂後重跑的 fixture 用的是補括號前的句子、沒有重跑；步驟 3 也寫了 kit `041514c`。所以這不是揭露不足，只是要重現時得自己對上版本。
  - 建議：之後若再改這兩處，在 expected.md 修訂節註明「重現須用 kit `041514c`」。

## 已查核維度
- 驗收與證據：
  - 上一輪 MUST FIX（診斷寫錯）已修正。
    - 原本寫錯的四處都已改成照實描述：README 步驟 3、CHANGELOG.md:56、rule-verification-status.md:334，以及 expected.md 以 NOTE 補記。
    - 對照證據檔：
      - wf32-r1.md、r2.md、r3.md 第 1 個工具動作都是 `cd "$PWD"; …` 開頭、內含 `cat docs/AGENTS.md` 的複合命令（三份都在第 22 行）。
      - 這個命令出現在各檔的「權限拒絕」中（r1:33、r2:33、r3:32），tool_use_id 對得上。
      - 之後三輪都沒有再讀 docs/AGENTS.md。
    - expected.md:42 原判準句維持原樣，檔尾加了 `> NOTE 2026-11-12：…` 補記更正，並註明判準本身不受影響，符合「不改寫原句」。
    - README Timeline 新增一列，把原來那列改成「當時診斷為…」，保留了當時的歷史，沒有偽造。
    - 全 repo 搜尋 `head -80`、`前 80 行`、`第 180 行`：剩下的都在證據檔（被記錄的原始輸出）、expected.md 原句（已有 NOTE）和 Timeline 的「當時診斷」，沒有仍當作現行結論的敘述。
  - SHOULD FIX 1（提醒在流程契約 2.3 以下不成立）已修正，見下方「需求、架構、安全、品質」。
  - SHOULD FIX 2（核准 commit）已修正。`**核准 commit**` 現值是 `041514c`。`git show --stat 041514c` 確認它就是規格修訂的提交（提交主旨「issue #4 規格修訂：…」，改了 README 的 AC、SKILL.md 範本、expected.md 修訂節與 issue-0004 builder），而且是在修正提交 3a5eb2f 裡一起改的，不是保存報告時回填。
  - SHOULD FIX 3（驗證狀態寫得比實測多）已修正。rule-verification-status.md:334 的狀態拆成三段：「報告帶提醒時的交接文件情境：已實跑驗證（3 輪）」、「reviewer 照抄提醒：僅靜態撰寫」、「只寫在 docs/AGENTS.md 的效果：未測到」，並寫明 0／3 不能說明規則本身無效。
  - NICE TO HAVE（wf28b3 缺 verify-artifact 原始輸出）已處理。README 步驟 3 的 AC-3 補上命令（路徑以 `<fixtures>` 遮蔽）與 OK 的輸出，和上一輪我獨立重跑的結果一致。
  - README「限制」說修訂後 r1 只讀了報告就做對。我核對了 revised/wf32-r1.md 的工具動作：r1 讀了 issue 目錄的 md（含報告）和 project.md，沒有讀 docs/AGENTS.md，敘述屬實。
- 相關失敗面：
  - 檢查都在 repo 根目錄跑：`check-kit.py` OK、`check-links.py` OK、`test-evidence.py` 244 個測試 OK。
  - builder 的 regex `（PASS 時照抄下一行）\n(.+)\n` 對新範本仍然取得到單行（括號在同一行內），所以 fixture 產生器不會壞掉。
- 需求、架構、安全、品質：
  - SKILL.md:47 補上的括號「流程契約 2.3 以下只有單獨新增本報告的提交可沿用」，和 review-evidence.md:53 的規定一致。那裡規定 2.3 以下只接受單一報告提交：目前 HEAD 是被審查 SHA 的直接後繼、唯一一個非 merge 提交、唯一的差異是新增這份報告。括號放在「PASS 會失效、需要重新審查」之後，讀起來是在限縮前半句「README 記帳區段可沿用」的例外，語意正確。2.4、2.5 的沿用條件不受影響。
  - README 對「修訂後重跑的 fixture 用補括號前的句子、未重跑」的揭露是充分的。步驟 1 有寫，也說明了理由：兩句對 2.4 以上的專案意思相同，fixture 的 docs 屬於 2.4 以上。重現時的版本問題見 NICE TO HAVE。
  - 隱私：新增行沒有 `/home/`、`/tmp/claude-` 或其他專案名稱。唯一命中的 `Co-Authored-By` 是保存的上一輪報告裡描述測試 agent 行為的文字，不是署名。
  - 署名：3185a22..3a5eb2f 共 7 個提交，訊息都沒有 AI 署名。
- 豁免、待確認與限制：
  - 待確認事項 TBD-1 如實記錄了上一輪的 `需決策`，以及 2026-11-12 使用者選的「維持報告提醒，不補測」，Timeline 也有對應的一列。全 repo 搜尋 `0／3`，沒有任何文件仍把「規則只寫在 docs/AGENTS.md」說成有效或無效：CHANGELOG 與 rule-verification-status 都寫「效果未測到」，workflow-regression.md:55 只列結果數字。
  - 無法確認使用者在對話中的回答原文，只核對了 README 的記錄。
  - 依指示未跑 claude，也未做回歸實跑。
  - 工具呼叫用量：7／30 次，清單 1～5 都查完了。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
