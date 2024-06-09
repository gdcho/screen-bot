import pytesseract
from PIL import Image, ImageDraw
import pyautogui
import time
import pyscreenshot as ImageGrab

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def find_text_and_click(target_text, confidence=0.8):
    try:
        screenshot = ImageGrab.grab()

        width, height = screenshot.size
        screenshot_resized = screenshot.resize((width // 2, height // 2))

        text_data = pytesseract.image_to_data(screenshot_resized, output_type=pytesseract.Output.DICT)

        draw = ImageDraw.Draw(screenshot_resized)

        for i in range(len(text_data['text'])):
            text = text_data['text'][i].strip()
            if target_text.lower() in text.lower():
                x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
                center_x, center_y = (x + w // 2), ((y + h // 2))
                draw.rectangle([(x, y), (x + w, y + h)], outline="red")

                pyautogui.moveTo(center_x, center_y)
                time.sleep(0.1) 
                pyautogui.rightClick()
                print(f"Clicked on '{target_text}' at ({center_x}, {center_y})")
                screenshot_resized.show()
                return True

        # screenshot_resized.show()
    except Exception as e:
        print(f"Error: {e}")

    print(f"Text '{target_text}' not found on the screen.")
    return False

def main():
    target_text = "TEXT" 
    interval = 5 

    while True:
        found = find_text_and_click(target_text)
        if found:
            break
        time.sleep(interval)

if __name__ == "__main__":
    main()
