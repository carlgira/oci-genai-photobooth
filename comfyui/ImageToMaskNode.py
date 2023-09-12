import torch
import numpy as np
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
        temp = (torch.clamp(image[0], 0, 1.0) * 255.0).round().to(torch.int)
        #temp = torch.bitwise_left_shift(temp[:,:,0], 16) + torch.bitwise_left_shift(temp[:,:,1], 8) + temp[:,:,2]
        #mask = torch.where((temp >= color_min) & (temp <= color_max), 255, 0).float()
        #mask = torch.where((temp[:,:,0] > r_min) & (temp[:,:,0] < r_max) & (temp[:,:,1] > g_min) & (temp[:,:,1] < g_max) & (temp[:,:,2] > b_min) & (temp[:,:,2] < b_max), 255, 0).float()
        raw_image = 255. * image[0].numpy()
        image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
        lower_bound = np.array([r_min, g_min, b_min])
        upper_bound = np.array([r_max, g_max, b_max])
        hsv_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(raw_image, lower_bound, upper_bound)
        inverted_mask = cv2.bitwise_not(mask)
        alpha_channel = np.ones(mask.shape, dtype=mask.dtype) * 255
        alpha_channel = cv2.bitwise_and(alpha_channel, alpha_channel, mask=inverted_mask)
        #mask = cv2.merge((image, alpha_channel))
        mask = torch.tensor(mask > 0).float()
        
        return (mask,)
    
NODE_CLASS_MAPPINGS = {
    "ImageColorsToMask": ImageColorsToMask,
}