from ParkingDetector import ParkingDetector
from Yolo import Yolo
from ocr import OCR
import cv2
import multiprocessing
import os

class SystemController:
    def __init__(self, cameras):
        #Inicializa os módulos de detecção de vagas, YOLO e OCR
        self.parking = ParkingDetector()
        self.yolo = Yolo()
        self.ocr = OCR()
        #Lista de câmeras (caminhos RTSP ou arquivos de vídeo)
        self.cameras = cameras

    def camera_process(self, camera_path):
        #Pega o identificador da câmera a partir do caminho (última parte do caminho)
        camera_id = camera_path.split('/')[-1]
        print(f'[{camera_id}] Inicializando...')

        #Abre o vídeo ou stream RTSP
        cap = cv2.VideoCapture(camera_path)
        if not cap.isOpened():
            print(f'[{camera_id}] ERRO: Não foi possível abrir o vídeo: {camera_path}')
            return

        while True:
            #Lê o próximo frame do vídeo
            ret, frame = cap.read()
            if not ret:
                print(f'[{camera_id}] Fim do vídeo ou erro na leitura.')
                break

            #Rotaciona o frame para alinhar corretamente (se necessário)
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # Executa a detecção de marcadores de vaga
            frame = self.parking.identificador_marker_frame(frame)

            #Se a vaga estiver ocupada, inicia a detecção de placas com YOLO e OCR
            if self.parking.vaga_ocupada:
                print(f'[{camera_id}] Vaga ocupada - iniciando detecção de placa...')
                crops = self.yolo.PlateDetector(frame)  #Detecta a placa no frame
                for crop in crops:
                    if crop.any():  #Se o crop da placa existir
                        texto = self.ocr.read_plate(crop)  #Lê a placa com OCR
                        print(f'[{camera_id}] Texto lido: {texto}')
                    else:
                        print(f'[{camera_id}] Nenhuma placa válida detectada.')
            else:
                print(f'[{camera_id}] Vaga não ocupada.')  #Se a vaga não estiver ocupada

            #Exibe o frame com as informações de detecção
            cv2.imshow(f'Monitoramento - {camera_id}', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):  #Se pressionar 'q', encerra o loop
                print(f'[{camera_id}] Encerrando monitoramento.')
                break

        #Libera o vídeo e fecha a janela
        cap.release()
        cv2.destroyAllWindows()

    def start(self):
        processes = []
        #Para cada câmera na lista de câmeras, cria um processo em paralelo
        for camera in self.cameras:
            process = multiprocessing.Process(target=self.camera_process, args=(camera,))
            processes.append(process)
            process.start()

        #Aguarda todos os processos terminarem
        for process in processes:
            process.join()


cameras = [
    'rtsp://localhost:8554/camera1',
    'rtsp://localhost:8554/camera2',
    'rtsp://localhost:8554/camera3',
]

controller = SystemController(cameras)
controller.start()