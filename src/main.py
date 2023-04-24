import tkinter as tk
from tkinter import ttk
import sv_ttk
from yt_dlp import YoutubeDL

def main():

    root = tk.Tk()

    root.geometry("640x480")

    inputBox = tk.Text(root, height=10, width=50)
    inputBox.pack()

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = float(d['downloaded_bytes'] / d['total_bytes'] * 100)
            progressBar['value'] = percent
            progressBar.update()

    def downloadVideo():
        url = inputBox.get("1.0", "end-1c")
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)

    button = tk.Button(root, text="Download Youtube Video", command = downloadVideo)
    button.pack()

    progressBar = ttk.Progressbar(root, length=300)
    progressBar.pack()

    sv_ttk.set_theme("dark")

    root.mainloop()


if __name__ == '__main__':
    main()