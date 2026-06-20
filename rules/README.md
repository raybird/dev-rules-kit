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

---

**建立日期**: 2026-05-08  
**最後更新**: 2026-06-20  
**文件版本**: 1.1  

