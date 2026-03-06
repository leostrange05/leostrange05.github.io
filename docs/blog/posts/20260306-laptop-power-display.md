---
date: 2026-03-06
title: 笔记本电脑电池功耗功率显示插件
categories: 
    - 捣鼓一下
tags:
    - 小组件
---

# 笔记本电脑电池功耗功率显示插件

离电使用笔记本电脑时，我总是有“电量焦虑”。

于是，我安装了 Lenovo Vantage，它是 Lenovo 官方提供的一个系统管理工具，里面也可以显示电池电量、预计剩余时间等信息。为了让电量百分比能够直接显示在任务栏上，我还安装了 Pure Battery add-on 这个小组件（在 Microsoft Store 中貌似现在要付费，我安装时好像免费）。

但是，它们都没办法直观地显示功率。我非常希望能够看到实时的功率数值，这样可以让我很好地监控电池的使用情况。

于是我利用 AI 的帮助，编写了一个 Python 脚本获取实时功耗，并在任务栏上显示出一个图标展示功耗数值。

在此分享一下这个简单的脚本，它比较轻量化，用轮询(Polling)的方式，每 2 秒更新一次功率数值，并且在图标上用不同的颜色来表示不同的功率范围。颜色目前按照浅色任务栏设计，可以自定义为深色背景适配的颜色。当功率超过 100 W 时，图标上会显示“++”来提示用户；连接电源时，显示“C”。日常开启占用内存约 10~20 MB 左右。

<!-- more -->

如果要将其转换为 Windows 的可执行文件，可以使用 PyInstaller 进行打包，命令如下：

```bash
pyinstaller --noconsole --onefile battery_power.py
```

脚本如下：

```python title="battery_power.py" linenums="1"
import wmi
import time
import threading
import pythoncom
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item

current_power_str = "0.0"

def format_power_for_tray(val_str):
    """
    将功耗字符串缩减至最多3个字符（两位数+小数点 或 两位整数）
    例如: "5.432" -> "5.4", "12.67" -> "13", "120.5" -> "99"
    """
    try:
        val = float(val_str)
    except (ValueError, TypeError):
        return val_str

    if val < 0:
        return "0"
    
    if val < 9.95:
        formatted = f"{val:.1f}"
        if float(formatted) >= 10.0:
            return "10"
        return formatted
    
    if val < 99.5:
        return str(round(val))

    return "++"

def get_battery_power():
    """从系统获取实时功耗"""
    pythoncom.CoInitialize()
    try:
        w = wmi.WMI(namespace="root\\wmi")
        batches = w.ExecQuery("Select * from BatteryStatus")
        for b in batches:
            rate = b.DischargeRate
            if rate is not None and rate > 0:
                return f"{rate / 1000.0:.1f}"
        return "C"
    except Exception:
        return "N/A"
    finally:
        pythoncom.CoUninitialize()

def create_transparent_icon(text):
    try:
        val = float(text)
    except:
        val = 0

    if val < 30:
        fill_color = (0, 120, 0, 255)    # 深绿色：待机/省电
    elif val < 55:
        fill_color = (204, 153, 0, 255)      # 黄色：中度负载
    else:
        fill_color = (200, 0, 0, 255)    # 强力红：高性能/插电爆发

    img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
    dc = ImageDraw.Draw(img)
    
    text_len = len(text)
    font_size = 55 if text_len <= 2 else 50
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 计算文字位置使其居中
    bbox = dc.textbbox((0, 0), text, font=font)
    w_txt = bbox[2] - bbox[0]
    h_txt = bbox[3] - bbox[1]
    
    dc.text(((64 - w_txt) // 2, (64 - h_txt) // 2 - 8), text, font=font, fill=fill_color)
    
    return img

def update_logic(icon):
    global current_power_str
    icon.visible = True
    
    while icon.visible:
        # 1. 获取数据
        val = get_battery_power()
        current_power_str = val
        
        # 2. 更新托盘图标数字
        icon.icon = create_transparent_icon(format_power_for_tray(val))
        
        # 3. 更新鼠标悬停文字
        icon.title = f"实时功耗: {val} W"
        
        # 4. 菜单
        icon.menu = pystray.Menu(
            item("退出程序", on_exit)
        )
        
        time.sleep(2)

def on_exit(icon, item):
    icon.visible = False
    icon.stop()

def setup():
    # 初始显示
    icon = pystray.Icon("PowerMonitor", 
                        icon=create_transparent_icon("..."), 
                        title="功耗监控启动中...")
    
    # 初始化菜单
    icon.menu = pystray.Menu(
        item(f"当前总功耗: -- W", lambda: None, enabled=False),
        item("退出", on_exit)
    )
    
    # 启动异步更新线程
    update_thread = threading.Thread(target=update_logic, args=(icon,), daemon=True)
    update_thread.start()
    
    icon.run()

if __name__ == "__main__":
    setup()
```