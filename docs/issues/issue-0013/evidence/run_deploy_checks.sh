#!/bin/bash
# issue #13 的暫存專案驗證：上一版 kit 初始化後以候選版更新（AC-1、AC-2），以及只建 project.md 的輕量步驟（AC-3）。
# 用法：bash run_deploy_checks.sh <kit repo> <上一版 SHA> <候選版 SHA> <暫存目錄（不存在）>
# 每條命令先印成 `$ 命令` 再印輸出與 exit code；kit 以 git archive 取出，不讀工作區。
set -u
REPO=$1; OLD=$2; NEW=$3; T=$4
mkdir "$T" || exit 1
run() { echo "\$ $*"; "$@"; echo "[exit $?]"; }
echo "上一版 kit：$(git -C "$REPO" rev-parse "$OLD")"
echo "候選版 kit：$(git -C "$REPO" rev-parse "$NEW")"
mkdir "$T/old" "$T/new"
git -C "$REPO" archive "$OLD" | tar -x -C "$T/old"
git -C "$REPO" archive "$NEW" | tar -x -C "$T/new"
OLDK=$T/old; NEWK=$T/new

echo; echo '## p1：上一版初始化 → 候選版更新（AC-1、AC-2）'
mkdir "$T/p1"; cd "$T/p1" && git init -q
run python3 "$OLDK/scripts/init-project.py" .
run python3 "$NEWK/scripts/init-project.py" . --update --dry-run
run python3 "$NEWK/scripts/init-project.py" . --update
run python3 "$NEWK/scripts/init-project.py" . --check
run grep -n '^## 修訂紀錄' docs/AGENTS.md
run grep -n '^\*\*文件版本\*\*\|^\*\*流程契約\*\*\|CHANGELOG' docs/AGENTS.md
run cmp docs/agents/project.md "$OLDK/docs/agents/project.md"

echo; echo '## p2：輕量步驟只建 project.md → 之後完整初始化（AC-3）'
mkdir "$T/p2"; cd "$T/p2" && git init -q && mkdir -p docs/agents
echo '$ [ -e docs/agents/project.md ] || cp <候選版>/docs/agents/project.md docs/agents/project.md'
[ -e docs/agents/project.md ] || cp "$NEWK/docs/agents/project.md" docs/agents/project.md; echo "[exit $?]"
echo '$ echo "自訂：測試命令 make test" >> docs/agents/project.md'
echo '自訂：測試命令 make test' >> docs/agents/project.md
run ls docs/agents
run python3 "$NEWK/scripts/init-project.py" . --dry-run
run python3 "$NEWK/scripts/init-project.py" .
run python3 "$NEWK/scripts/init-project.py" . --check
run tail -1 docs/agents/project.md

echo; echo '## p3：輕量步驟遇到已存在的 project.md 不覆蓋（AC-3）'
mkdir -p "$T/p3/docs/agents"; cd "$T/p3"
echo '$ printf "# 既有的專案規範\n" > docs/agents/project.md'
printf '# 既有的專案規範\n' > docs/agents/project.md
echo '$ [ -e docs/agents/project.md ] || cp <候選版>/docs/agents/project.md docs/agents/project.md'
[ -e docs/agents/project.md ] || cp "$NEWK/docs/agents/project.md" docs/agents/project.md; echo "[exit $?]"
run cat docs/agents/project.md

echo; echo '## p4：已整套部署的專案，可移除清單取自 manifest 的 files（AC-3 修訂）'
mkdir "$T/p4"; cd "$T/p4" && git init -q
run python3 "$NEWK/scripts/init-project.py" .
echo '$ printf "# 專案地雷\n" > docs/agents/pitfalls.md'
printf '# 專案地雷\n' > docs/agents/pitfalls.md
echo '$ python3 -c "列出 docs/.dev-rules-kit.json 的 files"'
python3 -c "import json;print('\n'.join(json.load(open('docs/.dev-rules-kit.json'))['files']))"; echo "[exit $?]"
run ls docs/agents
