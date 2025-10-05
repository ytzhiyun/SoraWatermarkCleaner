# SoraWatermarkCleaner

[English](README.md) | 中文

这个项目提供了一种优雅的方式来移除 Sora2 生成视频中的 Sora 水印。


- 移除水印后

https://github.com/user-attachments/assets/8cdc075e-7d15-4d04-8fa2-53dd287e5f4c

- 原始视频

https://github.com/user-attachments/assets/3c850ff1-b8e3-41af-a46f-2c734406e77d




## 1. 方法

SoraWatermarkCleaner（后面我们简称为 `SoraWm`）由两部分组成：

- SoraWaterMarkDetector：我们训练了一个 yolov11s 版本来检测 Sora 水印。（感谢 YOLO！）

- WaterMarkCleaner：我们参考了 IOPaint 的实现，使用 LAMA 模型进行水印移除。

  （此代码库来自 https://github.com/Sanster/IOPaint#，感谢他们的出色工作！）

我们的 SoraWm 完全由深度学习驱动，在许多生成的视频中都能产生良好的效果。



## 2. 安装

我们强烈推荐使用 `uv` 来安装环境：

1. 安装：

```bash
uv sync
```

> 现在环境将被安装在 `.venv` 目录下，你可以使用以下命令激活环境：
>
> ```bash
> source .venv/bin/activate
> ```

2. 下载预训练模型：

训练好的 YOLO 权重将存储在 `resources` 目录中，文件名为 `best.pt`。它将从 https://github.com/linkedlist771/SoraWatermarkCleaner/releases/download/V0.0.1/best.pt 自动下载。`Lama` 模型从 https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt 下载，并将存储在 torch 缓存目录中。两者都是自动下载的，如果失败，请检查你的网络状态。

## 3. 演示

基本用法，只需尝试 `example.py`：

```python

from pathlib import Path
from sorawm.core import SoraWM


if __name__ == "__main__":
    input_video_path = Path(
        "resources/dog_vs_sam.mp4"
    )
    output_video_path = Path("outputs/sora_watermark_removed.mp4")
    sora_wm = SoraWM()
    sora_wm.run(input_video_path, output_video_path)

```

我们还提供了基于 `streamlit` 的交互式网页界面，使用以下命令尝试：

```bash
streamlit run app.py
```

<img src="resources/app.png" style="zoom: 25%;" />

## 4. 许可证

Apache License



## 5. 引用

如果你使用了这个项目，请引用：

```bibtex
@misc{sorawatermarkcleaner2025,
  author = {linkedlist771},
  title = {SoraWatermarkCleaner},
  year = {2025},
  url = {https://github.com/linkedlist771/SoraWatermarkCleaner}
}
```

## 6. 致谢

- [IOPaint](https://github.com/Sanster/IOPaint) 提供的 LAMA 实现
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) 提供的目标检测
