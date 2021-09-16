import tkinter as tk
import webbrowser
import subprocess
import signal
import time

# Comment by Nick: Automatically opens a GUI which allows interaction between the server and python command line

django_server = subprocess.Popen(['python', 'manage.py', 'runserver', '127.0.0.1:8000'])  # start localserver


 # open browser and call local server

def terminate():
    django_server.send_signal(signal.CTRL_C_EVENT) # quit local server
    window.quit()  # quit tkinter window




window = tk.Tk()
window.title('SurfTheOWL')
window.geometry('600x300')

GUI_head = tk.Label(text='SurfTheOWL')
GUI_info = tk.Text(window,  height=10, width=250)
text = 'SurfTheOwl runs a Localserver in the background,\nto display the OWL dependencies in a Browser.\n\
By terminating this window you also terminate the Localserver.'
GUI_terminate = tk.Button(text='terminate SurfTheOWL', command=terminate, bg='red' )
GUI_head.pack()
GUI_head.config(font=('Arial', 30))
GUI_info.pack()
GUI_info.insert('end', text)
GUI_info.configure(state='disabled')
GUI_terminate.pack()
GUI_terminate.config(font=('Arial', 26))
webbrowser.open("http://127.0.0.1:8000/")

window.mainloop()