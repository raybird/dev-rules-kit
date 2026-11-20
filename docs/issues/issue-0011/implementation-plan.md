# Issue 11 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。

### 狀態的語意（寫進 docs/AGENTS.md「有特殊意義的狀態值」）

- `**狀態**` 只寫階段：例如待實作、實作中、審查中、審查通過，以及三個特殊值。括號裡只放日期、SHA 這類錨定事件，不寫部署、推送、發版這類會被其他人或其他流程改變的狀態。範例 `已完成（2026-11-12 併入 main）` 改成不帶合併事件的寫法。
- `已完成` 的定義改為「這份 README 進入目標分支即結案」：有效 PASS 或明確豁免、沒有待決定的建議、沒有未豁免的待觀察項目時，保存報告的提交或之後的記帳提交在分支上寫好。有待觀察項目時改寫 `等待外部驗收窗`。`**狀態**` 本來就是記帳欄位，verify-artifact 不用改。
- 判定是否真的結案一律看合併判定，不看欄位。dev-cycle 狀態表「狀態為 `已完成` 且有其他可追溯的核准結案依據」那一列，改成合併判定已合併、或有不經合併的核准結案依據時才放行；分支上還沒合併時落到「等待合併」那一列。完成條件第 5 項改為合併前寫好終態、合併後不補提交。
- 懸置掃描在主幹上讀到的 `已完成` 已經經過合併；「已合併未結案」照舊抓舊專案留在「待合併」的 README。

### 進度只寫一處

- rules 第七節旁加一段通用原則（中英版同一章節）：同一份文件或 issue 裡，會變的進度只寫在一處，其他地方指向它；開頭的說明或警示只寫規則，不寫目前進度。
- kit 範本：概述不寫「目前進度」；待確認事項的影響欄只寫影響與關聯驗收編號；Timeline 去掉負責人欄。document-types.md 與 issue-checklist.md 同步。

### 核准 commit

- acceptance.md：欄位只寫目前基線的一個 SHA，重新核准時覆寫，舊基線記 Timeline。合併後仍是 `待提交` 屬正常，以「規格修訂的查核」的推導命令取得基線。
- verify-artifact.py：舊值去掉反引號後以 `待提交` 開頭即可回填（現行只認 `old.startswith('待提交')`）；新值的判定不變。review-evidence.md 第 47 行同步。

### 相容性

docs/AGENTS.md 文件版本 2.15，流程契約 2.6 → 2.7（minor）。dev-cycle 的「看到 `已完成` 一律依合併判定確認」對所有版本都成立，2.6 以下的 README 不需遷移；技能宣告的最低契約不變。

### 回歸案例

fixture 以 issue-0010 的產生器方式建立，放在本 issue 的 `fixtures/`；判準寫進 `fixtures/expected.md`，實跑前提交。實跑依 [workflow-regression](../../workflow-regression.md)，用隔離設定載入工作樹的技能，每組 2 輪。

- **WF-38**（SCN-003，首要驗證）：分支上的 README 狀態為 `已完成`、有效 PASS 報告，要求 `/dev-cycle` 查詢。未合併組：分支尚未併入 main。已合併組：已以 `--no-ff` 併入 main。
- **WF-39**（SCN-002）：有效 PASS、沒有建議，README 狀態為「審查通過」，要求 `/dev-cycle` 推進到交付合併前。
- **WF-40**（SCN-001、SCN-005）：Small issue 已併入 main，告訴 agent「已部署到測試環境，正式環境下週部署」，要求記錄；另一組是一份含開頭警示與待辦表的 issue 描述檔，要求把其中一項標為完成。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | docs/AGENTS.md「有特殊意義的狀態值」與工作流程第 3 項、文件版本 2.15／契約 2.7；dev-cycle 狀態表與完成條件；WF-38、WF-39 fixture 與 expected.md 先提交 | SCN-002、003、008 已核准 | SCN-002、003、008 | 逐列走過狀態表：未合併的 `已完成` 不會命中任何結案列；fixture 的未合併組確實不是 main 的祖先（以 git 確認）；判準在 S2 前提交 | ✅ 2026-11-20 docs/AGENTS.md「有特殊意義的狀態值」改為只寫階段（SCN-001 的權威定義一併寫在這裡）、`已完成` 與合併前已知要等待的 `等待外部驗收窗` 在合併前寫好；工作流程第 3 項 Timeline 不記合併；文件版本 2.15、契約 2.7。dev-cycle：`已完成` 結案列限「不經合併的結案依據」、`等待外部驗收窗` 列限已合併或不經合併，表下一段寫明分支上未合併的終態依下方各列判定、回報待合併；推進步驟 3、5 寫明終態在保存 PASS 報告或記錄建議結論的提交寫好。readme-templates 檔尾說明原本寫「不要預先寫成已完成」，與新語意衝突，提前在本步改寫（其餘範本留在 S3）。逐列走過：未合併的 `已完成` 不命中「PR 已 merged」兩列、不修復列、不經合併的結案列與等待列，落到審查與 PR 的 gate，最後是 create-pr 或等待合併；已合併的命中「PR 已 merged」。懸置掃描在主幹讀到的 `已完成` 已經過合併，偵測規則不用改。[s1-fixture](evidence/s1-fixture.txt)：wf38 的分支不是 main 的祖先（exit=1）、wf38b 是（exit=0），三組 `verify-artifact.py` 對 H1 都判 OK，部署的 docs 為契約 2.7。判準 [expected.md](fixtures/expected.md) 與本步驟同一提交。`scripts/skill-hashes.txt` 依 check-kit 要求重產 |
| S2 | 隔離設定實跑 WF-38 兩組、WF-39，各 2 輪 | S1 | SCN-002、003 | WF-38 未合併組 2／2 回報待合併、不宣稱結案、不改檔；已合併組 2／2 直接結案、不要求補提交；WF-39 2／2 在分支上的記帳提交寫好 `已完成`，verify-artifact 判有效。未達成時修正文字後重跑，記錄每一輪 | ✅ 2026-11-20 kit `250441c`，隔離設定，三組同時跑、每輪重新產生 fixture。wf38（未合併）[r1](evidence/s2-wf38/wf38-r1.md)、[r2](evidence/s2-wf38/wf38-r2.md) 2／2 通過：都以 git 查到 main 沒有含 issue-3601 的 merge commit，回報「待合併」並說明欄位寫的已完成要合併後才算數，沒有改檔或提交。wf38b（已合併）[r1](evidence/s2-wf38/wf38b-r1.md)、[r2](evidence/s2-wf38/wf38b-r2.md) 2／2 通過：都依 merge commit 回報已結案，沒有要求補提交或補合併日期（r1 另提醒可刪除已合併的本機分支）。四輪的工作樹雜湊變化只來自被忽略的 `__pycache__/`，解讀見 [expected.md](fixtures/expected.md) 末節。wf39 [r1](evidence/s2-wf38/wf39-r1.md)、[r2](evidence/s2-wf38/wf39-r2.md) 2／2 通過：都在分支上新增一個只改 `**狀態**` 為 `已完成` 的提交，對 H1 執行 `verify-artifact.py` 判 OK，main 未動、Timeline 沒有新增合併列。附註：wf38-r2 的 agent 沒有執行 verify-artifact（它判斷腳本在允許路徑外），改為手動對照規則；隔離設定沒有語言偏好，wf39 兩輪以英文回報 |
| S3 | rules 中英版的通用原則；readme-templates、document-types、issue-checklist 的狀態說明、概述、影響欄與 Timeline 欄位；WF-40 fixture 與 expected.md 先提交 | SCN-001、004、005 已核准 | SCN-001、004、005 | check-kit 的雙語章節對應通過；範本不再出現負責人欄與帶合併事件的狀態範例；判準在 S4 前提交 | ✅ 2026-11-20 rules 中英版第六節「外部狀態以實查為準」之後各加一段「會變的進度只寫在一處」：進度記在一個地方、其他地方指向它，開頭的說明或警示只寫規則，某一項做完只更新記錄進度的那一處。readme-templates 兩份範本：概述的佔位字寫明進度只記在 `**狀態**` 與任務清單；Timeline 只有日期與異動兩欄，註解改為合併時間以 Git 為準。document-types「議題概述」、issue-checklist 的 Timeline 項同步；docs/AGENTS.md「待確認事項」寫明結論在狀態欄、影響欄只寫影響與關聯驗收編號，修訂紀錄 2.15 補上這些變更。check-kit 通過（雙語章節數一致）；`grep -n '負責人\|併入 main）' docs/agents/readme-templates.md docs/AGENTS.md` 沒有任何符合的行。WF-40 fixture（wf40、wf40b）與判準 [expected.md](fixtures/expected.md)「WF-40」與本步驟同一提交 |
| S4 | 隔離設定實跑 WF-40 兩組，各 2 輪 | S3 | SCN-001、005 | 部署組 2／2 的 `**狀態**` 沒有寫進部署情況；描述檔組 2／2 只改待辦表那一列，開頭警示不寫進度 | ✅ 2026-11-20 部署組達成、描述檔組未達成（1／2），使用者決定照實記錄並進 S5。三次實跑，判準與每次的修改見 [expected.md](fixtures/expected.md) 的 WF-40 各節。第一次（kit `c4fc58c`，[s4-wf40](evidence/s4-wf40/)）：wf40 1／2，r2 把測試環境的部署只記在 Timeline，理由是外部狀態表每列都要有查證命令；wf40b 0／2，兩輪都把開頭改成新的進度。修改 rules 中英版（開頭寫著進度時改成只剩規則）與 document-types 外部狀態表（取不到查證命令時仍列一列、註明來源）後重跑（kit `ee27b3c`，[s4-wf40-rerun](evidence/s4-wf40-rerun/)）：wf40 2／2，兩輪的 `**狀態**` 都維持「已完成」、概述沒動，測試環境與正式環境都列進 `## 現況`，測試環境的查證命令欄寫「未登記」；wf40b 0／2，開頭改成「A 已於 2026-11-20 執行完成；B、C 還沒執行」。rules 這段的粗體開頭改成「更新進度時，進度只留在一處」並加逐段檢查的完成判準後，只重跑 wf40b（kit `159078f`，[s4-wf40-rerun2](evidence/s4-wf40-rerun2/)）：r2 通過，引用規則把開頭改成「每一項確認後才動手，進度見待辦表」；r1 仍改成「A 已於 2026-11-20 執行；B、C 還沒執行」。五輪的 wf40b 都讀到這一段（fixture 的 AGENTS.md 經 CLAUDE.md 匯入），失敗的輪次都回報「A 做完後這句就不對了」。SCN-005 的 rules 段落只部分有效，S6 在 rule-verification-status 與 CHANGELOG 照實寫明 |
| S5 | acceptance.md、review-evidence.md 的核准 commit 寫法；verify-artifact.py 接受帶反引號或附註的 `待提交`；test-evidence.py 正負向案例 | SCN-006、007 已核准 | SCN-006、007 | 新增案例：`待提交`（反引號）與「待提交（附註）」回填祖先 SHA 判有效；回填後代、不存在的 SHA、由 SHA 改成其他值都判無效；既有案例全部通過 || ✅ 2026-11-20 test-evidence.py 新增三個案例（各在流程契約 2.4、2.5、2.3、無契約四組執行；2.3 以下照舊判需 2.4）：`待提交`、`待提交（實作提交時回填）`、`` `待提交`（實作提交時回填） `` 三種寫法回填核准提交或被審查提交判有效；三種寫法回填後代或不存在的 SHA 判無效；一般 `待提交` 回填後代判無效。由 SHA 改成其他值沿用既有 `test_approval_sha_replaced_invalid`。紅燈：改 verify-artifact.py 前 8 個子案例失敗，都是帶反引號的兩種寫法（不帶反引號的附註本來就以 `startswith` 通過）；修正為比對前去掉開頭的反引號後，`python3 scripts/test-evidence.py` 308 項全數通過。acceptance.md：核准 commit 只寫目前基線、重新核准時覆寫並把舊基線記在 Timeline，合併後仍是 `待提交` 屬正常、以推導命令取得；review-evidence.md 第 47 行、readme-templates 兩處佔位字同步；docs/AGENTS.md 修訂紀錄 2.15 補上。review 技能變更後重產 `scripts/skill-hashes.txt`，五項檢查通過 |
| S6 | workflow-regression 新增 WF-38～40；rule-verification-status；CHANGELOG（未發布）；usage.md 有語意落差才改；跑根目錄五項檢查 | S2、S4、S5 | SCN-001～008 | 五項檢查通過；CHANGELOG 寫明未實跑的部分 || ✅ 2026-11-20 workflow-regression 新增 WF-38～40 與 issue #11 實跑的結果連結（wf40b 寫明未達標）；rule-verification-status 新增「未發布」一節八列，rules 的進度一處段落記為「已實跑，不穩定（三版文字 6 輪 1 輪通過）」，範本、核准 commit 寫法與流程契約相容性記為僅靜態撰寫；CHANGELOG `[未發布]` 寫明變更、WF-40 平台 issue 描述組未達標、基準組沒有跑、未實跑的分支與下游試用待做；usage.md 等待合併段補一句流程契約 2.7 起審查通過就在分支上寫 `已完成`、結案以合併判定為準（README.md、INSTALL.md 沒有相關敘述）。五項檢查通過 |
| S7 | 送獨立審查（工具呼叫上限 30 次，固定檢查清單：狀態表的結案列、完成條件、雙語 rules 語意、verify-artifact 的負向案例、相容性） | S6 | SCN-001～008 | PASS，或已依使用者決定處理 || 🔄 2026-11-20 第一輪 [review-67e37e0](review-67e37e0.md) RETURN：M1（需決策）分支上未合併的等待窗口一律回報待合併，會跳過合併前就能做的觀察，2.6 以下也受影響；S1 合併後才需要的提交沒有定義；S2 懸置掃描沒指定讀哪個分支；S3 合併判定認不出快轉合併；S4 SCN-005 未記豁免；N1～N3。使用者決定 M1 照舊支援合併前的觀察窗、以窗口是否依賴合併區分，S4 記為豁免。修正（`c689f6d`、`68651d2`）：dev-cycle 等待列只對窗口要等合併的等待另加合併條件（流程契約 2.7 起），合併判定指向 pending-scan 的預設順序；推進步驟 5 與 docs/AGENTS.md 統一為「保存報告的提交或之後的記帳提交」，合併後才需要的提交同時更新狀態；pending-scan 讀目標分支的 README、預設合併判定加上 Reviewed HEAD 是目標分支的祖先；README 新增 Gate 豁免紀錄；test-evidence 補帶反引號的 SHA 改成其他值（N3）。新增 WF-41（[s7-wf41](evidence/s7-wf41/)，判準先提交）：wf41（窗口合併前就會到）2／2 回報下一步執行觀察，wf41b（窗口要等合併）2／2 回報待合併，四輪都沒改檔。wf41 r1 另指出合併前做完觀察後證據寫進計畫會讓 PASS 失效，屬既有行為、不在本 issue 範圍。workflow-regression、rule-verification-status、CHANGELOG 同步。增量覆審 [review-6681a19](review-6681a19.md) RETURN：M1 合併前觀察完成後的寫法會讓 PASS 失效的提交寫成 `已完成`，第 5 項與 SCN-002 有落差；S1（需決策）窗口是否要等合併沒有記錄依據；S2 懸置掃描排除了合併前的等待；S3 CHANGELOG 舊說法；N1～N3。使用者決定：只有沒有待觀察項目時才在合併前寫 `已完成`，有待觀察項目照原規則處理（SCN-002 修訂並重新核准，新基線 `03d474c`）。修正（`03d474c`、`1a8a18a`）：dev-cycle 等待列還原成與 BASE 相同，表下段落只談 `已完成`；第 5 項與 docs/AGENTS.md 兩列、修訂紀錄、CHANGELOG 改為有待觀察項目時合併前不寫終態，合併後記錄觀察證據的提交同時寫 `已完成`；pending-scan 只把目標分支還不包含的 `已完成` 視為非終態。[s7-wf42](evidence/s7-wf42/)（判準先提交）：wf41 重跑 2／2 回報下一步執行觀察，兩輪都指出證據寫進計畫會讓 PASS 失效；WF-42 2／2 維持「審查通過」、不合併、不標 S3 完成。待增量覆審 |
| S8 | 發布前以候選版在一個下游實際 issue 試用，至少走到審查通過後寫好終態與合併；結果記在 README `## 現況` | S7 | SCN-002、003 | 試用回報記錄終態寫在哪個提交、合併後有沒有補提交、dev-cycle 的結案判讀 | 📝 |
