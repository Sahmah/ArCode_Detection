from ultralytics import YOLO
import os
import time
from ultralytics.utils.plotting import save_one_box

class Yolo:

    def __init__(self, model_path= 'yolo11n.pt'):
        self.model = YOLO(model_path)

    def PlateDetector(self, frame):

        if frame is None: #Verifica se o frame não está vazio
            print('Frame inválido passado para o detector.')
            return None

        #Roda a detecção no frame, salva crops
        results = self.model.predict(
            source=frame,
            #save=True,
            save_crop=False,
            #project='CropsVoxSC/yolo_results', #Salva e cria na pasta definida
            #name='detect', #Subdiretório
            #exist_ok=True #Sobrescreve nos arquivos existentes
        )
        #O sistema deve não salvar no disco, passando os crops da Placa diretamente pra o ocr sem salvar

        #results = self.model(frame, save_crop=False)
        #O que eu to retonando aqui são caixas delimitadoras
        crops = [save_one_box(b, results[0].orig_img, BGR=True, save=False) for b in results[0].boxes.xyxy]
        #b: itera cada uma das caixas delimitadoras
        #save_one_box: recorta a região da imagem original de acordo com o b
        return crops

        '''
        crop_dir = 'CropsVoxSC/yolo_results/detect/crops/Pallet' #Caminhos onde os crops vão ser guardados

        if os.path.exists(crop_dir): #Se o caminho existe
            crops = os.listdir(crop_dir) #Lista os arquivos do caminho
            crops.sort() #Organiza os arquivos
            if len(crops) >= 1: #Garantir que tenha pelo menos 1 crop
                    crop_path = os.path.join(crop_dir, crops[0]) #Caminho da pasta até a imagem da placa
                    print(f'Placa detectada: {crop_path}')
                    return crop_path
            else: #Se não tiver nenhum crop
                print('Imagem da placa não encontrada.')
                return None
        else: #Se a pasta dos crops não existe
            print('Pasta das placas não encontrada.')
            return None
        '''



Detect = Yolo()
#Detect.PlateDetector()