#!/bin/bash
# 下游試用：在下游 issue 的 worktree 開一個載入 kit 候選版技能的 Claude Code session。
# 做法與 docs 放法的選擇見 docs/workflow-regression.md「下游試用」。
#
# 用法：cd <下游 issue worktree> && bash <kit>/scripts/trial-session.sh <候選版 SHA> [claude 參數…]
#
# - 技能取自 `git archive <SHA>`，與 kit 工作區的狀態無關；重開機或重開 session 時以同一個 SHA 重跑。
# - 只有 kit 的技能換成候選版；全域 CLAUDE.md、settings、記憶（projects）、其他技能、plugins、hooks 與 MCP 照常。
#   技能目錄解參照複製（symlink 的技能變成複本，斷掉的連結略過），候選版只寫進設定目錄。
#   CLAUDE.md、settings、projects、plugins、hooks 以 symlink 共用，~/.claude.json 用複本：腳本本身不修改
#   原本的 ~/.claude 與 ~/.claude.json，但 session 執行中對共用檔案（記憶、settings 等）的寫入會進原檔。
# - 試用目錄 ~/.cache/dev-rules-kit/trial-<SHA 前 7 碼>-XXXX 重開機不會被清掉，底下有設定目錄 .claude/
#   （CLAUDE_CONFIG_DIR）與解出的候選版 kit/，下游以 kit/scripts/init-project.py 更新 docs；
#   試用結束後刪除整個試用目錄（腳本會印出路徑）。中途失敗時刪除這次建的試用目錄，不啟動 claude。
# - 只支援 Claude Code。
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法：bash $0 <候選版 SHA> [claude 參數…]" >&2
  exit 2
fi
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if ! SHA=$(git -C "$KIT" rev-parse --verify --quiet "$1^{commit}"); then
  echo "停止：$1 不是 $KIT 裡的提交" >&2
  exit 1
fi
shift

ROOT="$HOME/.cache/dev-rules-kit"
mkdir -p "$ROOT"
SP=$(mktemp -d "$ROOT/trial-${SHA:0:7}-XXXX")
trap 'rm -rf "$SP"' EXIT
C="$SP/.claude"
mkdir "$SP/kit" "$C" "$C/skills"
git -C "$KIT" archive "$SHA" | tar -x -C "$SP/kit"

# cp -a 會保留 symlink：install.sh 會順著連結把候選版寫到原處，相對連結搬過來也會斷掉
shopt -s nullglob dotglob
for s in "$HOME/.claude/skills"/*; do
  if [ ! -e "$s" ]; then
    echo "略過斷掉的連結：$s" >&2
    continue
  fi
  cp -RL "$s" "$C/skills/"
done
shopt -u nullglob dotglob
# 只在這一步改 HOME：install.sh 把 kit 技能裝進 $SP/.claude/skills，不碰原本的 ~/.claude
HOME="$SP" bash "$SP/kit/scripts/install.sh" claude >/dev/null

for f in CLAUDE.md settings.json settings.local.json .credentials.json keybindings.json projects plugins hooks; do
  if [ -e "$HOME/.claude/$f" ]; then
    ln -s "$HOME/.claude/$f" "$C/$f"
  fi
done
if [ -e "$HOME/.claude.json" ]; then
  cp "$HOME/.claude.json" "$C/.claude.json"
fi

trap - EXIT
echo "候選版 kit：$SHA"
echo "設定目錄：$C"
echo "試用結束後刪除：$SP"
echo "更新下游 docs：python3 $SP/kit/scripts/init-project.py --update <下游專案路徑>"
exec env CLAUDE_CONFIG_DIR="$C" claude "$@"
