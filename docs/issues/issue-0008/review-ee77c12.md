# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：c0c7e9f17cbc14a96bd8f28425b910a27be2d3f9
- Reviewed HEAD SHA：ee77c1270dc97238a7200be1495195c825e4ecc2
- Reviewed patch-id：21a3f901ae7d90a37a3ea2686190e51f730a859b（已用 `git diff c0c7e9f ee77c12 | git patch-id --stable` 重算，結果相同）
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0008/review-ee77c12.md

## 問題與風險
- **MUST FIX**：無
- **SHOULD FIX**：`CHANGELOG.md:37`。「下游更新」第二點說要「把該檔換回上一版 kit 的原文後更新」，這只在專案的部署基線剛好是 v4.12.0 時才行得通。`--update` 比對的是基線記錄的雜湊，不是「上一版」的雜湊。我在 scratchpad 實測：用 c0c7e9f 之前的版本（ab1e901）初始化，改寫 document-types.md，再照條目換回 c0c7e9f 的原文，`--update` 仍然判為衝突（rc=1）。改成換成本版 kit 的 document-types.md 原文就能成功（rc=0）。建議改寫成「把改寫的內容移到 project.md『本地 gate 與案例』，再把 document-types.md 換成本版 kit 的原文後執行 `--update`」，這個做法不受基線版本影響。實際影響很小：rule-verification-status 記錄本機 7 個下游都沒改過這份檔，但這是給下游照做的步驟，寫錯了照做就會失敗。
- **SHOULD FIX**：`docs/usage.md:13`。「首次部署建立核心規範、範本、`docs/agents/project.md` 與部署基線」裡的「範本」，指的就是 `docs/_templates/`。這句是 6b2b57f（v4.0.0）寫的，當時 init-project.py 會部署 `_templates`，project.md 另外列出，readme-templates.md 則屬於核心規範。本次變更後這句已經不對了，S2～S4 證據寫「docs/usage.md 沒有引用，不需修改」，只用 `grep _templates` 查，沒有覆核敘述的意思（AGENTS.md 維護規範：check-kit 不驗證敘述語意）。建議把「範本、」刪掉。
- **NICE TO HAVE**：無

（這兩項 SHOULD FIX 若要修，提交會讓本 PASS 失效，需要重新審查。）

## 已查核維度
- **驗收與證據**：
  - SCN-001：`scripts/test-install.py:162-165` 斷言 `docs/_templates` 不存在，基線條目剛好是 `docs/AGENTS.md` 加 6 份 `docs/agents/` 核心檔；後面重跑初始化、`--check` 回 0。成立。
  - SCN-002：`test_update_from_baseline_with_templates` 涵蓋 dry-run 不改檔案樹與基線、`--update` 後三份舊檔逐位元組不變、基線不含 `_templates` 條目、`--check` 回 0。我另外用 c0c7e9f 舊 kit 實際初始化出 v4.12.0 形狀的專案，走 dry-run → update → check，三份檔 sha256 不變，條目從 3 筆變 0 筆。成立。
  - SCN-003：`git diff -M --stat` 顯示三份範本是 0 行增減的改名。`install.sh:153-157` 用 `cp -r` 複製整個技能目錄，references/ 會一起安裝。`docs/AGENTS.md:186` 有那句 pointer；除了 CHANGELOG、`docs/issues/`、腳本註解與測試以外，`git grep _templates` 沒有其他引用。成立；只是上面的 usage.md「範本」是沒有寫出 `_templates` 字樣的語意殘留。
  - SCN-004：`docs/agents/document-types.md:114-115` 已沒有「應客製」，並指向 project.md「本地 gate 與案例」。diff 不含 project.md，PAST_TEMPLATES 不必加。成立。
  - SCN-005：`CHANGELOG.md:36` 涵蓋兩點：不再部署、舊檔不刪、可以手動刪除；刪除前先查專案自己的文件有沒有引用。成立。另外加寫的第 37 行步驟不準確，見 SHOULD FIX。
  - SCN-006：`skills/execute-task/SKILL.md:21` 回寫步驟寫明「新建時可參考本技能 `references/` 的架構、領域與修訂紀錄範本」。成立。
  - issue README 在分支上的變更只有核准 commit 回填、Timeline 與狀態，屬記帳性質。
- **紅燈真實性（s1-red.txt）**：兩個失敗都對得上舊程式的實際行為。第一個是舊程式會部署 `_templates`，所以目錄存在。第二個是舊程式把清單裡的 `_templates` 與基線雜湊比對，雜湊相符、內容和 kit 不同，就列入 pending 並覆蓋，第 233 行的斷言失敗訊息與此相符。
- **斷言會不會假綠**：如果改成刪除舊檔，`read_bytes` 會拋例外；如果條目留在基線，`assertEqual([...], [])` 會失敗；如果 dry-run 寫了基線，manifest 的位元組比較會失敗。dry-run 的檔案樹只比對檔名，但這個案例裡核心檔沒有待更新的，唯一可能寫入的只有 manifest，而它已經逐位元組比對，沒有假綠的空間。初始化案例改成精確比對基線條目清單，之後新增 `docs/agents/` 檔案要同步改測試，這是刻意的耦合，可以接受。
- **相關失敗面（init-project.py 舊基線形狀，scratchpad 實測）**：

  | 舊基線與磁碟的組合 | 指令 | 結果 | 判定 |
  |---|---|---|---|
  | 條目在、檔案與範本相同 | dry-run、update、check | dry-run 不寫入；update 後條目清掉、檔案保留；check OK | 正確 |
  | 條目在、檔案已刪除 | update、check | OK，條目清掉 | 正確 |
  | 條目在、檔案改過內容 | update | OK，修改保留。舊程式在這裡會判為衝突，新程式不再擋 | 正確，屬改善 |
  | 條目在、`_templates` 是 symlink | update | OK，沒有寫入連結的目標 | 正確 |
  | 條目在、`_templates` 是一般檔案 | update | OK | 正確 |
  | 條目在、核心落後 | `--check` 或不加 `--update` 的初始化 | 回 1、不寫入，條目保留到下次寫入基線 | 正確，與 CHANGELOG「下次寫入基線時移除」相符 |

  程式只把清單內的檔案拿來比對，`previous` 多出的鍵不會造成例外或誤判。沒有找到會出錯的其他形狀。
- **根目錄五項檢查（在 HEAD ee77c12、工作樹乾淨下執行）**：check-kit OK、check-links OK、`bash -n` OK、test-install 16 項 OK、test-evidence 296 項 OK。
- **文件一致性**：
  - `docs/AGENTS.md:19` 的部署說明已改。第 21 行「已移除的上游檔案不自動刪除，依版本說明處理」與 CHANGELOG 一致。
  - 文件版本 2.12、修訂紀錄一列、日期 2026-11-17 都正確。
  - 流程契約維持 2.5 合理：沒有技能或 gate 依賴 `_templates`；新版 docs 配舊技能時，pointer 指向的範本不存在，但那句是「可參考」，不影響任何 gate。
  - document-types.md 的 Mermaid 那句改寫恰當。
  - project.md 四節中，「本地 gate 與案例」是最接近的落點，但該節說明（`docs/agents/project.md:19`）沒有提到文件組合。SCN-004 規定不動 project.md，所以接受現狀。
  - README.md、INSTALL.md、skills/README.md 沒有需要跟著改的敘述。
- **CHANGELOG 4.13.0 與 rule-verification-status**：變更項目與實際 diff 相符。rule-verification-status 三列的狀態用語與既有詞彙一致；第一列標「本地測試驗證」並附先紅後綠來源，正確；另兩列照實標為僅靜態撰寫。
- **需求、架構、安全、品質**：init-project.py 的改動是最小改法，已直接列出 `docs/agents`，沒有留下只剩一個元素的迴圈。test-install.py 把 `hashlib` 移到檔頭，消除了重複 import。pointer 在 docs/AGENTS.md 與 SKILL.md 各寫一次，是使用者在 TBD-1 決定的，不算多餘的重複。沒有過度設計，也沒有安全面的變化：不再對 `_templates` 做任何寫入。

## 豁免、待確認與限制
- 沒有豁免。TBD-3（發布前的下游試用）屬於審查之後的步驟，不在本次範圍。
- agent 在新建常青文件時會不會讀到 references/ 的範本，靜態審查無法證明，計畫已標為由下游試用觀察。
- 工具呼叫用量：約 16 次，未超過 30 次上限，固定清單 1～7 項都查完了。所有暫存專案都建在 實作 session 的 scratchpad（review8 子目錄），沒有碰任何真實的下游專案。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
