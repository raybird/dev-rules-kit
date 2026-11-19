# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：50b44922ef8b15124dd3b3cb5c7e9070fae21aa6
- Reviewed HEAD SHA：186e0c629a846c9748ca4ead7d4861b351a0d75e
- Reviewed patch-id：307bb848f47bd7c6c4a4c685c5559d7370951a47
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-0010/review-186e0c6.md
- 增量覆審：上一份報告是 [review-09b22fb](review-09b22fb.md)（PASS，綁定 H1 = 09b22fba97832e2452e14bfce1f5e91b694ad3f4，完整範圍）。增量範圍是 `09b22fb..186e0c6`，含 4fb8810 與 186e0c6 兩個提交。依 HEAD 版 review-evidence.md:61-63 核對三項條件，都成立：
  - (1) review-09b22fb 綁定 H1、記完整範圍。表頭 patch-id `af58eca9…` 與 `git diff BASE 09b22fb | git patch-id --stable` 重算的結果相同。`merge-base --is-ancestor 09b22fb HEAD` 成立，`rev-list --merges 09b22fb..HEAD` 為 0。
  - (2) `git merge-base main HEAD` 與 main 都是 `50b4492`，等於 Reviewed BASE。
  - (3) 協調者把上一份報告與新範圍一起交給本 reviewer。
  - 另外重算 `BASE..HEAD` 的 patch-id，得到 `307bb848…`，與上方相同；HEAD 是 186e0c6，工作樹乾淨。

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE：無

## 已查核維度
- 驗收與證據：上一份報告的建議都決定修正（README TBD-3），逐項確認如下。
  - SHOULD FIX 1，已修好。
    - rule-verification-status.md:343 已補上 s6 的重跑：kit `1800523`／`1dd86c2`；影響組 1／1；對照組 r5 因 fixture 失敗，補 fixture 後 r6 1／1。
    - 原本那句「到審查前沒有再改」已刪除。
    - CHANGELOG.md:32 的 WF-36 項補了同樣內容。
    - 事實核對：
      - `git log 1800523^..HEAD -- docs/agents/review-evidence.md skills/review skills/dev-cycle` 只列出 1800523。
      - s6 三輪證據開頭記的 kit HEAD，wf36-r3、wf36b-r5 是 `1800523`，wf36b-r6 是 `1dd86c2`。
      - 三輪的隔離設定技能摘要都是 `b38f184cd52b2ced`。
      - 所以 s6 驗證的就是現行規則文字，敘述正確。
  - SHOULD FIX 2，已修好、事實正確。implementation-plan.md S2 列改成「以 kit `04feb29` 的產生器重建，wf36b、wf36c 的 H1 是 `e2ff4af`」，並說明 SHA 隨 kit 變動、以各輪證據開頭的 kit HEAD 為準。實測方式與結果：
    - 在 scratchpad 把 repo clone 下來並 checkout `04feb29`；因為 .gitattributes 對 `docs/issues/` 設了 export-ignore，`git archive` 拿不到 fixture。
    - 用該版的 build_fixtures.py 重建，輸出是 `wf36: H1 775859c HEAD 0378aac`、`wf36b: H1 e2ff4af HEAD f427b78`、`wf36c: H1 e2ff4af HEAD fb9c7e7`。
    - wf36b 的 HEAD `f427b78` 與 wf36b-r3、r4 開頭記的「前：HEAD `f427b78`」相同，那兩輪的 kit HEAD 也是 `04feb29`。
  - NICE TO HAVE 1，已修好。
    - docs/AGENTS.md:204 的 2.14 修訂列改成「上一份報告綁定被審查提交且記完整範圍」與「變動影響到的未改動程式或上一份報告的結論要重新查核」。
    - docs/usage.md:67 改成「查核變動與它影響到的未改動程式和既有結論」。
    - 計畫設計段 :9、:11 改用新措辭；:22 改成「沒有選修正時依『審查之後的提交』判定；選了修正時結論與修正同一提交，再送增量覆審」，並註明依據 review-40f9475、權威定義的位置。
  - NICE TO HAVE 2，已修好。expected.md「fixture 事實」節末加了一行標註「（2026-11-19 補記）」的說明：fixture 的提交形狀早於同一提交的規定，只用來測 review 端，不是示範寫法。
  - SCN-001～005：增量只改文字與記帳，不影響判定前提，沿用上一份報告的結論。
- 增量範圍逐檔結論：
  - 4fb8810：只新增 review-09b22fb.md，並改 README 的 `**現行 review**`、Timeline 一列與 `**狀態**` 的值。`verify-artifact.py --reviewed 09b22fb --head 4fb8810` 回 OK，判定只有記帳變更，符合「只動記帳區段與新增報告」。
  - 186e0c6：`verify-artifact.py --reviewed 09b22fb --head 186e0c6` 回 INVALID（CHANGELOG.md），所以需要本次覆審，這是預期結果。各檔結論：
    - CHANGELOG.md：只改 [5.2.0] 驗證段 WF-36 一項，內容正確。
    - docs/AGENTS.md：只改 2.14 修訂列，該版本尚未發布，不必另外升版號。
    - docs/issues/issue-0010/README.md：只動待確認事項（新增 TBD-3）、Timeline 一列與 `**狀態**`。SCN 區塊沒有變動，TBD-3 寫明「只改文字、不改規則語意，不重跑 WF」，結論與修正放在同一提交，符合 dev-cycle:44。
    - fixtures/expected.md：只在「fixture 事實」節末新增一行標了日期的補記，「通過條件」與各節判準原文沒有改動。
    - implementation-plan.md：設計段 :9、:11、:22，S2、S6 兩列的狀態欄，內容正確。
    - docs/rule-verification-status.md：v5.2.0 區塊一列，內容正確。
    - docs/usage.md：「PR 與 review」一段，內容正確。
- 相關失敗面：措辭修改有沒有偏離權威定義，逐處對照如下。
  - 對照 review-evidence.md:61 的條件 1（綁定 H1、記完整範圍、PASS 或 RETURN）與 :67 的影響範圍（未改動的程式或上一份報告的結論）：docs/AGENTS.md 2.14、usage.md、計畫設計段、CHANGELOG、rule-verification-status 五處的意思都一致。
  - 計畫 :22 與 dev-cycle:43-44 的狀態表列一致：沒有選修正時依「審查之後的提交」判定；選了修正時結論與修正同一提交。
  - 這些都是摘要，並且指回權威檔，沒有新增或改寫規則。
- 需求、架構、安全、品質：增量只改文件，不動程式、檢查器或技能。根目錄五項檢查在 HEAD 都通過：
  - `check-kit.py`：exit 0
  - `check-links.py`：exit 0
  - `bash -n scripts/install.sh`：exit 0
  - `test-install.py`：OK
  - `test-evidence.py`：OK
- 增量覆審時，重新查核的項目與理由：
  - 改了措辭的 5 處，理由是要確認它們與權威定義一致。
  - S2 的 SHA 敘述，理由是它屬於事實陳述，已實際重建 fixture 核對。
  - rule-verification-status 與 CHANGELOG 的驗證來源，理由是它們決定讀者以哪一輪驗證為準，已核對 git log 與各輪證據開頭。
  - README 的記帳與 SCN 有沒有變動。
- 增量覆審時，沿用的結論：
  - review-09b22fb 對 review-evidence.md、review 技能、dev-cycle 狀態表、WF-36／37 證據與 fixture 產生器的結論，因為這些檔案在增量範圍內都沒有改動。
  - 措辭修改是摘要層級，不影響這些結論的前提。
- 豁免、待確認與限制：
  - TBD-1（契約 2.5 以下的相容做法要在下游試用確認）仍待確認，S7 的下游試用尚未開始。
  - 沒有重跑 WF，因為增量沒有改規則語意，不需要重跑。
  - 重建 fixture 只核對 `04feb29` 這一版。
  - 本次未用到工具呼叫上限，沒有未查核的項目。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
