# tests-that-can-fail

[English](README.md)

给 AI 编程 agent(Claude Code、Codex,以及任何读 `SKILL.md` 的工具)用的 skill,针对一个场景:让模型来写"判断对错的东西",包括单元测试、属性测试、契约、benchmark、eval。

模型很会写看起来周全的测试,但其中相当一部分永远不会失败、永远失败,或者比的根本不是文档说的那两样东西。这个 skill 给 agent 三个逐条自问的问题、五类根因、一套写测试的流程,以及一张审查模型已写测试的清单。

## 来源

这些模式是实测出来的。在盲测里,两个模型家族只看文档,为真实 Python 库(python-semver、more-itertools、humanize、inflect、num2words、parse)写声明式契约。每个库有两个版本:一个带着 changelog 里记录的缺陷,一个是修好的版本。由机械裁判在两个版本上执行契约。并发相关的条目来自另一个包含 17 个时序缺陷机制的实验台。

每份写错的契约都按种类记账。去重后的 256 条失败归为五类根因:

| 根因 | 占比 |
| --- | --- |
| 操作数:比较的两样东西不是文档关联的那两样 | 34% |
| 作用域:只在部分输入上成立,却写成对所有输入成立 | 27% |
| 填充:为了凑数量或凑规则而写的断言 | 25% |
| 裁判:计分方式本身有错 | 8% |
| 协议:校验反馈误导了模型 | 6% |

对这个 skill 影响最大的两个结果:

- 同样的文档、同样的两个版本,事先写下 `error == null` 的模型抓住了错误的异常;同一个模型自由测试时,12 次会话里 12 次亲眼打印出这个异常,然后判定"与文档一致"。
- 把教训贴进提示词,在两次对照实验里都没有效果;改变模型要填写的结构才有效。

## 边界

样本是六个小型纯 Python 库和两个模型家族,百分比只描述这份记录。契约是对调用结果的声明式断言,比自由编写的测试代码范围窄。目录记录的是哪里出过错、当时靠什么拦住,不保证在别处有同样的比例。

## 安装

```bash
git clone https://github.com/SLYysl/tests-that-can-fail.git
cp -R tests-that-can-fail/skills/tests-that-can-fail ~/.claude/skills/    # Claude Code
cp -R tests-that-can-fail/skills/tests-that-can-fail ~/.codex/skills/     # Codex
```

之后照常提需求:"给这个模块写测试"、"审一下这些测试"、"这个 benchmark 靠谱吗",任务匹配时 agent 会自动加载。

## 内容

- [`SKILL.md`](skills/tests-that-can-fail/SKILL.md):三个问题、五类根因、流程和审查清单(英文)。
- [`references/failure-modes.md`](skills/tests-that-can-fail/references/failure-modes.md):30 条实测失败模式及对应防法(英文)。

## 许可

Apache-2.0
