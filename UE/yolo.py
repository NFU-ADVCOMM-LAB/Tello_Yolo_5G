import torch
from PIL import Image, ImageDraw, ImageFont

class yolov5_addon:
    def __init__(self,weight_path):
        self.model = torch.hub.load('./yolov5', 'custom', weight_path, source = "local")
        self.bounding_box_color = "blue"
    def draw_bounding_box(self, image, xyxy_list, label_classes):
        image = Image.fromarray(image)
        if (xyxy_list != []):
            draw = ImageDraw.Draw(image)
            for result in xyxy_list:
                result_name = "{0} {1:.2f}".format(label_classes[int(result[5])], result[4])
                xyxy = result[0:4]
                box_shape = [(xyxy[0], xyxy[1]), (xyxy[2], xyxy[3])]
                draw_text = " " + result_name + " "
                text_shape = (xyxy[0],xyxy[1])
                text_font = ImageFont.truetype('arial.ttf', 30)
                text_box_shape = [(xyxy[0], xyxy[1] - 25), (xyxy[0] + text_font.getlength(draw_text), xyxy[1])]
                draw.rectangle(box_shape, outline = self.bounding_box_color, width=5)
                draw.rectangle(text_box_shape, fill = self.bounding_box_color)
                draw.text(text_shape, draw_text, fill = "white", anchor = "lb", font = text_font)
        return image
    def pred(self,image):
        results = self.model(image)
        image = self.draw_bounding_box(image, results.xyxy[0], results.names)
        return image