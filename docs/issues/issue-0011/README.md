# Issue 11 - 會變的狀態只寫一處，合併後不必回頭改 README

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #11](https://github.com/raybird/dev-rules-kit/issues/11)。2026-11-20 詢問五個下游專案，照 kit 流程寫出的文件裡，哪些內容沒人讀、沒有資訊量或會誤導。走 kit issue 流程的四個專案都回報：最會誤導的，是同一個狀態寫在好幾處、事後只更新其中一處。

- `**狀態**` 寫進「production 未部署」「待合併與發版」，部署或發版後沒人回頭改；有一個專案的 project.md 還拿這個欄位判斷是否已合併。
- 同一個狀態同時寫在檔尾 `**狀態**`、Timeline、`## 現況`、概述的「目前進度」、待確認事項的影響欄與交接文件，一次異動要改 3～5 處。
- `已完成` 只能在真的合併之後寫，所以每次合併後都要在主幹補 1～3 個收尾提交；沒補的專案，README 就一直停在「待合併」。
- `**核准 commit**` 被寫成一串歷次重新核准的 SHA；合併後仍是 `待提交` 時，讀者分不清是沒提交還是沒人回填。verify-artifact 只認不帶反引號的 `待提交`，agent 只好繞路，還把繞路經過寫進 Timeline。

沒走 kit issue 流程的第五個專案，在平台 issue 描述裡也有同一種問題：開頭寫「都還沒執行」，同一份待辦表已標已完成。根源是寫作習慣，kit 的範本把它放大了。

收錄依據（AGENTS.md「範圍」）：四個下游專案實際發生，project.md 登記解決不了範本與 dev-cycle 的結案語意。

不在範圍：審查報告累積與記帳提交數量（[#12](https://github.com/raybird/dev-rules-kit/issues/12)，本 issue 合併後再規劃）、下游部署內容瘦身（[#13](https://github.com/raybird/dev-rules-kit/issues/13)）。

## 現況

**現行 review**: review-e8daf73.md

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| `**狀態**` 的內容 | 自由描述，範例本身就在括號裡寫進合併事件 | 只寫階段，括號只放日期、SHA 這類錨定事件；部署、發版狀態不寫進來 |
| 何時寫 `已完成` | 真的合併之後，在主幹補提交 | 審查 PASS 後，分支上的記帳提交就寫好；合併後主幹自然正確，不補提交 |
| dev-cycle 判定結案 | 看到 `已完成` 且有結案依據就結案 | `已完成` 一律依合併判定確認；還沒合併就回報待合併 |
| 進度寫在哪 | 狀態、Timeline、概述、影響欄各寫一次 | rules 通用原則：進度只寫一處；kit 範本的概述與影響欄不寫進度，Timeline 去掉負責人欄 |
| `**核准 commit**` | 會累積成 SHA 串；合併後是 `待提交` 時意義不明 | 只寫目前基線；合併後是 `待提交` 屬正常，以推導命令取得；verify-artifact 接受帶反引號或附註的 `待提交` |

## 涉及檔案

- `rules/AGENTS.md`、`rules/AGENTS.zh-TW.md`：進度只寫一處的通用原則
- `docs/AGENTS.md`：「有特殊意義的狀態值」改為只寫階段、合併前寫好終態；工作流程第 3、6 項；文件版本 2.15、流程契約 2.7 與修訂紀錄
- `docs/agents/readme-templates.md`、`docs/agents/document-types.md`、`docs/agents/issue-checklist.md`：狀態說明、概述不寫進度、Timeline 欄位、核准 commit 的寫法
- `docs/agents/acceptance.md`、`docs/agents/review-evidence.md`：核准 commit 只寫目前基線、合併後的 `待提交`、可回填的寫法
- `skills/dev-cycle/SKILL.md`、`skills/dev-cycle/references/pending-scan.md`：結案判定與合併前寫好終態
- `skills/review/scripts/verify-artifact.py`、`scripts/test-evidence.py`：帶反引號或附註的 `待提交` 可以回填
- `docs/workflow-regression.md`、`docs/rule-verification-status.md`、`CHANGELOG.md`、`docs/usage.md`：回歸案例、驗證狀態與版本說明
- `docs/issues/issue-0011/`：本 issue 的規格、計畫與證據

## Gherkin 驗收劇本

```gherkin
Feature: 會變的狀態只寫一處，合併後不必回頭改 README

  @SCN-001
  Scenario: 狀態只寫階段
    Given 一個流程契約 2.7 的 issue，變更已部署到測試環境、尚未部署到正式環境
    When agent 更新 README 的 **狀態**
    Then **狀態** 只寫階段，括號裡只放日期、SHA 這類錨定事件
    And 不寫「未部署」「待發版」這類會被其他人或其他流程改變的狀態
    And 驗收需要觀察部署結果時，記為 等待外部驗收窗 並寫明窗口與判準
    And 只是要記錄部署情況時，寫在 ## 現況 的外部狀態表，附查證命令

  @SCN-002
  Scenario: 審查通過後在分支上寫好終態
    Given 完整交付範圍有有效 PASS，沒有待決定的建議，也沒有未豁免的待觀察項目
    When 協調者準備交付合併
    Then 保存報告的提交或之後的記帳提交，在分支上把 **狀態** 改成 已完成
    And 有未豁免的待觀察項目時合併前不寫終態，照原規則以 等待外部驗收窗 處理，合併後記錄觀察證據的提交同時寫 已完成
    And verify-artifact.py 判定有效，原 PASS 沿用
    And 合併後不在主幹補收尾提交，Timeline 不另記合併那一列

  @SCN-003
  Scenario: dev-cycle 以合併判定確認是否結案
    Given 分支上的 README **狀態** 為 已完成
    When dev-cycle 查詢或推進這個 issue
    Then 依 project.md 的合併判定確認是否已合併
    And 還沒合併時回報「待合併」階段，不宣稱結案、不改 README
    And 已經合併時直接結案，不要求補提交或補記合併日期
    And 懸置掃描不把主幹上的這種 已完成 列為缺少合併紀錄

  @SCN-004
  Scenario: issue 文件的進度不重複
    Given agent 依 kit 範本建立或更新 issue README
    When 寫概述、待確認事項與 Timeline
    Then 概述不寫「目前進度」，進度只由 **狀態** 與任務清單表示
    And 待確認事項的影響欄只寫影響與關聯驗收編號，不重複狀態欄的內容
    And 新範本的 Timeline 只有日期與異動兩欄，既有 README 不需要改

  @SCN-005
  Scenario: 平台 issue 與其他文件也只寫一處進度
    Given agent 撰寫的平台 issue 描述或文件，同時有開頭說明與待辦表
    When 某個待辦項目完成
    Then agent 只更新待辦表的那一列
    And 開頭說明或警示只寫規則（例如每項確認後才動手），不寫「都還沒執行」這類進度

  @SCN-006
  Scenario: 核准 commit 只寫目前基線
    Given 一個 Medium 風險的 issue，規格重新核准過
    When agent 更新 **核准 commit**
    Then 欄位只寫目前基線的一個 SHA，舊基線記在 Timeline
    And 回填只併進本來就要做的提交，不單獨提交
    And issue 合併後欄位仍是 待提交 時，reviewer 與 dev-cycle 以 acceptance.md 的推導命令取得基線，不回報為缺漏、不要求回填

  @SCN-007
  Scenario: 帶反引號或附註的待提交可以回填
    Given 被審查版本的 **核准 commit** 寫成 `待提交`（帶反引號）或「待提交（附註）」
    When 之後的記帳提交把它改成被審查提交或其祖先的 SHA
    Then verify-artifact.py 判定有效
    And 改成被審查提交的後代、不存在的 SHA，或由 SHA 改成其他值時，仍判需重新審查

  @SCN-008
  Scenario: 流程契約 2.6 以下的專案照舊
    Given 專案的 docs/AGENTS.md 是流程契約 2.6 以下
    When dev-cycle 或 review 處理該專案的 issue
    Then 照原規則運作，既有 README 不需要遷移
    And dev-cycle 看到 已完成 時同樣依合併判定確認
```

## Gherkin 核准紀錄
- **核准 commit**: 03d474c
- **核准來源**: 2026-11-20 對話：Q1～Q4 都選建議答案（狀態只寫階段、合併前先寫好、寫進 rules、只寫目前基線），列出 SCN-001～008 後使用者回覆「核准」；SCN-002 於 2026-11-20 增量覆審 review-6681a19 後修訂，使用者選「待觀察的 issue 照舊，只有沒有待觀察項目才在合併前寫已完成（建議）」（選項寫明需修改 SCN-002）

| Scenario | 核准日期 | 狀態 |
|---|---|---|
| SCN-001 | 2026-11-20 | 已核准 |
| SCN-002 | 2026-11-20 | 已核准 |
| SCN-003 | 2026-11-20 | 已核准 |
| SCN-004 | 2026-11-20 | 已核准 |
| SCN-005 | 2026-11-20 | 已核准 |
| SCN-006 | 2026-11-20 | 已核准 |
| SCN-007 | 2026-11-20 | 已核准 |
| SCN-008 | 2026-11-20 | 已核准 |

## 風險與首要驗證

- **最大風險**：`已完成` 改成合併前就寫，dev-cycle 把還沒合併的分支當成已結案（現行狀態表「狀態為已完成且有其他結案依據」那一列會直接放行），屬於不會報錯的假結案
- **風險等級與理由**：Medium。改變所有下游 dev-cycle 讀取的結案語意，但合併判定在 project.md 已有登記；失敗會讓 issue 停在未合併而被回報為完成，可由懸置掃描或下一次查詢發現，不損失資料
- **首要驗證**：先改 dev-cycle 狀態表與完成條件，以隔離設定實跑「分支上已寫已完成、尚未合併」的 fixture，對照組是已合併
- **選擇理由**：直接量測 agent 會不會只看欄位就結案；靜態審查看得出文字，看不出 agent 的判讀
- **完成證據**：未合併組 2／2 回報待合併、不宣稱結案、不改檔；已合併組 2／2 直接結案、不要求補提交；判準在實跑前提交

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|---|---|---|---|
| TBD-1 | review-67e37e0 M1：合併前就能觀察的等待窗口要不要照舊支援 | 已解決：2026-11-20 使用者選「照舊支援，以窗口是否依賴合併區分（建議）」，理由是 staging 驗證後才合併這類窗口在 2.6 已經支援（WF-23 對照二）；之後 dev-cycle 的等待列還原成 BASE，窗口類型只在第 5 項寫入時區分（見 TBD-2） | 未確認時，未合併、窗口已到的等待會跳過觀察直接回報待合併，使用者可能在觀察前合併；SCN-002、SCN-008 |
| TBD-2 | review-6681a19 S1：審查通過時還有待觀察項目，合併前要不要寫終態 | 已解決：2026-11-20 使用者選「待觀察的 issue 照舊，只有沒有待觀察項目才在合併前寫已完成（建議）」，理由是不必讓 agent 在讀取時判斷窗口類型，等待列可以維持 BASE；SCN-002 修訂並重新核准 | 未確認時，要等合併的窗口在合併前寫成等待會卡在等待列，合併前觀察完成後可能在 PASS 已失效的提交寫已完成；SCN-002 |
| TBD-3 | review-da37945 N2、N3：快轉到 Reviewed HEAD 但寫終態的記帳提交還沒進主幹時判已合併；推測的合併判定結案時沒註明 | 不影響本次交付：追蹤：無。2026-11-20 使用者選「不修，記理由（建議）」；懸置掃描讀主幹，會把前者列為已合併未結案，不是靜默錯誤；後者的誤判方向是看起來沒合併，偏安全 | 快轉合併的專案可能在主幹 README 還不是終態時被 dev-cycle 回報結案；SCN-003 |
| TBD-4 | review-004e551 N2、N3：本 README 關鍵差異「何時寫已完成」沒有待觀察項目的條件；readme-templates 與 usage.md 沒帶出要等合併的窗口維持實際階段 | 不影響本次交付：追蹤：無。2026-11-20 使用者選「不修，記理由（建議）」；前者是本 issue 內的變更摘要，規格修訂已記在 SCN-002、核准紀錄與計畫 S7；後者寫入終態時以 dev-cycle 第 5 項為準，誤讀時與 BASE 相同、不會假結案 | 讀者只看關鍵差異或範本時可能以為有待觀察項目也在合併前寫已完成；SCN-002 |
| TBD-5 | review-e8daf73 N1：計畫 S7 列漏了 review-004e551 的限制（dev-cycle 第 5 項新句子只靜態檢查，WF-42 在修改前跑） | 不影響本次交付：追蹤：無。2026-11-20 使用者選「不修，記理由（建議）」；未實跑的總清單在 CHANGELOG 與 rule-verification-status，只影響追溯 | 未確認時讀者可能以為 dev-cycle 第 5 項的新句子已實跑；SCN-002 |
| TBD-6 | review-e8daf73 N2：S8 完成時是否更新計畫 S8 列（更新會讓 PASS 失效） | 已解決：2026-11-20 使用者選「更新計畫並再審一次（建議）」，理由是只寫 `## 現況` 會讓計畫 S8 停在待辦、兩處進度不一致；S8 結果寫進 `## 現況` 並更新計畫 S8 列，之後做一次增量覆審 | 未確認時 S8 收尾可能只改一處，計畫與現況不一致；SCN-002、SCN-003 |
| TBD-7 | S8 下游專案 A：候選版 docs 必須放進下游交付分支，合併會把未發版的流程契約帶進主幹，revert 後分支回到舊契約、下一輪只能完整審查；verify-artifact 參數用錯時也回 INVALID | 不影響本次交付：追蹤：#11 合併後另開 kit issue。2026-11-23 使用者選「#11 合併後另開 kit issue（建議）」；這是試用方式與工具訊息的問題，不在本 issue 的狀態寫法範圍內 | 未處理時，下游試用候選版要在 revert 與帶進主幹之間二選一；SCN-002、SCN-003 的下游驗證受限 |
| TBD-8 | S8 下游專案 A：候選版 session 把狀態寫成「審查通過，待決定審查建議」，在階段後接下一步；「只寫階段」沒有明說這種寫法 | 不影響本次交付：追蹤：無。2026-11-23 使用者選「記成 TBD，不改規則（建議）」；本 issue 處理的是合併後會過時的外部狀態，這種後綴是 issue 內部的下一步，下一次記帳就會覆寫；之後若觀察到合併後仍殘留再修 | 狀態後綴在合併後殘留時，讀者可能誤以為還有工作沒做；SCN-001 |

## Gate 豁免紀錄

- 2026-11-20 使用者選「照實記錄，進 S5（建議）」，審查 review-67e37e0 後再確認「記為豁免（建議）」。範圍：SCN-005 的行為驗收（WF-40 wf40b 需 2／2，實際三版規則文字 6 輪 1 輪通過）；rules 的段落保留，rule-verification-status 與 CHANGELOG 寫明只部分有效。殘餘影響：下游 agent 更新進度時，仍可能把開頭的說明改寫成新的進度。

## Timeline

| 日期 | 異動 |
|------|------|
| 2026-11-20 | 依五個下游專案的唯讀回覆建立 issue 與 GitHub #11；使用者對 Q1～Q4 選建議答案，核准 SCN-001～008 |
| 2026-11-20 | 獨立審查 review-67e37e0：RETURN TO execute-task（M1 需決策） |
| 2026-11-20 | 增量覆審 review-6681a19：RETURN TO execute-task（S1 需決策） |
| 2026-11-20 | SCN-002 修訂並重新核准：有待觀察項目時合併前不寫終態；舊基線 0379d3e |
| 2026-11-20 | 增量覆審 review-da37945：PASS，附 SHOULD FIX 1 項、NICE TO HAVE 7 項 |
| 2026-11-20 | 增量覆審 review-004e551：PASS，附 NICE TO HAVE 3 項 |
| 2026-11-20 | 記錄 review-004e551 建議的結論：N1 補待確認事項的理由與影響，N2、N3 不修（TBD-4） |
| 2026-11-20 | 增量覆審 review-e8daf73：PASS，附 NICE TO HAVE 2 項 |
| 2026-11-20 | 記錄 review-e8daf73 建議的結論（TBD-5、TBD-6）；S8 下游試用選定兩個下游專案 |
| 2026-11-23 | S8：下游專案 A 中止試用（候選版 docs 放在交付分支會隨合併帶進主幹，使用者選合併前 revert）；試用結果於 S8 收尾時寫入計畫 |
| 2026-11-23 | 記錄下游專案 A 試用觀察的結論（TBD-7、TBD-8） |

---
**建立日期**: 2026-11-20  
**分級**: Medium — 規則、範本、dev-cycle 與一處判定腳本多檔修改，邏輯直接，不需 Phase／Task 拆解  
**風險**: Medium  
**狀態**: 審查通過
