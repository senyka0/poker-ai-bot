from openai import OpenAI
import base64
import numpy as np
import os
import time
import cv2
import pyautogui
import matplotlib.pyplot as plt

image_path = "./board.png"
SCREENSHOT_H = slice(0, 860) # H position of poker window from top to bottom
SCREENSHOT_W = slice(0, 1015) # W position of poker window from left to right
TURN_H = slice(510, 610) # H position of avatart to track if it is your trun
TURN_W = slice(450, 550) # W position of avatart to track if it is your trun

client = OpenAI(api_key="") # Your OpenAI API key


def encode():
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


def is_my_turn():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = screenshot[TURN_H, TURN_W]
    return screenshot.mean() > 90 and screenshot.mean() < 110 # adjust to track if it is your turn


while True:
    if is_my_turn():
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = screenshot[SCREENSHOT_H, SCREENSHOT_W]
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        result, encimg = cv2.imencode('.jpg', screenshot, encode_param)
        if result:
            with open(image_path, mode='wb') as f:
                f.write(encimg)
        base64_img = encode()
        print("Move")
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "If you were a math expert, considering all metrics and game theory, what would you choose? Choose only between [fold, check/call, bet/raise, x2bet, x3bet, x4bet, x5bet, 1/2pot, 2/3pot, pot, allin] give me only answer. Do not fold if you can just check.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_img}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        move = response.choices[0].message.content.lower()
        print(move)

         # Adjust hotkeye !
        if move in "fold":
            pyautogui.hotkey('ctrl', 'left')
        elif move in "check/call":
            pyautogui.hotkey('ctrl', 'down')
        elif move in "bet/raise":
            pyautogui.hotkey('ctrl', 'right')
        elif move in "x2bet":
            pyautogui.hotkey('ctrl', '2')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "x3bet":
            pyautogui.hotkey('ctrl', '3')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "x4bet":
            pyautogui.hotkey('ctrl', '4')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "x5bet":
            pyautogui.hotkey('ctrl', '5')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "1/2pot":
            pyautogui.hotkey('ctrl', '6')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "2/3pot":
            pyautogui.hotkey('ctrl', '7')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "pot":
            pyautogui.hotkey('ctrl', '8')
            pyautogui.hotkey('ctrl', 'right')
        elif move in "allin":
            pyautogui.hotkey('ctrl', '0')
            pyautogui.hotkey('ctrl', 'right')
            pyautogui.hotkey('ctrl', 'down')

        os.remove(image_path)
        time.sleep(5)
    else:
        time.sleep(1)
