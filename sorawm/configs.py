from pathlib import Path
from re import T

ROOT = Path(__file__).parent.parent


RESOUCRES_DIR = ROOT / "resources"
WATER_MARK_TEMPLATE_IMAGE_PATH = RESOUCRES_DIR / "watermark_template.png"

WATER_MARK_DETECT_YOLO_WEIGHTS = RESOUCRES_DIR / "best.pt"

OUTPUT_DIR = ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


DEFAULT_WATERMARK_REMOVE_MODEL = "lama"

