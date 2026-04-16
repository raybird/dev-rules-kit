---
description: 清除 Antigravity 與 Windsurf 衝突導致的 WebView 快取與 Service Worker 錯誤
---

這個工作流將會清除可能導致 `InvalidStateError` 的快取資料，包括 Windsurf 和 Antigravity 的 Service Worker 快取。執行後，建議您手動執行 `Developer: Reload Window` 以恢復正常。

// turbo-all
1. 清除 Antigravity 相關快取目錄
```bash
rm -rf "$HOME/.config/Antigravity/Service Worker" "$HOME/.config/Antigravity/Cache" "$HOME/.config/Antigravity/GPUCache" "$HOME/.config/Antigravity/Code Cache" "$HOME/.config/Antigravity/CachedData" "$HOME/.config/Antigravity/Local Storage" "$HOME/.config/Antigravity/Session Storage"
```

2. 清除 Windsurf 相關快取目錄（避免衝突）
```bash
rm -rf "$HOME/.config/Windsurf/Service Worker" "$HOME/.config/Windsurf/Cache" "$HOME/.config/Windsurf/GPUCache" "$HOME/.config/Windsurf/Code Cache" "$HOME/.config/Windsurf/CachedData"
```

3. 完成清理
完成快取清理。請現在按下 `Ctrl + Shift + P` 並執行 **Developer: Reload Window** 以套用變更。如果問題仍然存在，建議完全關閉 Antigravity 後重新開啟。