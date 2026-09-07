#!/usr/bin/env bash
#
# dev-rules-kit 安裝腳本：把 rules / workflows / skills 複製到各平台的設定目錄。
#
# 路徑的真相來源是 rules/README.md、workflows/README.md、skills/README.md 的
# 「安裝方式」章節。修改本檔的 targets_for() 時必須同步那三份 README，
# scripts/sync-skills.py --check 會驗證兩邊一致。
#
# 用法：
#   bash scripts/install.sh                    # 自動偵測已安裝的平台並安裝 workflows + skills
#   bash scripts/install.sh opencode claude    # 只裝指定平台
#   bash scripts/install.sh --with-rules       # 另外安裝規則檔（會先備份既有檔案）
#   bash scripts/install.sh --dry-run          # 只列出會做什麼，不實際複製
#   bash scripts/install.sh --list             # 列出平台與對應路徑
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ALL_PLATFORMS=(claude windsurf antigravity opencode cursor)

WITH_RULES=0
RULES_LANG=zh
DRY_RUN=0
LIST_ONLY=0
SELECTED=()

# 各平台的偵測目錄：存在才視為已安裝該平台
base_dir_for() {
  case "$1" in
    claude)      echo "$HOME/.claude" ;;
    windsurf)    echo "$HOME/.codeium/windsurf" ;;
    antigravity) echo "$HOME/.gemini/config" ;;
    opencode)    echo "$HOME/.config/opencode" ;;
    cursor)      echo "$HOME/.cursor" ;;
  esac
}

# 目標路徑：<rules 目標檔>|<workflows 目標目錄>|<skills 目標目錄>
# "-" 代表該平台不以檔案方式安裝這類內容
targets_for() {
  case "$1" in
    claude)      echo "-|-|$HOME/.claude/skills" ;;
    windsurf)    echo "$HOME/.codeium/windsurf/memories/global_rules.md|$HOME/.codeium/windsurf/global_workflows|$HOME/.codeium/windsurf/skills" ;;
    antigravity) echo "$HOME/.gemini/config/AGENTS.md|$HOME/.gemini/config/global_workflows|$HOME/.gemini/config/skills" ;;
    opencode)    echo "$HOME/.config/opencode/AGENTS.md|$HOME/.config/opencode/commands|$HOME/.config/opencode/skills" ;;
    cursor)      echo "-|$HOME/.cursor/commands|$HOME/.cursor/skills" ;;
  esac
}

# 不以檔案方式安裝規則檔的平台，各自的替代做法
rules_note_for() {
  case "$1" in
    claude) echo "Claude Code 不自動載入 AGENTS.md：請把 rules/AGENTS.zh-TW.md 複製到專案根目錄，並在 CLAUDE.md 開頭加一行 @AGENTS.md" ;;
    cursor) echo "Cursor 無檔案系統層級的全域規則：請在 Settings → Rules → User Rules 貼上 rules/AGENTS.zh-TW.md 的內容" ;;
  esac
}

die() { echo "錯誤：$*" >&2; exit 1; }

is_known_platform() {
  local p
  for p in "${ALL_PLATFORMS[@]}"; do
    [ "$p" = "$1" ] && return 0
  done
  return 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --with-rules) WITH_RULES=1 ;;
    --rules-lang) shift; RULES_LANG="${1:-}" ;;
    --dry-run)    DRY_RUN=1 ;;
    --list)       LIST_ONLY=1 ;;
    -h|--help)    sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)           die "未知選項 $1（用 --help 看用法）" ;;
    *)            is_known_platform "$1" || die "未知平台 $1（可用：${ALL_PLATFORMS[*]}）"
                  SELECTED+=("$1") ;;
  esac
  shift
done

case "$RULES_LANG" in
  zh) RULES_SRC="$REPO_ROOT/rules/AGENTS.zh-TW.md" ;;
  en) RULES_SRC="$REPO_ROOT/rules/AGENTS.md" ;;
  *)  die "--rules-lang 只接受 zh 或 en" ;;
esac

if [ "$LIST_ONLY" = 1 ]; then
  for p in "${ALL_PLATFORMS[@]}"; do
    IFS='|' read -r r w s <<< "$(targets_for "$p")"
    installed="未安裝"; [ -d "$(base_dir_for "$p")" ] && installed="已安裝"
    echo "$p（$installed）"
    echo "  rules     : ${r/#$HOME/\~}"
    echo "  workflows : ${w/#$HOME/\~}"
    echo "  skills    : ${s/#$HOME/\~}"
    echo
  done
  exit 0
fi

# 未指定平台時，自動偵測已安裝的平台
if [ ${#SELECTED[@]} -eq 0 ]; then
  for p in "${ALL_PLATFORMS[@]}"; do
    [ -d "$(base_dir_for "$p")" ] && SELECTED+=("$p")
  done
  [ ${#SELECTED[@]} -eq 0 ] && die "未偵測到任何平台的設定目錄（用 --list 查看路徑，或直接指定平台名）"
  echo "偵測到已安裝的平台：${SELECTED[*]}"
  echo
fi

run() {
  if [ "$DRY_RUN" = 1 ]; then
    echo "    [dry-run] $*"
  else
    "$@"
  fi
}

# 安裝規則檔：既有檔案內容不同時先備份，避免蓋掉本機客製的規則
install_rules() {
  local platform="$1" target="$2"
  if [ "$target" = "-" ]; then
    echo "  規則：$(rules_note_for "$platform")"
    return
  fi
  if [ -f "$target" ] && ! cmp -s "$RULES_SRC" "$target"; then
    local backup="$target.bak-$(date +%Y%m%d-%H%M%S)"
    run cp "$target" "$backup"
    echo "  規則：既有檔案已備份到 ${backup/#$HOME/\~}"
  fi
  run mkdir -p "$(dirname "$target")"
  run cp "$RULES_SRC" "$target"
  echo "  規則：${RULES_SRC#$REPO_ROOT/} -> ${target/#$HOME/\~}"
}

install_workflows() {
  local platform="$1" target="$2"
  if [ "$target" = "-" ]; then
    echo "  工作流程：$platform 不使用 workflows，改用 skills"
    return
  fi
  run mkdir -p "$target"
  local count=0 f
  for f in "$REPO_ROOT"/workflows/shared/*.md; do
    run cp "$f" "$target/"
    count=$((count + 1))
  done
  # Antigravity 另有平台專屬工作流程
  if [ "$platform" = antigravity ]; then
    for f in "$REPO_ROOT"/workflows/antigravity/*.md; do
      run cp "$f" "$target/"
      count=$((count + 1))
    done
  fi
  echo "  工作流程：$count 個檔案 -> ${target/#$HOME/\~}/"
}

install_skills() {
  local target="$1"
  if [ "$target" = "-" ]; then
    return
  fi
  run mkdir -p "$target"
  local count=0 d name
  for d in "$REPO_ROOT"/skills/*/; do
    [ -f "$d/SKILL.md" ] || continue
    name="$(basename "$d")"
    run cp -r "$d" "$target/$name"
    count=$((count + 1))
  done
  echo "  技能：$count 個技能 -> ${target/#$HOME/\~}/"
}

[ "$DRY_RUN" = 1 ] && echo "（dry-run 模式，不會實際寫入）" && echo

for platform in "${SELECTED[@]}"; do
  IFS='|' read -r rules_target workflows_target skills_target <<< "$(targets_for "$platform")"
  echo "$platform"
  [ "$WITH_RULES" = 1 ] && install_rules "$platform" "$rules_target"
  install_workflows "$platform" "$workflows_target"
  install_skills "$skills_target"
  echo
done

# 遷移前的舊路徑若仍存在，會被當作 fallback 讀到舊版流程
OLD_ANTIGRAVITY="$HOME/.gemini/antigravity/global_workflows"
if [ -d "$OLD_ANTIGRAVITY" ]; then
  echo "提醒：偵測到 Antigravity 遷移前的舊目錄 ~/.gemini/antigravity/global_workflows/，"
  echo "      其內容可能被當作 fallback 載入。確認新路徑可用後建議清空該目錄。"
  echo
fi

if [ "$WITH_RULES" = 0 ]; then
  echo "未安裝規則檔（rules/）。需要時加上 --with-rules，腳本會先備份既有檔案。"
fi
echo "驗證：於 AI 對話框輸入 /，應出現 decompose、create-commit、new-issue、dev-cycle 等指令。"
