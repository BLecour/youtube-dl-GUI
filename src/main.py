import tkinter as tk
from tkinter import ttk
from tkinter import *
from yt_dlp import YoutubeDL
from PIL import Image, ImageTk
from urllib.request import urlopen
import sv_ttk

def main():

    root = tk.Tk()

    audioToggle = IntVar(root)
    audioToggle.set(0)
    formatToggle = IntVar(root)
    formatToggle.set(0)
    formatSelection = IntVar(root)


    root.geometry("800x600")
    root.title("youtube-dl GUI")

    sv_ttk.set_theme("dark")

    url = ""
    thumbnailURL = ""

    def progress_hook(d):
        global videoTitle
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = round(float(d['downloaded_bytes'] / d['total_bytes'] * 100), 2)
            else:
                percent = round(float(d['downloaded_bytes'] / d['total_bytes_estimate'] * 100), 2)

            # convert bytes per second to mebibytes per second
            if d['speed'] == None:
                speed = 0.
            else:
                speed = round(float(d['speed']) / 1048576.0, 2)
            
            try:
                seconds = int(d['eta']) % 60
            except:
                seconds = 0

            try:
                minutes = int(d['eta'] / 60)
            except:
                minutes = 0

            progressText.config(text=f"{percent}% of {d['_total_bytes_str']} at {speed}MiB/s\nETA: {minutes:02d}:{seconds:02d}")
            progressBar['value'] = percent
            progressBar.update()
            statusText.config(text=f'Downloading: "{videoTitle}"')
        elif d['status'] == 'finished':
            if d['speed'] == None:
                speed = 0.
            else:
                speed = round(float(d['speed']) / 1048576.0, 2)
            progressText.config(text=f"100.00% of {d['_total_bytes_str']} at {speed}MiB/s\nETA: 00:00")
            progressBar['value'] = 100.0
            statusText.config(text=f'Finished: "{videoTitle}"')

    def downloadVideo():
        statusText.config(text="")
        progressBar.pack()
        progressText.pack(pady=10)
        global url
        url = inputBox.get()
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
                formats = videoInfo.get('formats', None)

            if formatToggle.get():
                popup = tk.Toplevel()
                popup.geometry("300x300")
                popup.wm_title("Select Format")

                canvas = tk.Canvas(popup)
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                scrollbar = ttk.Scrollbar(popup, command=canvas.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                frame = ttk.Frame(canvas)
                canvas.create_window((0, 0), window=frame, anchor=tk.NW)

                for format in formats:
                    if 'filesize' in format:
                        ttk.Radiobutton(frame, text=f"Format ID = {format['format_id']}", variable=formatSelection, value=format['format_id']).pack(pady=20)

                frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox(tk.ALL))

            # if the download is a playlist then 'formats' is empty at first. this avoids error
            if formats != None:
                for format in formats:
                    if 'filesize' in format:
                        print(format['format_id'], format['ext'], format['resolution'], format['fps'], format['filesize'])
                    else:
                        print(format['format_id'], format['ext'], format['resolution'], format['fps'])

                try:
                    thumbnailURL = "http://img.youtube.com/vi/" + videoInfo.get("id", None) + "/0.jpg"
                    print(thumbnailURL)
                    u = urlopen(thumbnailURL)
                    thumbnailData = u.read()
                    u.close()
                    thumbnail = ImageTk.PhotoImage(data=thumbnailData)
                    thumbnailLabel = ttk.Label(image=thumbnail)
                    thumbnailLabel.image = thumbnail
                    thumbnailLabel.pack()

                except Exception as e:
                    statusText.config(text=f"Unable to display thumbnail: {e}")
                ydl.download(url)
        except Exception as e:
            if " is not a valid URL." in str(e):
                statusText.config(text=f'Error: URL "{url}" is not valid.')
            else:
                statusText.config(text=f"Error: {e}")

    def optionsWindow():
        clearScreen()
        ttk.Checkbutton(root, text="Audio Only", variable=audioToggle, onvalue=1, offvalue=0).pack(pady=20)
        ttk.Checkbutton(root, text="Select Format", variable=formatToggle, onvalue=1, offvalue=0).pack(pady=10)
        backButton = ttk.Button(root, text="Back to Main", command=lambda: [clearScreen(), mainWindow()])
        backButton.pack(pady=20)

    def clearScreen():
        for widget in root.winfo_children():
            widget.pack_forget()
        root.update()

    inputBox = ttk.Entry(root, width=40)
    downloadButton = ttk.Button(root, text="Download", command=downloadVideo)
    optionsButton = ttk.Button(root, text="Options", command=optionsWindow)
    progressBar = ttk.Progressbar(root, length=300)
    progressText = ttk.Label(root, justify='center')
    statusText = ttk.Label(root)

    def mainWindow():
        clearScreen()
        ttk.Label(root, text="Enter URL below:").pack(pady=10)
        inputBox.pack(anchor='center', pady=20)
        optionsButton.pack(anchor='center', pady=10)
        downloadButton.pack(anchor='center', pady=10)
        statusText.pack(anchor='center', pady=20)
        statusText.config(text="")

    mainWindow()

    root.mainloop()

if __name__ == '__main__':
    main()