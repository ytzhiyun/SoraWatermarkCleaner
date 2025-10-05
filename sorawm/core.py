from pathlib import Path

from sorawm.utils.video_utils import VideoLoader
from sorawm.utils.watermark_utls import (detect_watermark, get_bounding_box,
                                         h_tmpl, w_tmpl)
from sorawm.watermark_cleaner import WaterMarkCleaner
from sorawm.watermark_detector import SoraWaterMarkDetector

# based on the sora tempalte to detect the whole, and then got the icon part area.


class SoraWM:
    def __init__(self, input_video_path: Path, output_video_path: Path):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.input_video_loader = VideoLoader(self.input_video_path)
        self.detector = SoraWaterMarkDetector()
        self.cleaner = WaterMarkCleaner()

    def run(self):
        import cv2
        import ffmpeg
        import numpy as np
        from tqdm import tqdm

        # 确保输出目录存在
        self.output_video_path.parent.mkdir(parents=True, exist_ok=True)

        # 获取视频信息
        width = self.input_video_loader.width
        height = self.input_video_loader.height
        fps = self.input_video_loader.fps
        total_frames = self.input_video_loader.total_frames

        # 创建ffmpeg输出进程
        process_out = (
            ffmpeg.input(
                "pipe:",
                format="rawvideo",
                pix_fmt="bgr24",
                s=f"{width}x{height}",
                r=fps,
            )
            .output(str(self.output_video_path), pix_fmt="yuv420p", vcodec="libx264")
            .overwrite_output()
            .run_async(pipe_stdin=True, pipe_stderr=True)
        )

        try:
            # 遍历所有帧
            for frame in tqdm(
                self.input_video_loader, total=total_frames, desc="处理视频帧"
            ):
                # 检测水印
                detection_result = self.detector.detect(frame)

                if detection_result["detected"]:
                    # 从bounding box创建mask
                    x1, y1, x2, y2 = detection_result["bbox"]
                    mask = np.zeros((height, width), dtype=np.uint8)
                    mask[y1:y2, x1:x2] = 255

                    # 去除水印
                    cleaned_frame = self.cleaner.clean(frame, mask)
                else:
                    # 未检测到水印，使用原帧
                    cleaned_frame = frame

                # 写入输出视频
                process_out.stdin.write(cleaned_frame.tobytes())

        finally:
            # 清理资源
            process_out.stdin.close()
            process_out.wait()

        print(f"视频处理完成，已保存至: {self.output_video_path}")


if __name__ == "__main__":
    from pathlib import Path

    # ========= 配置 =========
    input_video_path = Path(
        "resources/19700121_1645_68e0a027836c8191a50bea3717ea7485.mp4"
    )
    output_video_path = Path("outputs/sora_watermark_removed.mp4")
    # =======================

    # 创建SoraWM实例
    sora_wm = SoraWM(input_video_path, output_video_path)

    # 运行水印去除
    sora_wm.run()
