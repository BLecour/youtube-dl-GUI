import tkinter as tk
from tkinter import ttk
from tkinter import *
import sv_ttk
from yt_dlp import YoutubeDL
from time import sleep

def main():

    root = tk.Tk()

    audioToggle = IntVar(root)
    audioToggle.set(0)

    root.geometry("640x480")
    root.title("youtube-dl GUI")

    sv_ttk.set_theme("dark")

    def progress_hook(d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = float(d['downloaded_bytes'] / d['total_bytes'] * 100)
            else:
                percent = float(d['downloaded_bytes'] / d['total_bytes_estimate'] * 100)
            progressBar['value'] = percent
            progressBar.update()

    def downloadVideo():
        statusText.config(text="")
        progressBar.pack(anchor="center")
        url = inputBox.get("1.0", "end-1c")
        ydl_opts = {
            'progress_hooks': [progress_hook],
        }

        if audioToggle.get():
            ydl_opts.update({"format": "bestaudio[ext=m4a]"})

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        except: 
            statusText.config(text=f"URL is not valid.")

    def optionsWindow():
        clearScreen()
        audio = ttk.Checkbutton(root, text="Audio Only", variable=audioToggle, onvalue=1, offvalue=0)
        audio.pack(pady=20)
        backButton = ttk.Button(root, text="Back to Main", command=lambda: [clearScreen(), mainWindow()])
        backButton.pack(pady=20)

    def clearScreen():
        for widget in root.winfo_children():
            widget.pack_forget()
        root.update()

    inputBox = tk.Text(root, height=10, width=50, borderwidth=2, relief='groove')
    downloadButton = ttk.Button(root, text="Download", command=downloadVideo)
    optionsButton = ttk.Button(root, text="Options", command=optionsWindow)
    progressBar = ttk.Progressbar(root, length=300)
    statusText = ttk.Label(root)

    def mainWindow():
        clearScreen()
        inputBox.pack(anchor='center', pady=20)
        downloadButton.pack(anchor='center', pady=10)
        optionsButton.pack(anchor='center', pady=10)
        statusText.pack(anchor='center', pady=20)
        statusText.config(text="")

    mainWindow()

    root.mainloop()

if __name__ == '__main__':
    main()