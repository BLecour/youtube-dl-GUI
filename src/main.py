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
    root.title("youtube-dl GUI")

    sv_ttk.set_theme("dark")

    url = ""

    def progress_hook(d):
        global videoTitle
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = round(float(d['downloaded_bytes'] / d['total_bytes'] * 100), 2)
            else:
                percent = round(float(d['downloaded_bytes'] / d['total_bytes_estimate'] * 100), 2)
            progressText.config(text=f"{percent}% of {d['_total_bytes_str']} at {d['_speed_str']}")
            progressBar['value'] = percent
            progressBar.update()
            statusText.config(text=f'Downloading: "{videoTitle}"')
        elif d['status'] == 'finished':
            progressText.config(text="100.0%")
            progressBar['value'] = 100.0
            statusText.config(text=f'Finished: "{videoTitle}"')

    def downloadVideo():
        statusText.config(text="")
        progressBar.pack()
        progressText.pack()
        global url
        url = inputBox.get("1.0", "end-1c")
        ydl_opts = {
            'progress_hooks': [progress_hook],
        }

        if audioToggle.get():
            ydl_opts.update({"format": "bestaudio[ext=m4a]"})

        try:
            with YoutubeDL(ydl_opts) as ydl:
                global videoTitle
                videoInfo = ydl.extract_info(url, download=False)
                videoTitle = videoInfo.get('title', None)
                ydl.download(url)
        except Exception as e:
            if " is not a valid URL." in str(e):
                statusText.config(text=f'Error: URL "{url}" is not valid.')
            else:
                statusText.config(text=f"Error: {e}")

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
    progressText = ttk.Label(root)
    statusText = ttk.Label(root)

    def mainWindow():
        clearScreen()
        inputBox.pack(anchor='center', pady=20)
        optionsButton.pack(anchor='center', pady=10)
        downloadButton.pack(anchor='center', pady=10)
        statusText.pack(anchor='center', pady=20)
        statusText.config(text="")

    mainWindow()

    root.mainloop()

if __name__ == '__main__':
    main()