import threading
import tkinter as tk
from tkinter.filedialog import *
from pytube import YouTube, request


# dark mode :
def darkmode():
    global btnState
    if btnState:
        btn.config(image=offImg, bg="#CECCBE", activebackground="#CECCBE")
        root.config(bg="#CECCBE")
        txt.config(text="Dark Mode: OFF", bg="#CECCBE")
        btnState = False
    else:
        btn.config(image=onImg, bg="#2B2B2B", activebackground="#2B2B2B")
        root.config(bg="#2B2B2B")
        txt.config(text="Dark Mode: ON", bg="#2B2B2B")
        btnState = True


is_paused = is_cancelled = False


def download_media(url,filename,audioOnly=False):
    if(url):
        global is_paused, is_cancelled
        download_button['state'] = 'disabled'
        download_audio_button['state'] = 'disabled'
        pause_button['state'] = 'normal'
        cancel_button['state'] = 'normal'
        var = optMval.get()
        try:
            progress['text'] = 'Connecting ...'
            yt = YouTube(url)
            if(audioOnly):
                stream = yt.streams.filter(subtype='mp4',only_audio=True).first()
                filename = filename + '/' + yt.title + '.mp3'
            else:
                stream = yt.streams[res_list_db[var]]
                filename = filename + '/' + yt.title + '.mp4'
            filesize = stream.filesize
            with open(filename, 'wb') as f:
                is_paused = is_cancelled = False
                stream = request.stream(stream.url)
                downloaded = 0
                while True:
                    if is_cancelled:
                        progress['text'] = 'Download cancelled'
                        break
                    if is_paused:
                        continue
                    chunk = next(stream, None)
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress['text'] = f'Downloaded {downloaded} / {filesize}'
                    else:
                        # no more data
                        progress['text'] = 'Download completed'
                        break
            print('done')
        except Exception as e:
            print(e)
        download_button['state'] = 'normal'
        download_audio_button['state'] = 'normal'
        pause_button['state'] = 'disabled'
        cancel_button['state'] = 'disabled'

def check_quality():
    yt = YouTube(url_entry.get())
    counter = 0
    global res_list_db
    res_list_db = {}
    for strm in yt.streams:
        if strm.mime_type != "audio/webm" and strm.resolution != None:
            text = str(strm.resolution) + " - " + str(strm.fps) + "fps - " + str(strm.video_codec) 
            res_list_db[text] = counter
            menu["menu"].add_command(label=text, command=tk._setit(optMval, text))
            counter +=1
    download_button["state"] = "normal"
    download_audio_button["state"] = "normal"

def start_download():
    filename = askdirectory()
    threading.Thread(target=download_media, args=(url_entry.get(),filename), daemon=True).start()

def start_audio_download():
    filename = askdirectory()
    threading.Thread(target=download_media, args=(url_entry.get(),filename,True), daemon=True).start()


def toggle_download():
    global is_paused
    is_paused = not is_paused
    pause_button['text'] = 'Resume' if is_paused else 'Pause'


def cancel_download():
    global is_cancelled
    is_cancelled = True


# gui
root = Tk()
root.title("Youtube Downloader")
root.iconbitmap("main img/icon.ico")
root.geometry("500x700")

# OptionsMenu default value
optMval = StringVar(root)
optMval.set("-")

# switch toggle:
btnState = False

# switch images:
onImg = PhotoImage(file="dark img/switch-on.png")
offImg = PhotoImage(file="dark img/switch-off.png")

# Copyright
originalBtn = Button(root, text="Made by Swapnil", font="Rockwell", relief="flat")
originalBtn.pack(side=BOTTOM)

# Night Mode:
txt = Label(root, text="Dark Mode: OFF", font="FixedSys 17", bg="#CECCBE", fg="green")
txt.pack(side='bottom')

# switch widget:
btn = Button(root, text="OFF", borderwidth=0, command=darkmode, bg="#CECCBE", activebackground="#CECCBE", pady=1)
btn.pack(side=BOTTOM, padx=10, pady=10)
btn.config(image=offImg)

# main icon section
file = PhotoImage(file="main img/youtube.png")
headingIcon = Label(root, image=file)
headingIcon.pack(side=TOP, pady=3)

# Url Field
url_entry = Entry(root, justify=CENTER, bd=5, fg='green')
url_entry.pack(side=TOP, fill=X, padx=10)
url_entry.focus()

# Download Button
download_img = PhotoImage(file="btnimgs/Download.png")
download_button = Button(root, image=download_img, command=start_download,borderwidth=0,bg=None)
download_button.pack(side=TOP, pady=10)

# Check Quality Button
check_quality_button = Button(root, text="Check Quailty", width=12, command=check_quality, font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
check_quality_button.pack(side=TOP, pady=5)

# OptionsMenu
menu = OptionMenu(root, optMval, "")
menu.pack()

# Download Audio Button
download_audio_img = PhotoImage(file="btnimgs/Download_Audio.png")
download_audio_button = Button(root, image=download_audio_img,command=start_audio_download,borderwidth=0,bg=None)
download_audio_button.pack(side=TOP, pady=10)

# Progress
progress = Label(root)
progress.pack(side=TOP)

# Pause Button
pause_img = PhotoImage(file="btnimgs/Pause.png")
pause_button = Button(root, image=pause_img, command=toggle_download, state='disabled',bg=None,borderwidth=0)
pause_button.pack(side=TOP, pady=10)

# Cancel Button
cancel_img = PhotoImage(file="btnimgs/Cancel.png")
cancel_button = Button(root, image=cancel_img, command=cancel_download, state='disabled',bg=None,borderwidth=0)
cancel_button.pack(side=TOP, pady=10)

# Set button defaults to 
download_button['state'] = 'disabled'
download_audio_button['state'] = 'disabled'

root.mainloop()