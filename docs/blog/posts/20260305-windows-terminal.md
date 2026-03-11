---
date: 2026-03-05
title: 在 Windows 上便捷地打开终端
categories: 
    - 捣鼓一下
tags:
    - Windows
---

# 在 Windows 上便捷地打开终端

### 2026-03-11 更新

发现了 Quicker 这个工具，可以设置快捷键来打开 Windows 终端，速度非常快。**甚至，它可以非常方便地探测到打开的文件夹，并从该文件夹所在位置打开终端**。相比之前的方案，这个工具更简单易用。工具的链接在[此处](https://getquicker.net/Sharedaction?code=95499ce4-bc30-4933-0c7d-08dbf467792d)。

不过，以下方案中“管理员权限”的部分仍然是一个较好的方案。Quicker 在使用管理员权限打开终端时，仍然会弹出权限提升提示框，而以下方案则可以避免这个问题。

!!! info "本文的核心结论"
    Windows 任务计划程序里面创建的任务可以在不弹出权限提升提示框的情况下以管理员权限运行。

---

在使用 :simple-ubuntu: Ubuntu 桌面环境时，++ctrl+alt+t++ 是打开终端的快捷键。我想在 Windows 上也获得类似的体验，于是捣鼓了一下。

!!! note "运行"
    Windows 上，其实 ++win+r++ 打开运行，输入 cmd 或者其他指令已经非常方便了，但我还是想要一个更直接的快捷键来打开终端。

<!-- more -->

在 Windows 11 上，有多个“终端类似物”，包括命令提示符 (cmd)、PowerShell 和 Windows 终端 (Windows Terminal, wt)。

- 命令提示符 (cmd) 是 Windows 的传统终端，在很早以前就存在，功能较为基础，界面也较为简陋，但优点是轻量化。
- PowerShell 是微软推出的更现代化的终端，功能更强大，支持更多的命令和脚本，但相对来说也更重一些，命令语法和 cmd 有较大不同。
- Windows 终端 (Windows Terminal, wt) 是微软最新推出的终端应用，支持多标签页、丰富的自定义选项和更漂亮的界面。但是通常来说，它的打开不如 cmd 快。**需要注意的是，它只是一个终端应用，用于打开上述两种终端“环境”。**在 wt 上面，可以打开 cmd、PowerShell 以及 WSL（Windows Subsystem for Linux）等多种终端环境。

在 Windows 上，对于某个快捷方式，可以在属性中设置快捷键。于是，我直接新建快捷方式，设置快捷键即可。

但是 wt 不够轻量，有时候打开极慢，甚至有时候抽风根本没反应。

于是我退而求其次，设置了 cmd 的快捷键为 ++ctrl+alt+t++。虽然它的功能不如 wt 强大，界面有些简陋，但至少能快速打开一个终端窗口。很多时候离电使用时，cmd 也会更快、更省电。

<p align="center"><img src="https://cdn.jsdelivr.net/gh/leostrange05/Images/image20260305223629279.png" alt="cmd" style="width:50%;height:auto;"></p>

但是，我还是希望能有一个更快的方式打开 wt，毕竟它的功能更强大，界面也更好看。

经过我的试验，以管理员身份运行 wt 时，打开速度明显提升，也很少会抽风。因此我决定，自定义 `su` 命令来以管理员身份打开 wt。这样，我就可以在 cmd 中输入 `su` 来快速打开 wt 了。

但是有一个问题是，每次调用管理员权限时，都会跳一个权限提升的提示框，很麻烦，虽然这是一种安全机制。询问 AI 之后，我找到了一个解决方案：使用 Windows 任务计划程序来创建一个以管理员权限运行的任务，然后使用 bat 脚本调用这个任务来打开 wt。Windows 的任务计划可以在不跳出权限提升提示框的情况下以最高权限运行任务，这样就可以达到需要的效果了。

![](https://cdn.jsdelivr.net/gh/leostrange05/Images/image20260305230333114.png)

具体来说，++win+r++ 打开运行，输入 `taskschd.msc` 打开任务计划程序，创建一个新的任务，勾选“使用最高权限运行”，并在操作中添加一个新的操作，选择“启动程序”，程序/脚本填写 wt 的路径（通常是 `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\wt.exe`），保存任务名称为 run_windows_terminal。

然后创建一个 su.bat 文件，内容如下：

<div class="annotate" markdown>
```bat title="su.bat"
@echo off
schtasks /run /tn run_windows_terminal (1)
```
</div>
1. 这里与之前创建的任务名称一致即可。

将 su.bat 的路径添加到系统环境变量 Path 中，这样在 cmd 中输入 `su` 就可以直接运行这个脚本，进而调用任务计划来打开 wt 了。

至此，所有的功能已经实现。按下 ++ctrl+alt+t++ 可以快速打开 cmd，在 cmd 中输入 `su` 可以快速打开管理员权限的 wt。