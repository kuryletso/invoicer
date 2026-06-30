from io import BytesIO
from PIL import Image

EMU_PER_PX_96_DPI = 9525        # most common case, highly detailed images ~300 dpi will render bigger but

def intristic_emu(image_bytes: bytes) -> tuple[int, int] | None:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            w_px, h_px = img.size
    except Exception:
        return None
    
    return w_px * EMU_PER_PX_96_DPI, h_px * EMU_PER_PX_96_DPI