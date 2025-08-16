import cv2 as cv
from cv2 import aruco
import numpy as np

class ParkingDetector:
    def __init__(self): 
        #self: chama outro método, guarda um valor permanente, acessa dados do objeto dentro da mesma classe, interliga funções e possibilita do objeto ser usado em outras classes
        #init: atribui valores, parametros, salva valores na própria classe, construtor da classe, que é chamado quando uma instância da classe ParkingDetector é criada. Ele inicializa variáveis e salva o comportamento do objeto.
        
        #Inicializa a gravação
        self.cap = cv.VideoCapture() 
        self.fps = self.cap.get(cv.CAP_PROP_FPS)
        
        #Definir fps 
        self.new_fps = 60
        self.tempo_espera = int(1000 / self.new_fps) # Converte FPS para tempo de espera em ms

        #Se o marcador for identificado o veículo não está na vaga, do contrátrio está na vaga
        self.vaga_ocupada = False

        #Dicionario e detector
        self.aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250) #Define um dicionário de marcadores ArUco. 
        self.parameters = cv.aruco.DetectorParameters() #Inicializa oa parametros do identificador de marcadores
        self.detector = cv.aruco.ArucoDetector(self.aruco_dict, self.parameters) #Cria um detector de marcadores ArUco

    # iterate through multiple frames, in a live video feed
    def identificador_marker_frame(self, frame):

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #Converte o quadro de entrada para escala de cinza.
        marker_corners, marker_IDs, reject = self.detector.detectMarkers(gray_frame) #Chama o método detectMarkers do detector ArUco, que encontra os marcadores no quadro

        # getting conrners of markers
        if marker_corners:
            #QrCode visível->vaga não ocupada
            if self.vaga_ocupada:
                #print('Vaga não ocupada!')
                self.vaga_ocupada=False

            for ids, corners in zip(marker_IDs, marker_corners): #Para cada marcador detectado se desenha uma linha ao redor do marcador com o cv.polylines
                cv.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                )
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left = corners[3].ravel()
                cv.putText(
                    frame,
                    f"id: {ids[0]}",
                    top_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (200, 100, 0),
                    2,
                    cv.LINE_AA,
                )
                # print(ids, "  ", corners)
        else:
            #QrCode não visível-> vaga ocupada
            if not self.vaga_ocupada:
                #print('Vaga ocupada!')
                self.vaga_ocupada=True

        return frame

    def iniciar_video(self):

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame=self.identificador_marker_frame(frame) #Processa o quadro atual para detectar marcadores e definir se a vaga ta ocupada

            #video_writer.write(frame)
            cv.imshow('frame', frame)
            key = cv.waitKey(self.tempo_espera)
            if key == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()

Detector = ParkingDetector()
#Detector.iniciar_video()

#name: guarda o nome do arquivo que ta sendo executado, e o valor main é quando o arquivo é executado ou vai ser
#if __name__ == '__main__'