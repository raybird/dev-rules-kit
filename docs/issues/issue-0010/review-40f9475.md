# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：50b44922ef8b15124dd3b3cb5c7e9070fae21aa6
- Reviewed HEAD SHA：40f94759a0b5613ff97b0829020599757f92aab7
- Reviewed patch-id：f86a0e27fdc31b4161200d2545a681e24d9e77b4
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-0010/review-40f9475.md

## 問題與風險

- MUST FIX：無

- SHOULD FIX 1：docs/agents/review-evidence.md:67。觸發條件寫成「變動會影響**上一份報告查過的內容**時」，範圍比已核准的 SCN-002 窄。SCN-002 的 Given 是「H1 之前就存在、H1..H2 沒有改動的程式呼叫它」，這也包含 BASE 之前就在目標分支上的程式。如果 H1..H2 改了一個在 BASE..H1 沒動過的既有函式，目標分支上原有的呼叫端不在上一份報告查過的範圍內，照字面讀就可以不查，報告卻仍被當成完整範圍的證據。這正是 README 寫的最大風險（漏掉變動對未改動程式的影響）。WF-36 的受影響呼叫端在 BASE..H1 之內，沒有測到這個面。建議改成「變動會影響未改動的程式或上一份報告的結論時」，例子保留不動。

- SHOULD FIX 2：skills/dev-cycle/SKILL.md:44，新列寫「沒有選修正時 PASS 沿用」，沒有附條件。dev-cycle 的最低契約是 2.2，而 2.3 以下只接受「只新增報告」的提交，所以把結論記入待確認事項就會讓 PASS 失效。上一列（:43）「需決策」寫的是「依『審查之後的提交』判定有效時沿用 PASS；其他情況依新範圍重新 review」，兩列對同一種記帳提交的說法不一致。重新偵測時，review 列（:42）和 create-pr 第 4 點都會擋下，不會產生錯的 PR，但同一回合內協調者可能誤以為 PASS 仍有效。建議比照 :43，改成「沒有選修正時，依 review-evidence.md『審查之後的提交』判定有效即沿用 PASS」。

- SHOULD FIX 3：skills/dev-cycle/SKILL.md:44，「選了修正」但還沒修完的中間狀態。如果協調者先提交結論記錄，在修正提交前回合就結束了（需要多輪、權限阻塞、使用者下一則才回答等），下一次偵測時：PASS 仍有效（只動記帳區段）；新列不觸發（README 已有結論）；RETURN 列不適用；於是落到 create-pr 列。使用者選的修正會被跳過，只在 PR 的待確認事項揭露。S3 的「逐列走過」沒有走到這個狀態，CHANGELOG 也列為未實跑。:43 的「需修正者回 execute-task」有同樣的既有缺口。建議擇一處理：一是新列條件加上「或結論為修正，但 Reviewed HEAD 之後還沒有對應的修正提交」；二是規定選了修正時，結論與修正放在同一串提交、修完才重新偵測，並讓待確認事項維持 `待確認` 直到修正提交。`需決策`：要不要一併修 :43 的同一缺口。

- NICE TO HAVE 1：docs/agents/review-evidence.md:61 條件 1 的「有效的持久化報告」。同一份文件和 dev-cycle 狀態表裡，「有效」指 verify-artifact 判定對目前 HEAD 仍有效；但 H1 的報告對新 HEAD 照定義就無效（正因為有修正提交）。照字面跑 `verify-artifact.py --reviewed H1 --head H2` 會得到無效，可能把該增量的情況擋成完整審查。WF-36 的 6 輪都解讀正確，實際風險低。建議寫成「H1 有一份綁定 H1、記完整範圍的持久化報告」，這樣也明說了部分審查的報告不適用（目前要靠條件 2 間接排除）。

- NICE TO HAVE 2：skills/review/SKILL.md:35 範本寫「沒有上一份報告時省略」，SCN-003 卻要求「找不到 H1 的有效報告」時也寫明不採增量的原因。真的是第一次審查時可以省略；有過審查但找不到報告的情況，範本沒有要求寫原因。rule-verification-status 已註明這種情況只做過靜態覆核。建議分成「首次審查省略；找不到或不適用上一份報告時寫原因」。

- NICE TO HAVE 3：README.md:63-71 的流程圖沒有加「通過但有建議」分支，docs/usage.md:38-42 加了。AGENTS.md 要求改流程時檢查 README.md。根目錄 README 原本就省略「需決策」分支，可能是刻意簡化；如果是刻意的，可以不改。

- NICE TO HAVE 4：證據的可重現性。修正 fixture（04feb29）同時改了 wf36c 的 H1 測試，但 wf36c 沒有重跑（expected.md:60 有寫明）。用目前的產生器重建，wf36c 的 H1 是 `e2ff4af`，證據裡是 `775859c`；evidence/s1-fixture.txt 的 wf36b 與 wf36c 也是修正前的輸出。建議在 s1-fixture 或計畫 S2 加一句「wf36c 證據與 s1-fixture 的 wf36b、wf36c 對應修正前的產生器」。

- NICE TO HAVE 5：wf36c 的判準 expected.md:47 寫「Reviewed HEAD 是 H2」，實際兩輪的 Reviewed HEAD 都是 agent 在 rebase 後先補的「映射核准 commit」提交（3d3e9ed、4853dbc），計畫 S2 判為記帳、不影響判定。這個判斷站得住：審查的是送審當下的 HEAD，映射動作也符合 acceptance.md。但這是事後解讀判準，只寫在計畫裡，CHANGELOG:32 與 rule-verification-status:344 直接寫 2／2。建議在 expected.md 的判定節補記這個解讀。

- NICE TO HAVE 6：WF-36 用 kit `b3ae52f`／`04feb29` 實跑，那時 dev-cycle 的新列和推進步驟 2 還沒加入（d104509）。review-evidence.md 與 review 技能在那之後沒有再改，結論不受影響，但 rule-verification-status 可以註明「WF-36 早於 dev-cycle 變更」。

## 已查核維度

- 驗收與證據：
  - SCN-001：review-evidence.md:59-65 定義條件與完整範圍的欄位；WF-36 影響組 r1、r2 都記 BASE `e88e386`、HEAD `0378aac`、增量 `775859c..0378aac`，wf36b r3、r4 記 `e2ff4af..f427b78`。「create-pr 以這份報告為完整範圍證據」只做了靜態查核，結果相容（見清單 2）。通過。
  - SCN-002：wf36-r1 與 r2 的報告都把 `overdue` 列為重新查核並判 MUST FIX／RETURN，r1 還搜尋整個 HEAD 找出 `due_of` 的所有呼叫端。我在 scratchpad 重建 fixture，確認 wf36 的 H2 測試全過，`overdue` 回傳 id 1、2 兩筆（2026-12-01 被誤判）；wf36b 只回傳 id 1，SHA 與證據一致。文字範圍有 SHOULD FIX 1 的缺口。
  - SCN-003：wf36c r1、r2 都寫明條件 1、2 不成立，BASE 為 `71c48e2`。只改 merge-base 與找不到報告兩種情況未實跑，已揭露。
  - SCN-004：dev-cycle:44 新列；wf37-r1 原文確認同一則訊息列 3 項，每項附建議答案與三種去向。在 scratchpad 跑 `verify-artifact.py`，wf37 的 PASS 判 OK。
  - SCN-005：review-evidence.md:59「修正來源不限」，加上 review 列與 create-pr 列，靜態成立；CHANGELOG:34 揭露未實跑。
- 相關失敗面：
  - 修正改了 BASE..H1 內的函式：WF-36 已覆蓋，通過。
  - 修正改了 BASE 之前就有的既有函式：未覆蓋，文字有缺口（SHOULD FIX 1）。
  - rebase：wf36c 已覆蓋，通過。
  - H1..H2 merge 了目標分支：merge-base 會變，條件 2 擋下，靜態通過。
  - merge 了非目標分支：`H1..H2` 的 diff 包含合入的內容，每個變動檔案都要給結論，靜態通過。
  - PR 換了目標分支：用新目標分支的 merge-base 判斷，相同時範圍一樣，靜態通過。
  - 契約 2.2／2.3 的專案記錄建議結論：SHOULD FIX 2。
  - 選了修正但回合中斷：SHOULD FIX 3。
  - 連續增量（H3 以 H2 的增量報告為上一份）：H2 報告本身就是完整範圍證據，可以接續，不會變成串接多份報告。
- 固定檢查清單：
  1. 條件三項：部分審查的報告靠條件 2 間接排除（部分審查的 BASE 不等於 merge-base）；merge 提交、換目標分支、rebase 都會被條件 1 或條件 2 擋下，或不影響正確性。不會把不該增量的情況當成增量。該增量的情況有一個被擋掉的可能，來自「有效」一詞的解讀（NICE TO HAVE 1）。整體成立。
  2. 報告欄位：增量報告記完整範圍的 BASE／HEAD／patch-id，所以 create-pr 第 4 點核對「merge-base＝Reviewed BASE」照樣成立。verify-artifact.py 只比對 `Reviewed HEAD SHA` 那一行，並把 2.6 當作 ≥2.5 處理（:314、:411），相容。範本兩處欄位（:35 表頭、:44 已查核維度）與 review-evidence.md:65 的四項對應；「找不到報告」的情況見 NICE TO HAVE 2。
  3. SCN-002 的查核責任：「在整個新 HEAD 找出這些地方」、「只有確認不受影響的結論才寫為沿用」、「受影響的測試重跑」這幾條足以要求 reviewer 找出呼叫端，實跑也相符（r1 搜尋全 HEAD，r2 推翻「ISO 比較」的沿用）。但觸發範圍限於「上一份報告查過的內容」，比 SCN-002 窄（SHOULD FIX 1）。
  4. 狀態表：逐一走過五種情況。PASS 無建議 → create-pr。PASS 附建議 → 新列提問並等待，記錄後新列不再觸發 → create-pr。PASS 附建議且選了修正 → 修正提交讓 PASS 失效 → review 列；但「已記錄、未修正」的中間狀態會落到 create-pr（SHOULD FIX 3）。RETURN → RETURN 列。PASS 兼有需決策 → :43 先觸發並把建議併入同一則訊息，記錄後兩列都不再觸發。沒有無限迴圈：建議以 README 有沒有結論為準，每次都要使用者回答才會前進。
  5. 相容做法：契約 minor 從 2.5 升到 2.6，review 最低需求維持 2.1、dev-cycle 維持 2.2，符合 docs/AGENTS.md:26 的「同 major、minor 不低於需求」。docs 仍是 2.5 時，review-evidence.md 沒有這一節，review 技能:10 明寫完整審查，行為與 2.5 相同；dev-cycle 新列不依賴 docs，在 2.5 下照樣提問，選了修正就完整重審。和齊備性檢查一致。實際行為待 S7／TBD-1 確認。
  6. 實跑紀錄的誠實度：CHANGELOG:31-34、rule-verification-status:343-347、計畫 S2 與 S4 的數字與 evidence 原文一致（wf36 與 wf36c 都是 RETURN、wf36b-r1 與 r2 都是 RETURN、r3 與 r4 都是 PASS、WF-37 兩組各 2／2）。wf36b 的處理站得住：修正 fixture 的補節和產生器改動在 04feb29（14:43）提交，重跑證據記 kit `04feb29`；判準沒有改，只改 fixture 中與 SCN-002 Given 不符的 H1 測試；第一次的 r1、r2 保留原樣；第一次 RETURN 是 reviewer 正確指出 fixture 缺陷，不是誤報。小瑕疵見 NICE TO HAVE 4、5、6。
  7. 撰寫規範：新段落以正面表述為主，條件可以檢查；權威定義只在 review-evidence.md，技能、usage、AGENTS 修訂紀錄與 CHANGELOG 只摘要並指回該處，沒有重複定義。rules/ 沒有改，增量覆審屬於下游 docs 與技能層級，雙語 rules 不需要同步。check-kit 通過。
- 需求、架構、安全、品質：
  - 需求範圍與 README 關鍵差異表一致；沒改檢查器，與 README 分級說明相符。
  - 沒有安全面。
  - 沒有跨 Task 重複邏輯。dev-cycle:44 引用 acceptance.md「逐題確認」卻固定「同一則訊息」，蓋過該檔第 3 點的拆題規則；這是 SCN-004 的明確要求，可以接受。
  - 五項檢查在 HEAD 重跑全數通過（check-kit、check-links、bash -n、test-install、test-evidence），工作樹仍是乾淨的。
- 豁免、待確認與限制：
  - 沒有 Gate 豁免。TBD-1 維持待確認，S7 尚未開始。
  - 只測 Claude Code。
  - 未查核：wf36c-r2、wf37-r2、wf37b 原文只抽查了判定與標頭；build_fixtures.py 只透過重建結果查核，沒有逐行閱讀；skill-hashes.txt 只靠 check-kit 驗證。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
