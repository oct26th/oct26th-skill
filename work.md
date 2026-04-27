# oct26th's Work Skill

## 核心工作哲學

### Research & Reuse (MANDATORY)
- **GitHub 優先** — `gh search repos` + `gh search code` 找既有實作
- **文檔次之** — Context7 或官方文檔確認 API / 版本細節
- **寧可重用 勿手寫** — 80% 匹配的開源方案優於 net-new code
- **包管理優先** — npm/PyPI/crates.io 已有的不重複造輪子

### Planning & Execution
1. **Plan First** — 用 planner agent 產 PRD + architecture + task breakdown
2. **TDD Mandatory** — RED → GREEN → IMPROVE，80%+ 覆蓋率
3. **Code Review Immediate** — 寫完即請 code-reviewer，處理 CRITICAL/HIGH，盡力 fix MEDIUM
4. **Commit Detailed** — 完整 commit history 分析，不切角

## 代碼標準（CRITICAL）

### Immutability
```
✗ 錯：modify(obj, key, val) → 就地修改 obj
✓ 對：update(obj, key, val) → 回傳新 copy
```
理由：防止隱藏 side effect、簡化 debug、安全並發

### 文件組織
- **小多於大** — 200-400 行典型，800 行為上限
- **高內聚低耦合** — 按 feature/domain 組織，不按 type（不是 components/, utils/, 這種）
- **提取工具函數** — 重複邏輯必須萃取

### 錯誤處理
- **顯式處理** — 每層都要 catch，不吞 error
- **用戶友好** — UI 層提供清楚訊息，server 層記詳細 context
- **fail fast** — 邊界驗證馬上擋住壞輸入

### 輸入驗證
- **邊界驗證** — user input、API response、file content 全驗
- **schema-based** — 有現成工具就用（Zod、joi 等），不自己寫
- **Never trust external data** — 縱使看起來正常也要驗

## 質量檢查清單

進度標示完成前：
- [ ] Code 可讀、命名清晰
- [ ] Function < 50 行
- [ ] File < 800 行
- [ ] 無深層嵌套 (>4 層)
- [ ] 完整錯誤處理
- [ ] 無 hardcoded value（用 constant/config）
- [ ] 無 mutation（immutable 模式）

## Git & PR 流程

### Commit Message Format
```
<type>: <description>

<optional body>
```
Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`

### PR Workflow
1. 分析完整 commit history（不只最新 commit）
2. 用 `git diff [base-branch]...HEAD` 看全部改動
3. 寫完整 PR summary（說 why，不是 what）
4. 包含 test plan with TODOs
5. push 時用 `-u` flag（新分支）

## Agent Delegation

| 場景 | Agent | 用法 |
|------|-------|------|
| 複雜特性規劃 | **planner** | 產生 PRD、架構、task list |
| 新特性 / bug fix | **tdd-guide** | 帶著 TDD 流程跑 |
| Code 寫完 | **code-reviewer** | immediate，處理 issue |
| 架構決策 | **architect** | 系統設計、大重構 |
| Build 失敗 | **build-error-resolver** | 快速 fix |
| 安全檢查 | **security-reviewer** | commit 前跑一次 |

> **Parallel execution** — 獨立工作用平行 agent，不要序列化

## Tech Stack (NERV-HQ 上下文)

### Infrastructure
- **Zeabur** — 主要部署平台（openclaw、hermes、intel 服務）
- **joeclaw VM** — 本機測試、Ollama LLM
- **Hermes bot** — Discord 獨立 bot token，用 MiniMax

### Skills & Tools
- **claudecode-discord** — 使徒 bot 本機版
- **tools/skills/** — 共用 skill 定義

### Operational Discipline
- **小步快走** — 增量部署，快速反饋
- **配置優先** — openclaw.json 改設定後即時 restart，不需重 build
- **狀態管理** — runtime 狀態 gitignore（credentials/, memory/, logs/）
