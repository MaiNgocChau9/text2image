# PyQt6
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
import sys

# Google
import google.generativeai as genai
import requests
import io
from PIL import Image

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("c:/Users/Windows/Desktop/text2image/text2image.ui", self)
        self.show()
        self.pushButton.clicked.connect(self.btn_clicked)
        subject = self.lineEdit.text()
        genai.configure(api_key="Gemini API")

    def btn_clicked(self):
        # Gemini API
        generation_config = {"temperature": 1,"top_p": 1,"top_k": 1,"max_output_tokens": 30}
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",generation_config=generation_config)
        response = model.generate_content([f"Generate a prompt (in English) to generate image with 2D style about \"{self.lineEdit.text()}\". Do not respond the prompt with any human (such as a gird, a man, a woman,...). Reply short and only prompt"])
        print(response.text)

        # Hugging Face API
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": "Hugging Face API"}

        def query(payload):
            try:
                # Gửi yêu cầu POST đến API
                response = requests.post(API_URL, headers=headers, json=payload)
                # Nâng lỗi nếu có
                response.raise_for_status()
                # Trả về nội dung phản hồi
                return response.content
            except requests.RequestException as e:
                print("Lỗi:", e)
                return None

        # Nhập mô tả ảnh
        image_description = response.text

        # Gửi yêu cầu API
        image_bytes = query(f"inputs: {image_description}")

        # Lưu hình ảnh
        with open("image.png", "wb") as f:
            f.write(image_bytes)
        
        self.label.setPixmap(QPixmap("image.png").scaled(480, 480))
        self.lineEdit.clear()

try:
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    app.exec()
except Exception as e:
    sys.exit()