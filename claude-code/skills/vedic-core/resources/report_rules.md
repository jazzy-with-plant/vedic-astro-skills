# 报告打包规则

> 用途：当用户说"生成报告""打包""导出HTML"时执行

---

## 脚本位置

report_builder.py 在本skill的 `scripts/` 目录下。
**完整路径**：使用相对于SKILL.md的路径 `scripts/report_builder.py`。

如果执行时提示找不到脚本，按以下顺序查找：
1. 当前skill目录下的 `scripts/report_builder.py`
2. 工作目录下的 `report_builder.py`（用户可能手动复制过）
3. 如果都找不到 → 告诉用户脚本路径，让用户确认位置

## 打包命令

### 默认：新手版

打包前先从现有的 `p5a_life.md`、`p5b_life.md`、`career_*.md`、`love_*.md`、
`qa_*.md` 和时间校准报告中生成 `beginner_summary.md`。这一步只做内容整理，不重算星盘。

`beginner_summary.md` 面向第一次接触吠陀占星的读者，正文控制在易于一次读完的长度，固定包含：

1. **一句话总览**：3—5句，说明主要优势、当前阶段和最需要处理的问题。
2. **事业与工作**：适合的角色、需要避开的环境、未来两年主要时机。
3. **感情与关系**：关系模式、真实需求、最近的机会窗口与筛选重点。
4. **生活基础**：财务、家庭、身心状态各1—2条，只保留会影响决策的内容。
5. **未来时间线**：最多6行，按日期排序，说明“适合做什么”和“需要防什么”。
6. **行动清单**：最多5条，可直接执行。

写作约束：

- 先说结论，再说原因；每段只表达一个重点。
- 不在正文罗列宫位、SAV、Shadbala、D9/D10宫主、梵文术语或审计编号。
- 术语确有必要时，放在括号内解释一次；详细数据留给折叠的技术附录。
- 不重复同一结论，不把“可能、也许、倾向”连续堆叠。
- 时间窗口必须保留条件和不确定性，不写成保证。

先根据当前 Skill 的 `client_language` 选择 `--lang`：

- English → `--lang en`
- 日本語 → `--lang ja`
- 中文 → `--lang cn`
- 其他语言 → 使用正文实际采用的语言；HTML 外壳暂选 `en`，不得因此把正文改回英文、日文或中文

```python
# 打包全部已有文件（默认新手版）
python scripts/report_builder.py [工作目录] --audience beginner --lang [cn|en|ja]

# 技术版：保留逐星、逐宫和分盘的独立章节
python scripts/report_builder.py [工作目录] --audience technical --lang [cn|en|ja]

# 只打包core
python scripts/report_builder.py [工作目录] --include core --lang [cn|en|ja]

# 只打包core + career
python scripts/report_builder.py [工作目录] --include core,career --lang [cn|en|ja]
```

report_builder自动检测目录中存在哪些MD文件，只打包存在的。
`--include`参数可选择只打包特定部分。
`--audience beginner`按“核心总结、事业、感情、生活基础、补充问答、技术附录”分组，
并折叠完整审计；`--audience technical`保留原来的逐文件章节结构。
报告根目录和`parts/`会同时扫描，`parts/`中的问答不会再遮蔽根目录正文。
`--lang`只控制封面、目录、章节标题和页脚；正文语言来自已有 Markdown，禁止把
正文放入不匹配的中文、英文或日文外壳。

## ⚠️ 禁止行为

1. **禁止自动打开浏览器预览**：生成HTML后不要用 `open`/`start`/`xdg-open` 打开浏览器。只告诉用户文件路径，让用户自己决定是否打开。
2. **禁止在聊天框中输出HTML代码**：HTML文件由脚本生成，不要在对话中贴代码。
3. **生成完成后只报路径**：`"报告已生成：[完整文件路径]"`，不在聊天框复制报告正文。
