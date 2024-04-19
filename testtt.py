import pyautogui
import time

button_image_src = "img/dictate_button.png"
def is_button_present(button_image_src, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            button_location = pyautogui.locateOnScreen(button_image_src, confidence=0.6)
            if button_location:
                print(f"\tButton found at {button_location}.")
                return True
        except Exception:
            pass
        time.sleep(0.1)  # Wait a bit before checking again

    return False

is_button_present(button_image_src, timeout=60)