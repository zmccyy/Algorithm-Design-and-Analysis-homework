# 毕设导师（grad-project-mentor）

嵌入式本科毕设全程导师型技能包。同一套 [Agent Skills](https://code.claude.com/docs/en/skills)（`SKILL.md`）同时用于 **Claude Code** 和 **Codex**，无需改格式。

## 包含内容

| 技能 | 用途 |
|---|---|
| `grad-project-mentor` | 导师人格本体：五阶段验收关卡、进度台账、防糊弄追问、风险分级、模拟组会 |
| `grad-project-topic-advisor` | 选题出题/体检/对比/预算，八大题型先验表与"烂大街"黑名单 |
| `grad-project-proposal-helper` | 开题报告六章节框架、技术路线、倒排进度、开题答辩预案 |
| `grad-project-thesis-writer` | 论文六章框架、测试用例表、查重自查、去 AI 味守则 |
| `grad-project-defense-ppt` | 答辩 PPT 大纲（8–12 页按时长缩放）、演示防翻车清单 |
| `grad-project-defense-qa` | 六类高频问题库、三层追问链、模拟答辩演练 |

## 安装

### Claude Code（推荐：作为插件市场安装）

```bash
claude plugin marketplace add zmccyy/-
claude plugin install grad-project-mentor@grad-project-mentor-pack
```

或在会话内：

```text
/plugin marketplace add zmccyy/-
/plugin install grad-project-mentor@grad-project-mentor-pack
```

技能带插件命名空间，例如 `/grad-project-mentor:grad-project-topic-advisor`；直接描述任务也会自动触发。

其他方式：

- 本地目录直接加载：`claude --plugin-dir ./grad-project-mentor`
- 只装技能副本：`bash grad-project-mentor/scripts/install.sh claude`

### Codex

Codex 从 `~/.codex/skills/`（个人）或项目内 `.codex/skills/` 读取技能。先克隆本仓库，然后：

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File .\grad-project-mentor\scripts\install.ps1 codex
```

```bash
# macOS / Linux
bash grad-project-mentor/scripts/install.sh codex
```

也可以手动复制：把 `grad-project-mentor/skills/` 下的 6 个文件夹复制到 `~/.codex/skills/`。

安装后**重启 Claude Code / Codex** 使技能生效。

## 使用

直接用自然语言描述任务即可自动命中，例如：

- "我电子信息专业，预算 150 元，12 月开题 5 月答辩，帮我出几个毕设题目"
- "题目是自动浇花系统，12 月 20 日交开题，帮我搭框架"
- "论文测试章节的数据怎么组织才可信"
- "10 分钟答辩，帮我排一下 PPT 结构和时间"
- "我的题目是智能药盒，模拟一次答辩追问"

导师技能会先过"台账三问"（上次承诺完成了吗 / 现在卡在哪 / 下次汇报前完成什么），再按五阶段关卡推进。

## 来源与许可

- 上游：**grad-project-mentor 1.0.0**，作者 **FirmwareSmith**，原发布于 Qoder 插件市场
- 许可：**MIT**，全文见 [LICENSE](LICENSE)；转换说明见 [NOTICE.md](NOTICE.md)
- 本包为跨平台转换版：仅清理了 Qoder 专用 frontmatter，并把导师 agent 定义转成了技能，正文内容未改动
- 正文中提到的 `embedded-debug-trees`、`motor-pid-tuner` 等 companion 技能**不在本包内**，相关转介只是文字提示

## 更新

- Claude Code 插件市场安装：`claude plugin update grad-project-mentor@grad-project-mentor-pack`
- 技能副本 / Codex：`git pull` 后重新运行安装脚本
