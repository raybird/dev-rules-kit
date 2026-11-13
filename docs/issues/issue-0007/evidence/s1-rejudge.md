# AC-4 重判：main 與本分支的 verify-artifact.py 判定比較（2026-11-12；依 review-a77b097、review-d49e8fc 修正後 2026-11-13 重跑）

每個案例先跑 main 版（`81368f7`，含 #5），再跑本分支版，比較 exit code 與輸出。下游試用的 repo 與 issue 目錄以 `<downstream>`、`issue-{下游}` 遮蔽。

## issue-#4-wf28b3

```text
$ verify-artifact.py（main）--reviewed 84a544b --head HEAD
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-2802/review-84a544b.md、Timeline、待確認事項、現況、現行 review（（無） → review-84a544b.md）
$ verify-artifact.py（branch）--reviewed 84a544b --head HEAD
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-2802/review-84a544b.md、Timeline、待確認事項、現況、現行 review（（無） → review-84a544b.md）
```

## issue-#3-wf31

```text
$ verify-artifact.py（main）--reviewed b2bfb79 --head HEAD
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-3101/review-b2bfb79.md、現況、現行 review（（無） → review-b2bfb79.md）
$ verify-artifact.py（branch）--reviewed b2bfb79 --head HEAD
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-3101/review-b2bfb79.md、現況、現行 review（（無） → review-b2bfb79.md）
```

## 下游試用第-1-輪

```text
$ verify-artifact.py（main）--reviewed 778ed0c --head fd7d78e
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-778ed0c.md、現況、現行 review（（無） → review-778ed0c.md）
$ verify-artifact.py（branch）--reviewed 778ed0c --head fd7d78e
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-778ed0c.md、現況、現行 review（（無） → review-778ed0c.md）
```

## 下游試用第-2-輪

```text
$ verify-artifact.py（main）--reviewed c71e203 --head f24d589
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-c71e203.md、現況、現行 review（review-778ed0c.md → review-c71e203.md）
$ verify-artifact.py（branch）--reviewed c71e203 --head f24d589
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-c71e203.md、現況、現行 review（review-778ed0c.md → review-c71e203.md）
```

## 下游試用第-3-輪

```text
$ verify-artifact.py（main）--reviewed aacbacc --head e0908f4
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-aacbacc.md、現況、現行 review（review-c71e203.md → review-aacbacc.md）
$ verify-artifact.py（branch）--reviewed aacbacc --head e0908f4
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-aacbacc.md、現況、現行 review（review-c71e203.md → review-aacbacc.md）
```

## 下游試用第-4-輪

```text
$ verify-artifact.py（main）--reviewed b38af46 --head 086fb3e
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-b38af46.md、現況、現行 review（review-aacbacc.md → review-b38af46.md）
$ verify-artifact.py（branch）--reviewed b38af46 --head 086fb3e
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-b38af46.md、現況、現行 review（review-aacbacc.md → review-b38af46.md）
```

## 下游試用第-4-輪最後的記帳提交

```text
$ verify-artifact.py（main）--reviewed b38af46 --head 5410c8a
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-b38af46.md、Timeline、待確認事項、現況、現行 review（review-aacbacc.md → review-b38af46.md）
$ verify-artifact.py（branch）--reviewed b38af46 --head 5410c8a
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-b38af46.md、Timeline、待確認事項、現況、現行 review（review-aacbacc.md → review-b38af46.md）
```

## 下游試用寫入規定以外狀態值的記帳提交（之後已改正）

```text
$ verify-artifact.py（main）--reviewed b38af46 --head f3eeac8
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-b38af46.md、Timeline、待確認事項、現況、現行 review（review-aacbacc.md → review-b38af46.md）
$ verify-artifact.py（branch）--reviewed b38af46 --head f3eeac8
exit 0
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-{下游}/review-b38af46.md、Timeline、待確認事項、現況、現行 review（review-aacbacc.md → review-b38af46.md）
提醒（不影響本次判定）：待確認事項 TBD-5「接受為殘餘風險（2026-11-12）：…」 的狀態不是規定的值；狀態欄以 `待確認`、`已解決`、`不影響本次交付` 之一開頭，後面可接結論。
```

