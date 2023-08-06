import time
import threading
from pynput import mouse
import keyboard

recorded_actions = []
record_clicks = False
stop_playback = False

def on_click(x, y, button, pressed):
    if pressed and record_clicks:
        action = {"time": time.time(), "x": x, "y": y}
        recorded_actions.append(action)
        print(f"Recorded click at position: x = {x}, y = {y}")

def record_mouse_actions():
    global record_clicks
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def play_recorded_actions(actions, repeat):
    global stop_playback
    for _ in range(repeat):
        for action in actions:
            if stop_playback:
                return  # Stop playback if 'q' key is pressed
            mouse.Controller().position = (action["x"], action["y"])
            mouse.Controller().click(mouse.Button.left, 1)
            time.sleep(0.5)  # Add a small delay between clicks if needed

def check_q_key():
    global record_clicks
    global stop_playback
    while True:
        if keyboard.is_pressed("q"):
            if record_clicks:
                record_clicks = False
                print("Recording stopped.")
            else:
                stop_playback = True
                print("Playback stopped.")
            break
        time.sleep(0.1)

def main():
    global record_clicks
    q_thread = threading.Thread(target=check_q_key)
    q_thread.start()

    while True:
        command = input("Type 'record' to start recording or 'play' to play back: ")

        if command == "record":
            print("Recording mouse clicks...")
            recorded_actions.clear()
            record_clicks = True
            recording_thread = threading.Thread(target=record_mouse_actions)
            recording_thread.start()

        elif command == "play":
            if not recorded_actions:
                print("No recorded actions to play. Please record first.")
            else:
                repeat = int(input("Enter the number of times to repeat playback: "))
                global stop_playback
                stop_playback = False
                print("Playing back recorded actions. Move to the terminal window and press 'q' to stop.")
                play_recorded_actions(recorded_actions, repeat)
        else:
            print("Invalid command. Please type 'record' or 'play'.")

if __name__ == "__main__":
    main()
