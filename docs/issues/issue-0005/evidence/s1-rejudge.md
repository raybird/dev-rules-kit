# AC-2 重判：以本分支 HEAD 的 verify-artifact.py 判定實跑保留的 agent 記帳提交（2026-11-12）

## issue-#4-wf28b3

```text
$ python3 skills/review/scripts/verify-artifact.py --repo <scratchpad>/runs-i4/f28/wf28b3 --reviewed 84a544b --head HEAD --artifact docs/issues/issue-2802/review-84a544b.md
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-2802/review-84a544b.md、Timeline、待確認事項、現況、現行 review（（無） → review-84a544b.md）
exit 0
```

## issue-#3-最後一輪-wf31

```text
$ python3 skills/review/scripts/verify-artifact.py --repo <scratchpad>/runs12/cand/wf31 --reviewed b2bfb79 --head HEAD --artifact docs/issues/issue-3101/review-b2bfb79.md
OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：新增報告 docs/issues/issue-3101/review-b2bfb79.md、現況、現行 review（（無） → review-b2bfb79.md）
exit 0
```

