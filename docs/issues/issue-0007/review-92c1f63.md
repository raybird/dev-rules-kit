# 審查報告
- 範圍：差異覆審（10af0b4..92c1f63；完整範圍 main..issue-0007-remaining）
- Reviewed BASE SHA：3469f604e601bfdddf9c5662a530f834b5eba99d
- Reviewed HEAD SHA：92c1f6311c9dd2bcd4570a211b02fe12bc11fba8
- Reviewed patch-id：603bd611fc6fd5c79c8f89b854cab4a2f8d24114
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0007/review-92c1f63.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX 1：scripts/init-project.py:14-19 的 `PAST_TEMPLATES`。e1bbf05 改了 docs/agents/project.md 範本，但修改前的雜湊 `c98fe5d917f623eb8d354ae7aa116ec5f4680dab9f9859a4b9cad56325b9ceb8` 沒有加進集合，違反同檔第 13 行的註解「修改範本時，把修改前的雜湊加入此集合」。影響：v4.10.0／v4.11.0 初始化、project.md 還是範本原文的下游，更新到 4.12.0 後不會再收到「project.md 仍是初始化範本原文」提醒。這只影響提醒，不影響是否覆寫 project.md。建議把這個雜湊加進去。另外，v4.10.0 的 6bfca60 改範本時也漏了 `de34e1562694df8e5f638fe23579109df12f0477f0cc7a7ae4763d957fc9a384`，那是本 issue 之前就有的遺漏，要不要一起補 `需決策`。
- NICE TO HAVE 1：92c1f63 是只回填核准 commit 的獨立提交。docs/agents/acceptance.md:40 要求「在下一個本來就要做的提交順手回填」，例如保存審查報告的記帳提交。結果沒有錯（e1bbf05 正是最後修改 `**核准來源**` 行的提交，和推導出的基線一致），只是多了一個提交。之後照規定順手回填即可。
- NICE TO HAVE 2：CHANGELOG.md 4.12.0「下游更新」寫的是「查證命令含管線的專案，可在 project.md…登記命令名稱」，漏了 `<`，和變更段的「含管線或 `<`」不一致。另外 `init-project.py --update` 會保留 project.md，所以「project.md 範本同步補這句」不會送到既有下游，只靠這一行提示手動補。可以順手補上「或 `<`」。

## 已查核維度
- 驗收與證據：
  - 第 1 項：
    - NICE TO HAVE 1：document-types.md:28 改成「含管線或 `<`」，括號說明「直線符號要寫成 `\|` 才不會切欄，照原文複製執行就會出錯」，已修正到位。
    - NICE TO HAVE 2：docs/AGENTS.md:182 拆成四個做法，各附代價：提交到主幹（快轉代價）；提交到另一個分支；等合併後再提交（要等到合併才看得到）；接受重審（多一輪審查）。快轉代價不再像是兩個做法共用。「提交到另一個分支」沒附代價，因為它本來就沒有快轉問題，可以接受。已修正到位。
    - NICE TO HAVE 3：project.md:11 範本補了「命令含管線或 `<` 時取一個名稱，`## 現況` 的表格只寫名稱」，已修正到位。
  - 第 2 項：在 scratchpad/pipe-fixture 建了 fixture repo（docs/AGENTS.md 含 `**流程契約**: 2.5`，報告 review-<sha7>.md 含完整 Reviewed HEAD SHA，同一個提交更新現行 review）。verify-artifact.py 的判定如下：
    - 只有報告與現行 review 的變更：OK
    - 審查後把 `## 現況` 一列改成含 `\|` 的命令：OK（exit 0）
    - 改成含 `>` 的命令：OK
    - 改成含 `<` 的命令：INVALID，整張表凍結
    - 未跳脫的 `|`：也是 OK
    
    在 shell 執行 `echo a \| wc -l` 會輸出 `a | wc -l`，也就是 `\|` 照原文複製後會被當成字面參數，不會變成管線。所以新說法正確，TBD-3 寫的「跳脫的直線符號在現況表判 OK，但照原文複製執行會出錯」也如實。收窄掉「重導」後，只用 `>` 的命令可以直接寫在表格，這點也有實測支持。
  - 第 3 項：
    - AC-5 的修訂原文寫明修訂日期、來源（review-10af0b4 TBD-3）、原文「需要管線、重導或 `<`」，以及 project.md 範本同步。
    - 核准來源行補上「同日 AC-5 依 review-10af0b4 的需決策項修訂，使用者選『三項都修並覆審』（TBD-3）」。用 `git log -S` 查，最後修改這一行的提交是 e1bbf05，和回填的核准 commit 一致。
    - 92c1f63 只改了 `**核准 commit**` 一行（`待提交` → `e1bbf05`）。
    - TBD-3 為 `已解決`，影響 AC-5、AC-7，敘述與實際變更相符。
    - Timeline 新增兩列：review-10af0b4 PASS 與規格修訂（含 PASS 失效），都如實。
    - 步驟 4 標 ⏳、「待差異覆審」，如實。
  - 第 4 項：
    - CHANGELOG 4.12.0 標題已補 project.md，三條變更與 diff 一致（例外見 NICE TO HAVE 2）。
    - docs/AGENTS.md 修訂紀錄 2.11 改成「含管線或 `<`」。
    - rule-verification-status 第一列措辭同步，仍是「僅靜態撰寫」。
- 相關失敗面：
  - AC-5 的失敗路徑沒有發生：說明沒有要求在表格寫含 `<` 或未跳脫直線符號的命令，scripts/ 在本輪 diff 中也沒有變動。
  - 實測發現檢查器對未跳脫的 `|` 也判 OK（會讓欄位錯位，但不會凍結）。這是既有行為，AC-5 明定檢查器不動，所以不列為問題，只記在這裡。
- 需求、架構、安全、品質：
  - 第 5 項，在 repo 根目錄執行：
    - check-kit.py：OK
    - check-links.py：OK
    - test-install.py：14 tests OK
    - test-evidence.py：296 tests OK
  - 範本雜湊遺漏見 SHOULD FIX 1。這是從第 1 項的 project.md 改動延伸查到的，不是開放式找漏洞。
- 豁免、待確認與限制：
  - 第 6 項：
    - 新增行沒有本機絕對路徑或其他專案名稱（grep 無命中）。
    - 10af0b4..92c1f63 的提交訊息沒有 AI 署名。
    - 新增的表格列扣掉 code span 後，直線符號數都和欄數一致：修訂紀錄、Timeline、rule-verification-status 各 4 個，待確認事項 TBD-3 列 5 個，沒有未跳脫的 `|`。
  - fixture 第一次執行時，報告檔名沒用 review-<sha7>.md，判 INVALID「artifact 路徑與被審查 SHA 不符」。改用正確檔名後重跑，上面列的結果以重跑為準。
  - 工具呼叫 13 次，未超過 30 次上限，清單各項都查完。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
