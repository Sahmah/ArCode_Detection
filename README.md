# Controle de Mouse com a Mão (OpenCV + MediaPipe)

Este projeto permite **controlar o mouse usando a webcam** e o **movimento da mão**, em especial o dedo indicador.  
Ele utiliza a biblioteca **OpenCV** para captura de vídeo, **MediaPipe** para detecção das mãos e uma classe auxiliar para simular cliques.

---

## 📌 Funcionalidades
- Captura de vídeo em tempo real via webcam.
- Detecção da mão usando **MediaPipe Hands**.
- Rastreamento do dedo indicador.
- Movimento do cursor de acordo com a posição do dedo.
- Clique do mouse com gestos.

---

## 📂 Estrutura do Projeto
```
├── WebCam.py # Classe principal que captura a webcam
├── Detect_finger.py # Classe que inicializa o MediaPipe e processa mãos
├── Click.py # Classe responsável por mover e clicar o mouse
```
