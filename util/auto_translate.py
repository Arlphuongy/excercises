import pyautogui
import time
import os
import glob
import re
import subprocess
import random


def write_text(text, interval=0.0, next_key=None):
    pyautogui.write(text, interval=interval)  # write text
    time.sleep(0.1)

    if next_key:
        pyautogui.press(next_key)  # press enter


# polling
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


def click_at_position(x, y, button="left", duration=0):
    time.sleep(0.05)
    pyautogui.moveTo(x, y, duration=duration)

    if button:
        pyautogui.click(button=button)
    time.sleep(0.05)


def universal_command(keys):
    time.sleep(0.05)
    if not 2 <= len(keys) <= 4:
        raise ValueError("The list of keys must contain between 2 and 4 elements.")

    command_pressed = False
    ctrl_pressed = False
    shift_pressed = False

    for i, key in enumerate(keys):
        if key == "command":
            pyautogui.keyDown(key)
            command_pressed = True
            time.sleep(0.1)
        elif key == "ctrl":
            pyautogui.keyDown(key)
            ctrl_pressed = True
            time.sleep(0.1)
        elif key == "shift":
            pyautogui.keyDown(key)
            shift_pressed = True
            time.sleep(0.1)
        else:
            pyautogui.press(key)
            time.sleep(0.1)

    if command_pressed:
        pyautogui.keyUp("command")
    if ctrl_pressed:
        pyautogui.keyUp("ctrl")
    if shift_pressed:
        pyautogui.keyUp("shift")

    time.sleep(0.05)


def numerical_sort_key(s):
    # Updated pattern to match 'dataset_' followed by 1 to 3 digits
    match = re.search(r"dataset_(\d{1,3})", os.path.basename(s))

    if match:
        # Extract and return the sentence number as an integer
        return int(match.group(1))
    else:
        # Return a default value or raise an error if the pattern is not found
        return None  # or raise ValueError("Pattern not found")


def process_file(folder_path, file, retries=1):
    # "src / temp / dataset_1.docx"
    base_filename, extension = os.path.splitext(os.path.basename(file))
    translation_filename = f"{base_filename}_t{extension}"
    start_time = time.time()

    subprocess.call(["open", file])
    time.sleep(1.5)
    time.sleep(1.5)

    universal_command(["command", "ctrl", "f"])  # full screen

    # open translation
    click_at_position(515, 100, button="left", duration=0.25)
    click_at_position(400, 130, button="left", duration=0.25)
    click_at_position(400, 180, button="left", duration=0.25)
    time.sleep(1.5)
    time.sleep(1.5)

    # press translation button
    click_at_position(2000, 390, button="left", duration=1.5)

    # check if translation succeed
    translation_flag = is_button_present("_img/dictate_button.png", timeout=60)

    if translation_flag:
        time.sleep(0.5)
        universal_command(["command", "s"])

        time.sleep(0.5)
        time.sleep(1.5)
        write_text(translation_filename, 0, "enter")

        time.sleep(0.5)
        universal_command(["command", "w"])

    else:
        print(f"Failed to tranlate {file}")

    time.sleep(0.5)
    universal_command(["command", "w"])

    processing_time = time.time() - start_time
    print(f"Processing time for {file}: {processing_time:.2f} seconds")

    if os.path.exists(os.path.join(folder_path, translation_filename)):
        print(f"Translation saved to {translation_filename}")
    else:
        universal_command(["command", "w"])
        print(f"Failed to save translation for {file}")
        if retries > 0:
            print(f"Retrying... {retries} attempts left")
            process_file(folder_path, file, retries - 1)
        else:
            raise Exception(f"Failed to process file after 2 attempts: {file}")


def get_last_processed_file_index(docx_files, folder_path):
    last_index = -1
    for i, file in enumerate(docx_files):
        base_filename, extension = os.path.splitext(os.path.basename(file))
        translation_filename = f"{base_filename}_t{extension}"
        if os.path.exists(os.path.join(folder_path, translation_filename)):
            last_index = i

    return last_index


def process_files(folder_path, base_filename):
    docx_pattern = f"{folder_path}/{base_filename}_*.docx"
    docx_files = glob.glob(docx_pattern)
    docx_files = [f for f in docx_files if not f.endswith("_t.docx")]
    docx_files.sort(key=numerical_sort_key)

    last_processed_index = get_last_processed_file_index(docx_files, folder_path)

    for file in docx_files[last_processed_index + 1 :]:
        try:
            process_file(folder_path, file)

        except Exception as e:
            print(e)
            wait_time = random.randint(600, 720)  # Random between 10 to 12 min
            print(
                f"Encountered an error. Waiting for {wait_time / 60:.2f} minutes before trying the next file."
            )
            time.sleep(wait_time)
            # Continue to the next file without breaking the loop
            continue


def main():

    # en/mixz2_s/dataset_zlib2_c_1_sentence_1.docx
    folder_path = "src/temp"
    base_filename = "dataset"

    process_files(folder_path, base_filename)


if __name__ == "__main__":
    main()

    # def get_mouse_position():
    #     x, y = pyautogui.position()
    #     print(f"The current mouse position is {x}, {y}")
    #     return x, y

    # time.sleep(3)
    # x, y = get_mouse_position()
