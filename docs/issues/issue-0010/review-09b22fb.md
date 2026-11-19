# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：50b44922ef8b15124dd3b3cb5c7e9070fae21aa6
- Reviewed HEAD SHA：09b22fba97832e2452e14bfce1f5e91b694ad3f4
- Reviewed patch-id：af58eca9c2f2bd51017c3a1856cb5bb5f48c2243
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-0010/review-09b22fb.md
- 增量覆審：上一份報告 [review-40f9475](review-40f9475.md)（PASS，綁定 H1 = 40f94759a0b5613ff97b0829020599757f92aab7，完整範圍），增量範圍 `40f9475..09b22fb`（7c43547、1800523、1dd86c2、09b22fb）。依 HEAD 版 review-evidence.md:61-63 核對三項條件，都成立：(1) review-40f9475 綁定 H1、記完整範圍，表頭 patch-id `f86a0e27…` 與 `git diff BASE 40f9475 | git patch-id --stable` 重算的結果相同；`merge-base --is-ancestor 40f9475 HEAD` 成立，`rev-list --merges 40f9475..HEAD` 為 0。(2) main 仍是 `50b4492`，等於 Reviewed BASE。(3) 協調者把上一份報告與新範圍一起交給本 reviewer。我重算 `BASE..HEAD` 的 patch-id，得到 `af58eca9…`，與上方相同。

## 問題與風險
- MUST FIX：無

- SHOULD FIX 1：CHANGELOG.md:31-34（[5.2.0] 驗證段）與 docs/rule-verification-status.md:342 沒有記錄修正後的重跑。1800523 依上一份 SHOULD FIX 1、NICE TO HAVE 1 改了 review-evidence.md 條件 1 與觸發條件的語意。現行文字的實跑來源是 evidence/s6-wf36/ 的三輪：wf36-r3 通過；wf36b-r5 因 fixture 缺陷失敗；wf36b-r6 在補完 fixture 後通過。但 rule-verification-status:342 的來源仍只列 s2-wf36（kit `b3ae52f`／`04feb29`），還寫「review-evidence.md 與 review 技能在那之後到審查前沒有再改」。這句對第一次審查成立，對現行文字不成立，讀者會以為現行規則是由 s2 驗證的。CHANGELOG 驗證段也只寫「修正 fixture 後重跑 2／2」，沒有提到第二次補 fixture，也沒有提到修正後的 1／1 重跑。AGENTS.md 要求新增規則在 rule-verification-status 記可指認的驗證來源。建議：:342 補上「review-40f9475 修正後（kit `1800523`／`1dd86c2`）：影響組 1／1；對照組 r5 因 fixture 未依 project.md 更新根目錄 README 而失敗，補 fixture 後 r6 1／1（docs/issues/issue-0010/evidence/s6-wf36/）」，並刪掉或改寫「到審查前沒有再改」。CHANGELOG 驗證段的 WF-36 那一項補一句同樣的內容。

- SHOULD FIX 2：docs/issues/issue-0010/implementation-plan.md:36（S2 列末尾）。為了上一份 NICE TO HAVE 4 補的那句「用目前的產生器重建，wf36b、wf36c 的 H1 是 `e2ff4af`」，在 HEAD 不成立。我在 scratchpad 用 HEAD 的產生器重建，結果是：wf36b、wf36c 的 H1 為 `547810e`，wf36 為 `bc1f2b0`（和 wf36-r3、wf36b-r6 一致），BASE 為 `39045dd`。這句在 1800523 提交時就已經不成立：wf36b-r5 用 kit `1800523` 產生的 H1 是 `bcc1068`。原因是 fixture 的 `docs/` 由 kit 部署，kit 文件一改 SHA 就跟著變，而 1dd86c2 又再改了一次產生器。這是證據來源檔裡的錯誤事實，重現的人會被誤導。建議改成「以 kit `04feb29` 的產生器重建，wf36b、wf36c 的 H1 是 `e2ff4af`；fixture 的 SHA 隨 kit 的 docs 與產生器變動，以各輪證據開頭記的 kit HEAD 為準」。

- NICE TO HAVE 1：舊措辭殘留在幾個未改動的摘要處，與這次修正後的權威定義不完全一致：
  - implementation-plan.md 設計段 :9「上一份報告有效（PASS 或 RETURN）」、:11「變動會影響上一份報告查過的內容時」、:22「記錄決定的提交只動記帳區段，PASS 沿用；選了修正的修完後送增量覆審」。:22 沒有附契約條件，也沒有「結論與修正同一提交」。
  - docs/AGENTS.md:204 的 2.14 修訂紀錄寫「上一份報告有效」，正是 NICE TO HAVE 1 想消除的歧義。這是下游會讀到的產品檔。
  - docs/usage.md:67「查核變動與它影響到的既有結論」。

  這幾處都只是摘要並指回 review-evidence.md，不會改變行為。建議 docs/AGENTS.md:204 改成「H1 有一份記完整範圍的報告」，計畫設計段補一句「依 review-40f9475 修正，見 review-evidence.md」，或者直接同步措辭。README SCN-001 Background 的「有效的持久化報告」、SCN-003 的「有效報告」屬於已核准的規格；照上下文讀，就是「對 H1 有效」，與新文字不矛盾，不建議為此重新核准。

- NICE TO HAVE 2：docs/issues/issue-0010/fixtures/build_fixtures.py:185-193。wf36 與 wf36b 的 fixture 先提交「保存報告並記錄決定」（TBD-1 已解決），之後才另外提交修正，正好是 HEAD 的 dev-cycle:43-44「結論與修正放在同一個提交」要避免的形狀。wf36b-r5 的 reviewer 已經把它列為流程偏差。WF-36 的判準只看 review 端，不影響判定。建議在 expected.md「fixture 事實」補一句「fixture 的提交形狀早於 dev-cycle 的同一提交規定，只用來測 review 端」，避免之後被當成示範寫法。

## 已查核維度
- 驗收與證據：
  - 上一份報告中決定修正的建議（README TBD-2），逐項確認：
    - SHOULD FIX 1：review-evidence.md:67 已照建議改成「變動會影響未改動的程式或上一份報告的結論時」，例子保留；CHANGELOG:21 同步。已修好。
    - SHOULD FIX 2：dev-cycle:44 已改成「依 review-evidence.md『審查之後的提交』判定有效即沿用 PASS」，與 :43 的說法一致。已修好。
    - SHOULD FIX 3：採第二種做法。:43「需修正者回 execute-task，結論與修正放在同一個提交」與 :44「結論與修正放在同一個提交，再送審新範圍」都改了，CHANGELOG:26 同步。逐列走過：選了修正時，結論不會單獨進入已提交狀態，「已記錄、未修正」的狀態不再落到 create-pr。如果回合中斷，留下未提交的結論，會由「交付變更尚未提交」列一起提交，PASS 失效後回到 review，由 reviewer 檢查決定要修的項目，不會漏修後進 PR。已修好。
    - NICE TO HAVE 1：review-evidence.md:61 改成「綁定 H1、記完整交付範圍的持久化報告（…局部審查的報告不算）」。已修好，殘留措辭見 NICE TO HAVE 1。
    - NICE TO HAVE 2：review SKILL:35 分成「曾經審查過，但完整審查…時寫原因；第一次審查時省略」，與 SCN-003 一致。已修好。
    - NICE TO HAVE 4：S2 補了說明，但事實有誤（SHOULD FIX 2）。
    - NICE TO HAVE 5：expected.md:152-154 補了解讀節，標題寫明「於實跑之後」、判準原文不改。已修好。
    - NICE TO HAVE 6：rule-verification-status:342 註明早於 d104509。已修好，但沒有涵蓋修正後的重跑（SHOULD FIX 1）。
    - NICE TO HAVE 3：依決定不修，增量範圍沒有改根目錄 README.md。符合。
  - SCN-001～005：判定依據與上一份報告相同，修正沒有改變這些結論的前提，沿用。SCN-002 的文字缺口已由 SHOULD FIX 1 補上。SCN-004 Then 第 3 行無條件寫「沿用 PASS」，dev-cycle:44 改成依契約判定，在 2.4 以上的專案行為相同，不矛盾。
- 增量範圍逐檔結論：
  - CHANGELOG.md：:21、:26 與新文字一致；驗證段缺修正後的重跑（SHOULD FIX 1）。
  - docs/agents/review-evidence.md：:61、:67 符合建議，沒有新的矛盾。
  - docs/issues/issue-0010/README.md：7c43547 加了 `**現行 review**`、Timeline 與 `**狀態**`；1800523 加了 TBD-2、Timeline 與 `**狀態**`。兩次都只動記帳區段。TBD-2 預定「各 1 輪」，實際 wf36b 跑了 2 輪，計畫 S6 有照實記錄。通過。
  - evidence/s6-wf36/ 六個檔案：見下方「重跑紀錄的誠實度」。
  - fixtures/build_fixtures.py：只對 `kind != 'impact'` 的 wf36b、wf36c 在 H1 加一行根目錄 README 說明，有 `assert` 確保只替換一處。wf37／wf37b 走 `build_pass`，不受影響，與 expected.md 寫的「wf36、wf37、wf37b 不改」相符。在 HEAD 重建五組，測試都通過；wf36b 的 `overdue` 回傳 `[1]`。
  - fixtures/expected.md：三節的提交順序見下方。
  - implementation-plan.md：S6 列與證據原文一致；S2 的補句有誤（SHOULD FIX 2）；設計段有舊措辭（NICE TO HAVE 1）。
  - review-40f9475.md：在 7c43547 單獨新增，之後沒有再改；表頭 SHA 與 patch-id 經重算確認。
  - rule-verification-status.md：SHOULD FIX 1。
  - scripts/skill-hashes.txt：dev-cycle 與 review 的 v5.2.0 雜湊已更新，check-kit 通過。
  - skills/dev-cycle/SKILL.md、skills/review/SKILL.md：同上方逐項確認，通過。
- 重跑紀錄的誠實度：
  - 提交順序有佐證：
    - 「審查建議修正後重跑 WF-36」在 1800523（15:10:50）提交。wf36-r3、wf36b-r5 開頭記 kit `1800523`，而且 r5 的 H1 `bcc1068` 就是 1800523 版產生器的對照組輸出，和 HEAD 重建的 wf37 H1（內容相同）一致。
    - 「修正後重跑的結果與 wf36b 再重跑」與 r3、r5 證據、產生器修改同在 1dd86c2（15:15:51），r6 記 kit `1dd86c2`，在 09b22fb（15:19:38）才提交。在 HEAD 重建的 SHA（wf36 `bc1f2b0..80c5fac`、wf36b `547810e..159d0e4`、BASE `39045dd`）與 r3、r6 的報告完全一致。
    - wf36c 解讀節自己標明「於實跑之後」，沒有冒充事前寫定。
  - 敘述與原文一致：r3 報告記 BASE `39045dd`、增量 `bc1f2b0..80c5fac`，把 `overdue` 列為重新查核，判 MUST FIX 與 RETURN。r5 記增量 `bcc1068..3ec8489`，`todo.py` 寫為沿用，以 project.md:15 常青文件為由判需決策的 MUST FIX 與 RETURN。r6 記增量 `547810e..159d0e4`，判 PASS，另有一項 H1 就有的需決策 SHOULD FIX（紅燈證據）。計畫 S6 與 expected.md 的描述和這些原文相符。
  - wf36b-r5 失敗後改 fixture 再跑，站得住：
    - fixture 的 project.md 規定使用者功能要更新根目錄 README，對照組 H1 改了清單輸出卻沒更新，fixture 違反了自己的規則。r5 的 reviewer 正確指出這點，不是誤報；WF-37 兩組也因同一條規定提問。
    - 修改只讓 fixture 符合它自己的 project.md，判準（expected.md:38-42）與規則文字都沒改，r5 保留原樣，再重跑的範圍事先寫定並提交。
    - 限制：wf36b 判準第 3 項要求整體 PASS，所以完整範圍裡任何真實缺陷都會讓對照組失敗，這是三次失敗（r1、r2、r5）的共同原因，與增量判斷無關。影響組 wf36 仍有同樣的 README 缺口，r3 沒有指出；但影響組的判準要求 RETURN，不受影響，只說明 reviewer 之間有差異。
- 相關失敗面：
  - 變動對未改動內容的影響：我在整個 HEAD 搜尋「查過的內容」「有效的持久化報告」「有效報告」「PASS 沿用」「同一個提交」等措辭。
    - review SKILL:10 與 :44 只指向 review-evidence.md，不受影響。
    - create-pr SKILL:15 第 4 點核對 merge-base 與 Reviewed BASE，條件 1 措辭的改動不影響它，沿用。
    - docs/usage.md:41 的流程圖與修正後的做法相容；:67 見 NICE TO HAVE 1。
    - README SCN-002、SCN-004 與新文字相容（見上方）。
    - 計畫設計段與 docs/AGENTS.md:204 有舊措辭（NICE TO HAVE 1）。
    - workflow-regression.md 的 WF-36 結果連到計畫 #實作步驟，S6 已經包含重跑，沿用。
  - 上一份報告列的其他失敗面（rebase、merge 目標分支、換目標分支、連續增量），前提沒有變，沿用。「選了修正但回合中斷」已由 SHOULD FIX 3 的修正處理。「契約 2.2／2.3 記錄建議結論」已由 SHOULD FIX 2 的修正處理。
- 需求、架構、安全、品質：
  - 權威定義仍只在 review-evidence.md，技能與 CHANGELOG 只摘要。rules/ 沒有改，不需要同步雙語。沒有安全面。
  - 根目錄五項檢查在 HEAD 重跑全部通過：check-kit OK；check-links OK；`bash -n scripts/install.sh` OK；test-install 32 tests OK；test-evidence 296 tests OK。工作樹仍是乾淨的。
- 增量覆審時：
  - 重新查核的項目與理由：
    - 條件 1 與觸發條件改了措辭：搜尋整個 HEAD 中依賴它們的地方。
    - dev-cycle :43、:44 改了：重走一次狀態表的列序與中斷狀態。
    - 規則語意改了：重新核對 WF-36 重跑的證據與提交順序。
    - 產生器改了：在 HEAD 重建 fixture，核對 SHA 與測試。
    - S2 的補句重寫了 SHA 事實：重建後發現有誤。
  - 沿用的結論：上一份報告的固定檢查清單第 2 項（報告欄位與 verify-artifact 相容）、第 5 項（契約 2.6 與最低需求的相容做法）、第 7 項（撰寫規範），以及 SCN-003、SCN-005 與 WF-37 的結論。增量沒有改 verify-artifact.py、docs/AGENTS.md 的契約欄位、WF-37 的 fixture 與證據，確認不受影響。
- 豁免、待確認與限制：
  - 沒有 Gate 豁免。TBD-1 維持待確認，S7 尚未開始。
  - 只測 Claude Code。dev-cycle「結論與修正同一提交」的新行為沒有實跑，已含在 CHANGELOG 的「選了修正之後的增量送審（連續回合）」未實跑項目中。
  - 未查核：r3、r5、r6 的 stream 原文只看了開頭與工具動作摘要，沒有逐行看完；報告原文已全部讀過。7c43547 保存的報告是否與當時 reviewer 交出的原稿逐字相同，無法從 repo 核對。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
