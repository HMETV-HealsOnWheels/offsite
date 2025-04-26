import socket
import tkinter as tk
from tkinter import Toplevel, Label

TCP_IP = '192.168.1.9'  # Pi’s IP
TCP_PORT = 5001

def send_instruction(instruction):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_IP, TCP_PORT))
            s.sendall(instruction.encode('utf-8'))
            print(f"Sent instruction: {instruction}")
            output_text.insert(tk.END, f"Sent: {instruction}\n")
            show_temp_popup("Sent successfully!")
    except Exception as e:
        error_msg = f"Failed to send: {e}"
        print(error_msg)
        output_text.insert(tk.END, error_msg + "\n")

def show_temp_popup(message):
    popup = Toplevel()
    popup.title("Info")
    popup.geometry("200x50+500+300")  # Width x Height + X + Y
    popup.attributes("-topmost", True)
    Label(popup, text=message, padx=10, pady=10).pack()
    popup.after(1000, popup.destroy)  # Auto-close after 1 sec

def launch_gui():
    def send_command():
        cmd = command_entry.get().strip().lower()
        duration = duration_entry.get().strip()

        if cmd not in ["forward", "backward", "left", "right", "stop", "wait", "done", "emergency-stop"]:
            output_text.insert(tk.END, f"Invalid command: {cmd}\n")
            return

        if not duration.isdigit() and cmd != "emergency-stop":
            output_text.insert(tk.END, f"Invalid duration: {duration}\n")
            return

        instruction = f"{cmd},{duration}" if cmd != "emergency-stop" else f"{cmd},0"
        send_instruction(instruction)

    def emergency_stop():
        send_instruction("emergency-stop,0")

    def send_path1():
        path = [
            "forward,20000",
            "done,0"
        ]
        output_text.insert(tk.END, "Sending path1:\n")
        for instruction in path:
            output_text.insert(tk.END, f"  {instruction}\n")
        output_text.insert(tk.END, "-------------------\n")

        for instruction in path:
            send_instruction(instruction)


    root = tk.Tk()
    root.title("Robot Client GUI")

    tk.Label(root, text="Command:").grid(row=0, column=0, padx=5, pady=5)
    command_entry = tk.Entry(root)
    command_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Duration (ms):").grid(row=1, column=0, padx=5, pady=5)
    duration_entry = tk.Entry(root)
    duration_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(root, text="Send Command", command=send_command).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(root, text="Emergency Stop", bg="red", fg="white", command=emergency_stop).grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(root, text="Send Path1", bg="skyblue", command=send_path1).grid(row=4, column=0, columnspan=2, pady=5)
    #tk.Button(root, text="Send Path2", bg="skyblue", command=send_path2).grid(row=5, column=0, columnspan=2, pady=5)


    global output_text
    output_text = tk.Text(root, height=12, width=40)
    output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()

