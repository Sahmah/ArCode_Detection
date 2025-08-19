
# 🎥 Sistema de Monitoramento de Vagas com YOLO + OCR

Este projeto implementa um sistema de **monitoramento de câmeras em tempo real**, capaz de:
- Detectar **vagas de estacionamento** (ocupadas ou não).
- Detectar **placas de veículos** utilizando **YOLO**.
- Reconhecer o **texto das placas** com **OCR**.

Ele suporta múltiplas câmeras em paralelo através de **multiprocessing**.

---

## 📂 Estrutura do Projeto
```
├── SystemController.py # Classe principal que gerencia as câmeras
├── ParkingDetector.py # Módulo para detectar vagas de estacionamento
├── Yolo.py # Módulo para detecção de placas com YOLO
├── ocr.py # Módulo para reconhecimento de texto (OCR)
```

---

## ⚙️ Pré-requisitos
Antes de rodar o projeto, instale as dependências necessárias:

```bash
pip install opencv-python ultralytics pytesseract

