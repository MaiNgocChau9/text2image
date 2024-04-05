import google.generativeai as genai
import requests
import io

subject = input("Subject: ")

genai.configure(api_key="Gemini API")
# Set up the model
generation_config = {"temperature": 1,"top_p": 1,"top_k": 1,"max_output_tokens": 30}
model = genai.GenerativeModel(model_name="gemini-1.0-pro",generation_config=generation_config)

prompt_parts = [f"Generate a prompt (in English) to generate image with 2D style about \"{subject}\". Do not respond the prompt with any human (such as a gird, a man, a woman,...). Reply short and only prompt"]
response = model.generate_content(prompt_parts)
print("Prompt:", response.text)
print("Image is generating...")

# API
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
image_bytes = query({"inputs": image_description})

# Lưu hình ảnh
with open("image.png", "wb") as f:
    f.write(image_bytes)

# Hiển thị ảnh
"""
if image_bytes:
    image = Image.open("image.png")
    image.show()
else:
    print("Lỗi: Không tìm thấy dữ liệu ảnh.")
"""