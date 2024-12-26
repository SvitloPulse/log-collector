import sys
import tkinter as tk
import serial
from datetime import datetime
import threading
import time
import serial.tools.list_ports

com_ports = [port.device for port in serial.tools.list_ports.comports()]

root = tk.Tk()
root.title("SvitloPulse Logger")

# Set minimum window size
root.minsize(300, 200)

# Create a frame for form layout
form_frame = tk.Frame(root, padx=10, pady=10)
form_frame.pack()

com_port = tk.StringVar()
com_port.set(com_ports[0])

com_port_label = tk.Label(form_frame, text="Оберіть порт:")
com_port_label.grid(row=0, column=0, sticky="w")

# Get a list of available COM ports
com_port_dropdown = tk.OptionMenu(form_frame, com_port, *com_ports)  # Add more COM ports if needed
com_port_dropdown.grid(row=0, column=1, padx=5)

def start_collection():
    selected_port = com_port.get()
    start_button["state"] = "disabled"
    label_text.set("Закрийте вікно програми, щоб припинити збір логів.")
    while True:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{current_datetime}_log.txt"
        log_file = open(log_filename, "w", encoding="utf-8")
        
        try:
            ser = serial.Serial(selected_port, 115200)

            while True:
                data = ser.readline().decode().strip()
                current_datetime = datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f] ")
                log_file.write(current_datetime + data + "\n")
                print(current_datetime + data)
                log_file.flush()
        except serial.SerialException:
            current_datetime = datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f] ")
            log_file.write(current_datetime + "Failed to connect to the COM port.\n")
            print("Failed to connect to the COM port.")
        finally:
            log_file.close()
        time.sleep(0.5)


log_collection_thread = threading.Thread(target=start_collection)
log_collection_thread.daemon = True

label_text = tk.StringVar()
label_text.set("Натисніть кнопку нижче, щоб почати збір логів.")

label = tk.Label(form_frame, textvariable=label_text)
label.grid(row=1, columnspan=2, pady=10)

start_button = tk.Button(form_frame, text="Збирати логи", command=lambda: log_collection_thread.start())
start_button.grid(row=2, columnspan=2, pady=10)


root.mainloop()
sys.exit(0)
