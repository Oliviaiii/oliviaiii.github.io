# Olivia Lin — 履歷網站

[Oliviaiii](https://github.com/Oliviaiii) 的個人履歷網站，純靜態、無建置步驟，部署在 GitHub Pages。

## 頁面

| 檔案 | 內容 |
| --- | --- |
| `index.html` | 履歷本體：定位、關鍵成果、工作方式、四個案例摘要、AI 數據摘要、經歷、公開作品、聯絡。可直接列印成一頁式履歷（有 print 樣式）。 |
| `work.html` | 四個案例的完整版（情境／我做的／結果／可核對的證據）與公開作品。 |
| `ai-workflow.html` | AI 工作方式：六個月 session 統計、制度清單（憲章、規範、skills、agents、hook）、一張票的完整流程、實際下過的指令、踩過的坑、界線與工具箱。 |
| `styles.css` | 設計系統：tokens（含深色模式）、版面、元件、響應式、列印。 |
| `script.js` | 只做年份與導覽狀態，沒有 JS 也能完整使用。 |
| `assets/` | 圖片（來自公開專案）。 |
| `林芷筠中文履歷.pdf` / `林芷筠英文履歷.pdf` | 可下載的 PDF 履歷。 |

## 數據來源

`ai-workflow.html` 與首頁的 AI 數據，是用腳本掃描本機 `~/.claude/projects` 與 `~/.codex/sessions` 的對話紀錄統計（2026-03-30 – 2026-09-05）；issue／留言數來自 `gh api search/issues`；commit 數與語言組成來自本機 14 個 git repo 的 `git log --all --author=<我的 email> --numstat`（排除 vendor、lock、詞典等非手寫檔，2025-04 – 2026-09）。統計腳本不在本倉庫；更新數據時直接改 HTML 內的數字與 SVG 長條高度。

## 本機預覽

```powershell
python -m http.server 4173
```

開啟 `http://127.0.0.1:4173`。

## 部署

推到 `main`，GitHub Pages 設定為 **Deploy from a branch → main / root**。
