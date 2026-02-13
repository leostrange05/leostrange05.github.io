---
    title: 本站志
---

# :memo: 本站志

本站基于 [:simple-materialformkdocs: Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)，由 :simple-googlegemini: Google Gemini 协同构建。你所看到的主页标题区域、最近更新内容的自动提取等，很大程度上均由 AI 辅助实现。你可以在 [本站的 :fontawesome-brands-github: GitHub 仓库](https://github.com/leostrange05/leostrange05.github.io) 查看源代码。

主页标题区域的背景图由 :simple-googlegemini: Nano Banana AI 生成，为构成主义风格启发的平面图像；右上角的小组件模拟了 [:simple-wikipedia: 机械翻页显示](https://zh.wikipedia.org/wiki/%E6%9C%BA%E6%A2%B0%E7%BF%BB%E9%A1%B5%E6%98%BE%E7%A4%BA) 的效果。

最近更新的内容则是通过访问 :simple-git: Git 日志定位到最近提交的 Markdown 文件，并提取其中的标题和链接来实现的，可以实现动态更新。仓库中的 `main.py` 实现了这一过程，并基于 mkdocs-macros 插件将结果注入到主页中。