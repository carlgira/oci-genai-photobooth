import torch
import numpy as np
from PIL import Image
import rembg
import cv2

class ImageColorsToMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": {
                    "image": ("IMAGE",),
                    "r_min": ("INT", {"default": 90, "min": 0, "max": 255, "step": 1, "display": "r_min"}),
                    "g_min": ("INT", {"default": 150, "min": 0, "max": 255, "step": 1, "display": "g_min"}),
                    "b_min": ("INT", {"default": 90, "min": 0, "max": 255, "step": 1, "display": "b_min"}),
                    "r_max": ("INT", {"default": 150, "min": 0, "max": 255, "step": 1, "display": "r_max"}),
                    "g_max": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "g_max"}),
                    "b_max": ("INT", {"default": 150, "min": 0, "max": 255, "step": 1, "display": "b_max"}),
                }
        }

    CATEGORY = "mask"

    RETURN_TYPES = ("MASK",)
    FUNCTION = "image_to_mask"

    def image_to_mask(self, image, r_min, g_min, b_min, r_max, g_max, b_max):
        raw_image = 255. * image[0].numpy()
        image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
        lower_bound = np.array([r_min, g_min, b_min])
        upper_bound = np.array([r_max, g_max, b_max])
        mask = cv2.inRange(raw_image, lower_bound, upper_bound)
        inverted_mask = cv2.bitwise_not(mask)
        alpha_channel = np.ones(mask.shape, dtype=mask.dtype) * 255
        alpha_channel = cv2.bitwise_and(alpha_channel, alpha_channel, mask=inverted_mask)
        mask = torch.tensor(mask > 0).float()
        
        return (mask,)

class RemoveBackgroundAndMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": {
                    "image": ("IMAGE",),
                }
        }

    CATEGORY = "image"

    RETURN_TYPES = ("MASK",)
    FUNCTION = "remove_background_image_to_mask"

    def remove_background_image_to_mask(self, image):
        raw_image = 255 * image[0].numpy()
        pil_image = Image.fromarray(raw_image.astype(np.uint8))
        output = rembg.remove(pil_image)
        output_array = np.array(output)
        gray = cv2.cvtColor(output_array, cv2.COLOR_BGR2GRAY)
        mask = torch.tensor(gray == 0).float()
        
        return (mask,)



NODE_CLASS_MAPPINGS = {
    "ImageColorsToMask": ImageColorsToMask,
    "RemoveBackgroundAndMask": RemoveBackgroundAndMask,
}