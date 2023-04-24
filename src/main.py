import tkinter as tk
from tkinter import ttk
from tkinter import *
import sv_ttk
from yt_dlp import YoutubeDL

def main():

    root = tk.Tk()

    audioToggle = IntVar(root)
    audioToggle.set(0)

    root.geometry("640x480")

    sv_ttk.set_theme("dark")

    def downloadVideo():
        progressBar.pack(anchor="center")
        url = inputBox.get("1.0", "end-1c")
        ydl_opts = {
            'progress_hooks': [progress_hook],
        }

        if audioToggle.get():
            ydl_opts.update({"format": "bestaudio"})

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)

    def optionsWindow():
        clearScreen()
        audio = ttk.Checkbutton(root, text="Audio Only", variable=audioToggle, onvalue=1, offvalue=0)
        audio.pack()

    inputBox = tk.Text(root, height=10, width=50)
    inputBox.config(borderwidth=2, relief='groove')
    downloadButton = ttk.Button(root, text="Download", command = downloadVideo)
    optionsButton = ttk.Button(root, text="Options", command = optionsWindow)
    progressBar = ttk.Progressbar(root, length=300)

    def mainWindow():
        inputBox.pack(anchor='center')
        downloadButton.pack(anchor='center')
        optionsButton.pack(anchor='center')

    mainWindow()

    def clearScreen():
        for widget in root.winfo_children():
            widget.destroy()

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = float(d['downloaded_bytes'] / d['total_bytes'] * 100)
            progressBar['value'] = percent
            progressBar.update()

    root.mainloop()

if __name__ == '__main__':
    main()