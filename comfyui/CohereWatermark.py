import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from torchvision import transforms
import cv2

transform = transforms.Compose([
    transforms.ToTensor()
])

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)


def add_watermark(base_img_path, top, font_path, text):
    base = Image.open(base_img_path)
    
    width, height = top.size
    
    scale_factor = min(1024 / width, 768 / height)
    
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    resized_top_image = top.resize((new_width, new_height))
    
    base.paste(resized_top_image, (1044//2 - new_width//2, 778//2 - new_height//2))
    
    draw = ImageDraw.Draw(base)
    rect_position = (30, 860, 1024, 915)
    font_size=20
    font = ImageFont.truetype(font_path, font_size)
    
    max_width, max_height = rect_position[2] - rect_position[0], rect_position[3] - rect_position[1]
    words = text.split()
    lines = []
    while words:
        line = ''
        while words:
            if get_text_dimensions(line + words[0] + ' ', font)[0] <= max_width:
                line += (words.pop(0) + ' ')
            else:
                break
        lines.append(line)
    
    
    current_height = 0
    for line in lines:
        if current_height + get_text_dimensions(line, font)[1] <= max_height:
            draw.text((rect_position[0], rect_position[1] + current_height), line, font=font, fill="white")
            current_height += get_text_dimensions(line, font)[1]
        else:
            break

    return base

class CohereWatermark:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": {
                    "image": ("IMAGE",),
                    "text": ("TEXT", {"input_format": {"text": "STRING"}}),
                }
        }

    CATEGORY = "image"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "cohere_watermark"

    def cohere_watermark(self, image, text):
        watermark_path = "/home/opc/ComfyUI/custom_nodes/genai_template.png" # FIX Add as params
        font_path = "/home/opc/ComfyUI/custom_nodes/CohereVariable.ttf" # FIX Add as params
        raw_image = 255 * image[0].numpy()
        pil_image = Image.fromarray(raw_image.astype(np.uint8))
        
        result = add_watermark(watermark_path, pil_image, font_path, text)
        
        i = ImageOps.exif_transpose(result)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        
        return (image,)
    
NODE_CLASS_MAPPINGS = {
    "CohereWatermark": CohereWatermark,
}