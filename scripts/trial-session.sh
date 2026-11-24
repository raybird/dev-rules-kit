#!/bin/bash
# 下游試用：在下游 issue 的 worktree 開一個載入 kit 候選版技能的 Claude Code session。
# 做法與 docs 放法的選擇見 docs/workflow-regression.md「下游試用」。
#
# 用法：cd <下游 issue worktree> && bash <kit>/scripts/trial-session.sh <候選版 SHA> [claude 參數…]
#
# - 技能取自 `git archive <SHA>`，與 kit 工作區的狀態無關；重開機或重開 session 時以同一個 SHA 重跑。
# - 只有 kit 的技能換成候選版；全域 CLAUDE.md、settings、記憶（projects）、其他技能、plugins、hooks 與 MCP 照常。
#   ~/.claude 底下的檔案以 symlink 共用，~/.claude.json 用複本，原本的設定不被修改。
# - 設定目錄在 ~/.cache/dev-rules-kit/trial-<SHA 前 7 碼>-XXXX，重開機不會被清掉；
#   解出的候選版 kit 在同一層的 kit/，下游以它的 scripts/init-project.py 更新 docs。
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
C="$SP/.claude"
mkdir "$SP/kit" "$C"
git -C "$KIT" archive "$SHA" | tar -x -C "$SP/kit"

if [ -d "$HOME/.claude/skills" ]; then
  cp -a "$HOME/.claude/skills" "$C/skills"
fi
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

echo "候選版 kit：$SHA"
echo "設定目錄：$C"
echo "更新下游 docs：python3 $SP/kit/scripts/init-project.py --update <下游專案路徑>"
exec env CLAUDE_CONFIG_DIR="$C" claude "$@"
