#!/usr/bin/env bash
#
# dev-rules-kit 下載安裝程式：不需 clone，下載 release 壓縮檔後執行該版的 install.sh（issue #9）。
#
# 用法：
#   curl -fsSL https://raw.githubusercontent.com/raybird/dev-rules-kit/main/scripts/get.sh | bash
#   curl -fsSL …/get.sh | bash -s -- --version v5.0.0     # 指定版本
#   curl -fsSL …/get.sh | bash -s -- --dry-run            # 只列出會做什麼
#   curl -fsSL …/get.sh | bash -s -- --check              # 唯讀查目前版本、最新版與各平台技能
#   其餘參數（平台名稱、--with-rules 等）原樣傳給 install.sh。重跑同一行就是更新。
#
# kit 存放在 ${XDG_DATA_HOME:-~/.local/share}/dev-rules-kit/<版本>/，current 連結指向目前版本；
# 初始化專案用 python3 ~/.local/share/dev-rules-kit/current/scripts/init-project.py <專案>。
#
set -euo pipefail

REPO_URL="${DEV_RULES_KIT_REPO_URL:-https://github.com/raybird/dev-rules-kit}"
DATA_DIR="${DEV_RULES_KIT_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/dev-rules-kit}"

VERSION=""
DRY_RUN=0
CHECK=0
PASS=()

die() { echo "錯誤：$*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --version)   shift; VERSION="${1:-}"; [ -n "$VERSION" ] || die "--version 需要版本，例如 v5.0.0" ;;
    --version=*) VERSION="${1#--version=}" ;;
    --dry-run)   DRY_RUN=1; PASS+=("$1") ;;
    --check)     CHECK=1 ;;
    -h|--help)   echo "用法見 https://github.com/raybird/dev-rules-kit/blob/main/scripts/get.sh 開頭的說明"; exit 0 ;;
    *)           PASS+=("$1") ;;
  esac
  shift
done

command -v curl >/dev/null || die "需要 curl"
command -v tar >/dev/null || die "需要 tar"

# 最新版以 releases/latest 的轉址取得，不用 GitHub API（不受額度限制）
latest_version() {
  curl -fsSI "$REPO_URL/releases/latest" 2>/dev/null | tr -d '\r' \
    | awk 'tolower($1) == "location:" { print $2 }' | tail -n 1 | sed 's#.*/tag/##'
}

valid_version() { [[ "$1" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; }

current_version() {
  [ -L "$DATA_DIR/current" ] && readlink "$DATA_DIR/current" || true
}

if [ "$CHECK" = 1 ]; then
  installed="$(current_version)"
  latest="$(latest_version || true)"
  echo "目前版本：${installed:-尚未以 get.sh 安裝}"
  if valid_version "$latest"; then
    echo "最新 release：$latest"
  else
    echo "最新 release：取不到（無法連到 $REPO_URL/releases/latest）"
  fi
  [ -n "$installed" ] || exit 0
  echo
  exec bash "$DATA_DIR/current/scripts/install.sh" --check ${PASS[@]+"${PASS[@]}"}
fi

if [ -z "$VERSION" ]; then
  VERSION="$(latest_version || true)"
  valid_version "$VERSION" || die "取不到最新版本；可用 --version 指定，例如 --version v5.0.0"
fi
valid_version "$VERSION" || die "版本格式應為 vX.Y.Z，收到「$VERSION」"

# 下載、解壓到暫存目錄，確認內容完整後才搬進版本目錄；任何一步失敗都只清掉暫存目錄
fetch_kit() {
  local into="$1" archive top
  archive="$into/kit.tar.gz"
  curl -fsSL "$REPO_URL/archive/refs/tags/$VERSION.tar.gz" -o "$archive" \
    || die "下載 $VERSION 失敗（$REPO_URL/archive/refs/tags/$VERSION.tar.gz）"
  mkdir "$into/x"
  tar -xzf "$archive" -C "$into/x" 2>/dev/null || die "$VERSION 的壓縮檔無法解壓"
  top="$(find "$into/x" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  [ -n "$top" ] && [ -f "$top/scripts/install.sh" ] || die "$VERSION 的壓縮檔缺少 scripts/install.sh"
  echo "$top"
}

TMP=""
cleanup() { [ -z "$TMP" ] || rm -rf "$TMP"; }
trap cleanup EXIT

if [ "$DRY_RUN" = 1 ]; then
  TMP="$(mktemp -d)"
  installed="$(current_version)"
  echo "（dry-run：會下載 $VERSION 到 ${DATA_DIR/#$HOME/\~}/$VERSION/；目前版本：${installed:-尚未以 get.sh 安裝}）"
  kit="$(fetch_kit "$TMP")"
  bash "$kit/scripts/install.sh" ${PASS[@]+"${PASS[@]}"}
  exit 0
fi

target="$DATA_DIR/$VERSION"
if [ -f "$target/scripts/install.sh" ]; then
  echo "沿用已下載的 $VERSION：${target/#$HOME/\~}/"
elif [ -e "$target" ]; then
  die "${target/#$HOME/\~} 已存在但不完整，請先移除後重跑"
else
  mkdir -p "$DATA_DIR"
  TMP="$(mktemp -d "$DATA_DIR/.get.XXXXXX")"
  kit="$(fetch_kit "$TMP")"
  mv "$kit" "$target"
  echo "已下載 $VERSION：${target/#$HOME/\~}/"
fi

bash "$target/scripts/install.sh" ${PASS[@]+"${PASS[@]}"}
ln -sfn "$VERSION" "$DATA_DIR/current"
echo "current -> $VERSION"
echo "專案初始化或更新：python3 ${DATA_DIR/#$HOME/\~}/current/scripts/init-project.py /path/to/project [--update]"
