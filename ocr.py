import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from Yolo import Yolo
from PIL import Image, ImageFont
import paddle
import os

#Leitor OCR: Pega o corte da placa em especifico e lê o que está na placa
class OCR:
    def __init__(self):
        # Forçando o OCR a rodar na CPU
        self.ocr = PaddleOCR(use_angle_cls=True, lang='pt', use_gpu=False)  # Use CPU

    def read_plate(self, image):
        print(f'Lendo a placa...')

        result = self.ocr.ocr(image, cls=True)[0]

        if not result:
            print('Nenhum texto detectado')
            return None

        boxes = [line[0] for line in result]
        txt = [line[1][0] for line in result]
        scores = [line[1][1] if isinstance(line[1][1], float) else line[1][1][0] for line in result]

        im_show = draw_ocr(image, boxes, txt, scores, font_path='Fonte_txt/Roboto-VariableFont_wdth,wght.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('placa_ocr.jpg')

        return txt[0]


