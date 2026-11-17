#!/usr/bin/env bash
#
# dev-rules-kit 下載安裝程式：不需 clone，下載 release 壓縮檔後執行該版的 install.sh（issue #9）。
#
# 用法：
#   curl -fsSL https://raw.githubusercontent.com/raybird/dev-rules-kit/main/scripts/get.sh | bash
#   curl -fsSL …/get.sh | bash -s -- --version v5.0.0     # 指定版本（v5.0.0 以後）
#   curl -fsSL …/get.sh | bash -s -- --dry-run            # 只列出會做什麼
#   curl -fsSL …/get.sh | bash -s -- --check              # 唯讀查目前版本、最新版與各平台技能
#   其餘參數（平台名稱、--with-rules、--list 等）原樣傳給 install.sh。重跑同一行就是更新。
#
# kit 存放在 ${XDG_DATA_HOME:-~/.local/share}/dev-rules-kit/<版本>/，current 連結指向目前版本；
# 初始化專案用 python3 ~/.local/share/dev-rules-kit/current/scripts/init-project.py <專案>。
#
# 全部包在 main 裡、最後一行才呼叫：curl | bash 下載中斷時不會執行到一半的腳本。
#
set -euo pipefail

REPO_URL="${DEV_RULES_KIT_REPO_URL:-https://github.com/raybird/dev-rules-kit}"
DATA_DIR="${DEV_RULES_KIT_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/dev-rules-kit}"
# 更早的版本沒有本地修改的備份與 --check，用它們的 install.sh 會直接覆蓋改過的技能
MIN_VERSION=v5.0.0
USAGE_URL="https://github.com/raybird/dev-rules-kit/blob/main/scripts/get.sh"

die() { echo "錯誤：$*" >&2; exit 1; }

# 最新版以 releases/latest 的轉址取得，不用 GitHub API（不受額度限制）
latest_version() {
  curl -fsSI "$REPO_URL/releases/latest" 2>/dev/null | tr -d '\r' \
    | awk 'tolower($1) == "location:" { print $2 }' | tail -n 1 | sed 's#.*/tag/##'
}

valid_version() { [[ "$1" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; }

# 純 bash 逐段比較，不依賴 sort -V（BusyBox 等環境沒有）；呼叫前已通過 valid_version
supported_version() {
  local want have i
  IFS=. read -r -a have <<< "${1#v}"
  IFS=. read -r -a want <<< "${MIN_VERSION#v}"
  for i in 0 1 2; do
    if (( 10#${have[i]} > 10#${want[i]} )); then return 0; fi
    if (( 10#${have[i]} < 10#${want[i]} )); then return 1; fi
  done
}

current_version() {
  if [ -L "$DATA_DIR/current" ]; then readlink "$DATA_DIR/current"; fi
}

# 下載、解壓到暫存目錄，確認內容完整後才回傳路徑；任何一步失敗都只留在暫存目錄
fetch_kit() {
  local version="$1" into="$2" archive top
  archive="$into/kit.tar.gz"
  curl -fsSL "$REPO_URL/archive/refs/tags/$version.tar.gz" -o "$archive" \
    || die "下載 $version 失敗（$REPO_URL/archive/refs/tags/$version.tar.gz）"
  mkdir "$into/x"
  tar -xzf "$archive" -C "$into/x" 2>/dev/null || die "$version 的壓縮檔無法解壓"
  top="$(find "$into/x" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  [ -n "$top" ] && [ -f "$top/scripts/install.sh" ] || die "$version 的壓縮檔缺少 scripts/install.sh"
  echo "$top"
}

main() {
  local version="" dry_run=0 check=0 list=0 pass=() installed latest kit target
  while [ $# -gt 0 ]; do
    case "$1" in
      --version)   shift; version="${1:-}"; [ -n "$version" ] || die "--version 需要版本，例如 $MIN_VERSION" ;;
      --version=*) version="${1#--version=}"; [ -n "$version" ] || die "--version 需要版本，例如 $MIN_VERSION" ;;
      --dry-run)   dry_run=1; pass+=("$1") ;;
      --list)      list=1; pass+=("$1") ;;
      --check)     check=1 ;;
      -h|--help)   echo "用法見 $USAGE_URL 開頭的說明"; exit 0 ;;
      *)           pass+=("$1") ;;
    esac
    shift
  done

  command -v curl >/dev/null || die "需要 curl"
  command -v tar >/dev/null || die "需要 tar"
  installed="$(current_version)"

  if [ "$check" = 1 ]; then
    latest="$(latest_version || true)"
    echo "目前版本：${installed:-尚未以 get.sh 安裝}"
    if valid_version "$latest"; then
      echo "最新 release：$latest"
    else
      echo "最新 release：取不到（無法連到 $REPO_URL/releases/latest）"
    fi
    [ -n "$installed" ] || exit 0
    echo
    exec bash "$DATA_DIR/current/scripts/install.sh" --check ${pass[@]+"${pass[@]}"}
  fi

  if [ -z "$version" ]; then
    version="$(latest_version || true)"
    valid_version "$version" || die "取不到最新版本；可用 --version 指定，例如 --version $MIN_VERSION"
  fi
  valid_version "$version" || die "版本格式應為 vX.Y.Z，收到「$version」"
  supported_version "$version" \
    || die "$version 早於 $MIN_VERSION，get.sh 只安裝 $MIN_VERSION 以後的版本（舊版不會備份改過的技能）；舊版請用 clone 安裝"

  TMP=""
  trap '[ -z "$TMP" ] || rm -rf "$TMP"' EXIT

  # dry-run 與 --list 不安裝：解壓到暫存目錄執行後刪除，不寫入資料目錄、不切換 current
  if [ "$dry_run" = 1 ] || [ "$list" = 1 ]; then
    TMP="$(mktemp -d)"
    if [ "$dry_run" = 1 ]; then
      echo "（dry-run：會下載 $version 到 ${DATA_DIR/#$HOME/\~}/$version/；目前版本：${installed:-尚未以 get.sh 安裝}）"
    fi
    kit="$(fetch_kit "$version" "$TMP")"
    bash "$kit/scripts/install.sh" ${pass[@]+"${pass[@]}"}
    exit 0
  fi

  target="$DATA_DIR/$version"
  if [ -f "$target/scripts/install.sh" ]; then
    echo "沿用已下載的 $version：${target/#$HOME/\~}/"
  elif [ -e "$target" ]; then
    die "${target/#$HOME/\~} 已存在但不完整，請先移除後重跑"
  else
    mkdir -p "$DATA_DIR"
    TMP="$(mktemp -d "$DATA_DIR/.get.XXXXXX")"
    kit="$(fetch_kit "$version" "$TMP")"
    mv "$kit" "$target"
    echo "已下載 $version：${target/#$HOME/\~}/"
  fi

  bash "$target/scripts/install.sh" ${pass[@]+"${pass[@]}"}
  ln -sfn "$version" "$DATA_DIR/current"
  echo "current -> $version"
  echo "專案初始化或更新：python3 ${DATA_DIR/#$HOME/\~}/current/scripts/init-project.py /path/to/project [--update]"
}

main "$@"
