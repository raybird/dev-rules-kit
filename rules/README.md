# Rules

本目錄存放 AI 開發助理的核心規則檔案。

## 參考來源與演進

本專案的規則內容起初參考自：
- **[andrej-karpathy-skills](https://github.com/vtroisWhite/andrej-karpathy-skills)** - Karpathy-Inspired Claude Code Guidelines

並在此基礎上，結合實際工程落地經驗，擴充與演化為一套更適用於團隊 Monorepo 與多人協作的開發規範。

## 核心原則

1. **Think Before Coding (編寫前先思考)**：拒絕盲目假設，主動攤開取捨與模糊點。
2. **Simplicity First (簡單優先)**：用最少、最直接的程式碼解決問題，拒絕過度設計。
3. **Surgical Changes (手術式修改)**：只改動必須修改的程式碼，不順手重構鄰近無關內容。
4. **Goal-Driven Execution (目標驅動驗證)**：先定義成功條件（如失敗測試），反覆執行至驗證通過。
5. **Workflow Triage (工作流程分級)**：小任務直接執行，大任務先寫計畫，避免流程繁瑣化。
6. **Token Economy (Token 經濟原則)**：推理與回答長度與任務大小成比例，拒絕長篇贅述。
7. **Monorepo Rules (Monorepo 規則)**：優先採用局部修復，找出最小受影響範圍，避免跨服務改動。

## 檔案說明

- `AGENTS.md` - AI 開發助理核心規則（英文版）
- `AGENTS.zh-TW.md` - AI 開發助理核心規則（繁體中文版）

## 安裝方式

各平台讀取全域規則的位置不同，擇一複製即可（繁中環境建議用 `AGENTS.zh-TW.md`）：

| 平台 | 全域規則位置 | 專案層覆寫 |
|------|-------------|-----------|
| **Claude Code** | 不自動載入 `AGENTS.md`，需在 `CLAUDE.md` 用 `@AGENTS.md` 匯入（見下方） | 專案根目錄 `AGENTS.md` |
| **Windsurf** | `~/.codeium/windsurf/memories/global_rules.md` | `.windsurfrules`（疊加而非覆寫） |
| **Antigravity** | `~/.gemini/GEMINI.md` | — |
| **Cursor** | 無檔案系統層級設定，需在 Settings → **Rules** → **User Rules** 貼上內容 | `.cursor/rules/*.mdc`（`.cursorrules` 為舊版單檔格式，仍可用） |
| **OpenCode** | `~/.config/opencode/AGENTS.md` | 專案根目錄 `AGENTS.md` |

```bash
# Windsurf
cp dev-rules-kit/rules/AGENTS.zh-TW.md ~/.codeium/windsurf/memories/global_rules.md

# Antigravity
cp dev-rules-kit/rules/AGENTS.zh-TW.md ~/.gemini/GEMINI.md

# OpenCode
cp dev-rules-kit/rules/AGENTS.zh-TW.md ~/.config/opencode/AGENTS.md
```

**Claude Code 的掛載方式**：Claude Code 只讀 `CLAUDE.md`，不會自動載入 `AGENTS.md`。將本檔複製到專案根目錄後，需在 `CLAUDE.md` 開頭加一行獨立的 `@AGENTS.md`（不可包在反引號或程式碼區塊內）。完整步驟與 `/init` 覆寫的注意事項見[根目錄 README](../README.md#下游專案掛載規則claude-code)。

外部工具（Serena / GitNexus / Superpowers）的設定見 [docs/setup/tools.md](../docs/setup/tools.md)。

---

**建立日期**: 2026-05-08  
**最後更新**: 2026-06-20  
**文件版本**: 1.1  

