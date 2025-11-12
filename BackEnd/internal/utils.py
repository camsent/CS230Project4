import cv2
import pytesseract
import os
import numpy as np
from transformers import pipeline
import requests
from huggingface_hub import InferenceClient



# get grayscale image
def get_grayscale(image):
    try:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        print(f"[ERROR] Failed to convert image to grayscale: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return None
        

# noise removal
def remove_noise(image):
    try:
        return cv2.medianBlur(image, 5)
    except cv2.error as e:
        print(f"[ERROR] Noise removal failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected noise removal error: {e}")
        return None


# thresholding
def thresholding(image):
    try:
        _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    except cv2.error as e:
        print(f"[ERROR] Thresholding failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected thresholding error: {e}")
        return None


# dilation
def dilate(image):
    try:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)
    except cv2.error as e:
        print(f"[ERROR] Dilation failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected dilation error: {e}")
        return None


# erosion
def erode(image):
    try:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)
    except cv2.error as e:
        print(f"[ERROR] Erosion failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected erosion error: {e}")
        return None


# opening (erosion followed by dilation)
def opening(image):
    try:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    except cv2.error as e:
        print(f"[ERROR] Opening (morphology) failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected opening error: {e}")
        return None


# canny edge detection
def canny(image):
    try:
        return cv2.Canny(image, 100, 200)
    except cv2.error as e:
        print(f"[ERROR] Canny edge detection failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected canny error: {e}")
        return None


# skew correction
def deskew(image):
    try:
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        return rotated
    except cv2.error as e:
        print(f"[ERROR] Deskew failed: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected deskew error: {e}")
        return None


def extract_image_text(contents): 
    
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    gray = get_grayscale(img)
    denoised = remove_noise(gray)
    thresh = thresholding(denoised)
    fixed = deskew(thresh)

    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    text = pytesseract.image_to_string(fixed, lang='eng')
    return text 
<<<<<<< HEAD
=======



hf_token = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/meta-llama/Meta-Llama-3.1-8B-Instruct"

headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}

#client = InferenceClient()
def create_flashcards(text: str):
    prompt = f"""
        Generate 3 study flashcards from this text. 
        Format each flashcard as:

        Q: <question text>
        A: <answer text>
        Separate flashcards with the symbol |||
        Text: {text}
    """ 
    payload = {
        "messages": [
            {
            "role": "user",
            "content": prompt
            }
        ],
        "model": "openai/gpt-oss-120b:fastest",  
        "stream": False
    }

    response = requests.post(
        "https://router.huggingface.co/v1/chat/completions",
        headers=headers,
        json=payload
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]
    
    
# TODO: parse response data into a list of flash cards

def to_flashcard_list(flashcards): 
    
    prams = {"Q", "A", "|||"}
    
    flashcard_generatory = dict()
    result = []
    
    flash_list = flashcards.split()
    
    idx = 0 
    while idx < len(flash_list): 
        constructor = []
        if flash_list[idx] == "A" or flash_list[idx] == "Q": 
            pass
    
    
    print(flash_list) 
>>>>>>> e6260db8ada0924a339fa6da5cdbda3c64e97dad
