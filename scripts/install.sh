#!/usr/bin/env bash
#
# dev-rules-kit 安裝腳本：把 rules / skills 複製到各平台的設定目錄。
#
# 路徑的真相來源是 rules/README.md、skills/README.md 的
# 「安裝方式」章節。修改本檔的 targets_for() 時必須同步那兩份 README，
# scripts/check-kit.py 會驗證兩邊一致。
#
# 用法：
#   bash scripts/install.sh                    # 自動偵測已安裝的平台並安裝 skills
#   bash scripts/install.sh opencode claude    # 只裝指定平台
#   bash scripts/install.sh --with-rules       # 另外安裝規則檔（會先備份既有檔案）
#   bash scripts/install.sh --dry-run          # 只列出會做什麼，不實際複製
#   bash scripts/install.sh --list             # 列出平台與對應路徑
#   bash scripts/install.sh --check            # 唯讀列出各平台每個技能是哪一版 kit 或本地修改
#
# 同名技能的內容不屬於任何一版 kit（依 scripts/skill-hashes.txt 判斷）時，
# 先把整個技能目錄備份到 <平台設定目錄>/skill-backups/ 再覆蓋。
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ALL_PLATFORMS=(codex claude antigravity opencode cursor)

WITH_RULES=0
RULES_LANG=zh
DRY_RUN=0
LIST_ONLY=0
CHECK_ONLY=0
SELECTED=()

# 各平台的偵測目錄：存在才視為已安裝該平台
base_dir_for() {
  case "$1" in
    codex)       echo "$HOME/.codex" ;;
    claude)      echo "$HOME/.claude" ;;
    antigravity) echo "$HOME/.gemini/config" ;;
    opencode)    echo "$HOME/.config/opencode" ;;
    cursor)      echo "$HOME/.cursor" ;;
  esac
}

# 目標路徑：<rules 目標檔>|<skills 目標目錄>
# "-" 代表該平台不以檔案方式安裝規則檔
targets_for() {
  case "$1" in
    codex)       echo "$HOME/.codex/AGENTS.md|$HOME/.codex/skills" ;;
    claude)      echo "-|$HOME/.claude/skills" ;;
    antigravity) echo "$HOME/.gemini/config/AGENTS.md|$HOME/.gemini/config/skills" ;;
    opencode)    echo "$HOME/.config/opencode/AGENTS.md|$HOME/.config/opencode/skills" ;;
    cursor)      echo "-|$HOME/.cursor/skills" ;;
  esac
}

# 3.0.0 以前安裝 workflows 的目錄，每行一個。OpenCode 的同名 command 會蓋過 skill，
# 這些目錄中與本 kit 同名的舊檔留著的話，/<name> 會一直執行舊版
legacy_workflow_dirs_for() {
  case "$1" in
    antigravity) printf '%s\n' "$HOME/.gemini/config/global_workflows" "$HOME/.gemini/antigravity/global_workflows" ;;
    opencode)    printf '%s\n' "$HOME/.config/opencode/commands" "$HOME/.config/opencode/command" ;;
    cursor)      printf '%s\n' "$HOME/.cursor/commands" ;;
  esac
}

# 不以檔案方式安裝規則檔的平台，各自的替代做法
rules_note_for() {
  case "$1" in
    claude) echo "Claude Code 無全域規則檔：請把 rules/AGENTS.zh-TW.md 複製為專案根目錄的 AGENTS.md；專案已有 CLAUDE.md 時，在開頭加一行 @AGENTS.md，否則 AGENTS.md 不會被讀取" ;;
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
    --check)      CHECK_ONLY=1 ;;
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
    IFS='|' read -r r s <<< "$(targets_for "$p")"
    installed="未安裝"; [ -d "$(base_dir_for "$p")" ] && installed="已安裝"
    echo "$p（$installed）"
    echo "  rules     : ${r/#$HOME/\~}"
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

# 每個 kit 技能一行：名稱<TAB>狀態<TAB>說明（狀態見 scripts/skill_state.py）
skill_states() {
  python3 "$REPO_ROOT/scripts/skill_state.py" classify "$REPO_ROOT" "$1" \
    || die "無法判斷 $1 的技能版本（需要 python3）"
}

install_skills() {
  local target="$1"
  if [ "$target" = "-" ]; then
    return
  fi
  local states stamp name state detail backup
  states="$(skill_states "$target")"
  stamp="$(date +%Y%m%d-%H%M%S)"
  # 本地修改的技能先整個備份到技能目錄之外，放在技能目錄內會被當成第二個同名技能載入
  local n
  while IFS=$'\t' read -r name state detail; do
    [ "$state" = modified ] || continue
    backup="$(dirname "$target")/skill-backups/$name.bak-$stamp"
    n=1
    while [ -e "$backup" ]; do   # 同一秒重跑時另取名稱，不複製進既有的備份
      n=$((n + 1))
      backup="$(dirname "$target")/skill-backups/$name.bak-$stamp-$n"
    done
    if [ "$DRY_RUN" = 1 ]; then
      echo "    [dry-run] 會備份 $name（本地修改：$detail）-> ${backup/#$HOME/\~}"
    else
      # -L 複製連結指向的內容：技能目錄或檔案是 symlink 時，之後的覆蓋會寫穿連結
      mkdir -p "$backup"
      if ! cp -RL "$target/$name/." "$backup/"; then
        rm -rf "$backup"
        die "備份 $name 失敗（例如指向不存在目標的 symlink），${target/#$HOME/\~}/ 尚未覆蓋任何技能；${DONE_PLATFORMS:+已安裝完成：$DONE_PLATFORMS。}處理後重跑"
      fi
      echo "  備份：$name（本地修改：$detail）-> ${backup/#$HOME/\~}"
    fi
  done <<< "$states"
  run mkdir -p "$target"
  local count=0 d
  for d in "$REPO_ROOT"/skills/*/; do
    [ -f "$d/SKILL.md" ] || continue
    name="$(basename "$d")"
    run mkdir -p "$target/$name"
    run cp -r "$d." "$target/$name/"
    count=$((count + 1))
  done
  echo "  技能：$count 個技能 -> ${target/#$HOME/\~}/"
}

check_skills() {
  local target="$1" states name state detail
  if [ "$target" = "-" ]; then
    return
  fi
  if [ ! -d "$target" ]; then
    echo "  技能目錄 ${target/#$HOME/\~}/ 不存在，尚未安裝"
    return
  fi
  states="$(skill_states "$target")"
  while IFS=$'\t' read -r name state detail; do
    case "$state" in
      new)      echo "  $name：未安裝" ;;
      same)     echo "  $name：與本 kit 相同（$detail）" ;;
      kit)      echo "  $name：kit $detail，與本 kit 不同" ;;
      modified) echo "  $name：本地修改（$detail）" ;;
    esac
  done <<< "$states"
}

# 把舊版以 workflow 形式安裝的同名檔改名備份：現有技能，加上已移除的 fix-webview-conflict。
# 使用者自己的其他 workflow 不動
retire_legacy_workflows() {
  local platform="$1" stamp dir name count=0
  stamp="$(date +%Y%m%d-%H%M%S)"
  while IFS= read -r dir; do
    [ -d "$dir" ] || continue
    for name in "${KIT_WORKFLOW_NAMES[@]}"; do
      [ -f "$dir/$name.md" ] || continue
      run mv "$dir/$name.md" "$dir/$name.md.bak-$stamp"
      count=$((count + 1))
    done
  done < <(legacy_workflow_dirs_for "$platform")
  if [ "$count" -gt 0 ]; then
    echo "  舊工作流程：$count 個本 kit 檔案已改名為 .bak-$stamp，不再被載入"
  fi
}

KIT_WORKFLOW_NAMES=(fix-webview-conflict)
for d in "$REPO_ROOT"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  KIT_WORKFLOW_NAMES+=("$(basename "$d")")
done

if [ "$CHECK_ONLY" = 1 ]; then
  for platform in "${SELECTED[@]}"; do
    IFS='|' read -r rules_target skills_target <<< "$(targets_for "$platform")"
    echo "$platform"
    check_skills "$skills_target"
    echo
  done
  exit 0
fi

[ "$DRY_RUN" = 1 ] && echo "（dry-run 模式，不會實際寫入）" && echo

DONE_PLATFORMS=""   # 備份失敗中止時，告知哪些平台已經裝完
for platform in "${SELECTED[@]}"; do
  IFS='|' read -r rules_target skills_target <<< "$(targets_for "$platform")"
  echo "$platform"
  [ "$WITH_RULES" = 1 ] && install_rules "$platform" "$rules_target"
  install_skills "$skills_target"
  retire_legacy_workflows "$platform"
  DONE_PLATFORMS="${DONE_PLATFORMS:+$DONE_PLATFORMS、}$platform"
  echo
done

if [ "$WITH_RULES" = 0 ]; then
  echo "未安裝規則檔（rules/）。需要時加上 --with-rules，腳本會先備份既有檔案。"
fi
echo "驗證：Codex 輸入 /skills 或以 \$ 提及技能；其他平台輸入 /，應出現 decompose、create-commit、new-issue、dev-cycle 等技能。"
echo "專案初始化：執行 python3 scripts/init-project.py /path/to/project，部署核心技能需要的 docs 規範。"
