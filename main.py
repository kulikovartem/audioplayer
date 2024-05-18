import tkinter as tk
from sound import *
from pygame import mixer

global paused
paused = False


def save_file_warning():
    win = tk.Toplevel()
    win.title('WARNING')
    win.geometry('250x60')
    label = tk.Label(win, justify='center', text='Please save a file!', fg='red')
    label.pack()
    btn = tk.Button(win, text='OK', command=lambda: win.destroy())
    btn.pack()


def choose_file_warning():
    win = tk.Toplevel()
    win.title('WARNING')
    win.geometry('250x60')
    label = tk.Label(win, justify='center', text='Please choose a file!', fg='red')
    label.pack()
    btn = tk.Button(win, text='OK', command=lambda: win.destroy())
    btn.pack()


def warning():
    win = tk.Toplevel()
    win.title('WARNING')
    win.geometry('250x60')
    label = tk.Label(win, justify='center', text='Please write a right value!', fg='red')
    label.pack()
    btn = tk.Button(win, text='OK', command=lambda: win.destroy())
    btn.pack()


def update():
    var.set(song.history_stack)


def get_save():
    try:
        song.save()
    except FileNotFoundError:
        save_file_warning()


def get_reverse():
    song.reverse_sound()
    update()


def get_undo():
    song.undo()
    update()


def get_redo():
    song.redo()
    update()


def get_overlay():
    try:
        song.overlay()
        update()
    except FileNotFoundError:
        choose_file_warning()


def get_merge():
    try:
        song.merge()
        update()
    except FileNotFoundError:
        choose_file_warning()


def get_repeat():
    value = repeat_entry.get()
    try:
        value = int(value)
    except ValueError:
        value = None
    if value is not None and value >= 1:
        times = value
        song.repeat_sound(times)
        update()
    else:
        warning()


def get_fade_out():
    value = fade_out_entry.get()
    try:
        value = float(value)
    except ValueError:
        value = None
    if value is not None and value > 0:
        song.fade_out(value)
        update()
    else:
        warning()


def get_fade_in():
    value = fade_in_entry.get()
    try:
        value = float(value)
    except ValueError:
        value = None
    if value is not None and value > 0:
        song.fade_in(value)
        update()
    else:
        warning()


def get_slice():
    value1 = first_slice_entry.get()
    try:
        value1 = float(value1)
    except ValueError:
        value1 = None
    value2 = second_slice_entry.get()
    try:
        value2 = float(value2)
    except ValueError:
        value2 = None
    if value1 is not None and value2 is not None and value1 > 0 and value2 > 0:
        begin = float(value1)
        end = float(value2)
        song.slice(begin, end)
        update()
    else:
        warning()


def get_volume():
    value = volume_entry.get()
    try:
        value = float(value)
    except ValueError:
        value = None
    if value is not None and value > 0:
        vol_arg = float(value)
        song.volume_change(vol_arg)
        update()
    else:
        warning()


def get_speed():
    value = speed_entry.get()
    try:
        value = float(value)
    except ValueError:
        value = None
    if value is not None and value > 0:
        speed_arg = float(value)
        song.speed_change(speed_arg)
        update()
    else:
        warning()


def open_sound():
    try:
        path = filedialog.askopenfilename(initialdir="/home/", title="What file do you want to import?",
                                              filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
        track = AudioSegment.from_mp3(path)
        song.filePath = path
        song.track = track
        song.stack = []
        song.queue = []
        song.history_stack = []
        song.history_queue = []
        song.overlayTrack = None
        name = song.filePath.split('/')[-1]
        song.history_stack.append(f'Open {name}')
        play_btn['state'] = 'normal'
        pause_btn['state'] = 'normal'
        stop_btn['state'] = 'normal'
        undo_btn['state'] = 'normal'
        redo_btn['state'] = 'normal'
        speed_btn['state'] = 'normal'
        speed_entry['state'] = 'normal'
        reverse_btn['state'] = 'normal'
        overlay_btn['state'] = 'normal'
        merge_btn['state'] = 'normal'
        volume_btn['state'] = 'normal'
        volume_entry['state'] = 'normal'
        slice_btn['state'] = 'normal'
        first_slice_entry['state'] = 'normal'
        second_slice_entry['state'] = 'normal'
        fade_in_btn['state'] = 'normal'
        fade_in_entry['state'] = 'normal'
        fade_out_btn['state'] = 'normal'
        fade_out_entry['state'] = 'normal'
        repeat_btn['state'] = 'normal'
        repeat_entry['state'] = 'normal'
        save_btn['state'] = 'normal'
        update()
    except FileNotFoundError:
        choose_file_warning()


def play():
    song.track.export("song.mp3", format="mp3")
    mixer.music.load("song.mp3")
    mixer.music.play(loops=0)


def stop():
    mixer.music.stop()


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True


if __name__ == "__main__":
    root = tk.Tk()
    mixer.init()
    root.title('Audio Editor')
    root.geometry('700x400')
    root.resizable(False, False)
    #root.config(bg='grey')

    song = Sound()

    play_img = tk.PhotoImage(file='1.png')
    pause_img = tk.PhotoImage(file='2.png')
    stop_img = tk.PhotoImage(file='3.png')

    play_btn = tk.Button(root, image=play_img, borderwidth=0, command=lambda: play(), state='disabled')
    pause_btn = tk.Button(root, image=pause_img, borderwidth=0, command=lambda: pause(paused), state='disabled')
    stop_btn = tk.Button(root, image=stop_img, borderwidth=0, command=lambda: stop(), state='disabled')

    play_btn.place(x=400, y=300)
    pause_btn.place(x=460, y=300)
    stop_btn.place(x=520, y=300)

    open_btn = tk.Button(root, borderwidth=0, text='Open', command=lambda: open_sound(), width=4)
    open_btn.place(x=40, y=40)

    undo_btn = tk.Button(root, borderwidth=0, text='Undo', command=lambda: get_undo(), width=4, state='disabled')
    undo_btn.place(x=40, y=70)

    redo_btn = tk.Button(root, borderwidth=0, text='Redo', command=lambda: get_redo(), width=4, state='disabled')
    redo_btn.place(x=40, y=100)

    speed_btn = tk.Button(root, borderwidth=0, text='Change\nspeed', command=lambda: get_speed(), width=4,
                          state='disabled')
    speed_btn.place(x=40, y=130)

    speed_entry = tk.Entry(root, width=6, state='disabled')
    speed_entry.place(x=40, y=176)

    reverse_btn = tk.Button(root, borderwidth=0, text='Reverse', command=lambda: get_reverse(), width=4,
                            state='disabled')
    reverse_btn.place(x=40, y=210)

    overlay_btn = tk.Button(root, borderwidth=0, text='Overlay', command=lambda: get_overlay(), width=4,
                            state='disabled')
    overlay_btn.place(x=40, y=240)

    merge_btn = tk.Button(root, borderwidth=0, text='Merge', command=lambda: get_merge(), width=4, state='disabled')
    merge_btn.place(x=40, y=270)

    volume_btn = tk.Button(root, borderwidth=0, text='Change\nvolume', command=lambda: get_volume(), width=4,
                           state='disabled')
    volume_btn.place(x=40, y=300)

    volume_entry = tk.Entry(root, width=6, state='disabled')
    volume_entry.place(x=40, y=346)

    slice_btn = tk.Button(root, borderwidth=0, text='Slice', command=lambda: get_slice(), width=4, state='disabled')
    slice_btn.place(x=120, y=40)

    first_slice_entry = tk.Entry(root, width=6, state='disabled')
    first_slice_entry.place(x=120, y=70)

    second_slice_entry = tk.Entry(root, width=6, state='disabled')
    second_slice_entry.place(x=180, y=70)

    fade_in_btn = tk.Button(root, borderwidth=0, text='Fade in', command=lambda: get_fade_in(), width=4,
                            state='disabled')
    fade_in_btn.place(x=120, y=100)

    fade_in_entry = tk.Entry(root, width=6, state='disabled')
    fade_in_entry.place(x=120, y=128)

    fade_out_btn = tk.Button(root, borderwidth=0, text='Fade out', command=lambda: get_fade_out(), width=4,
                             state='disabled')
    fade_out_btn.place(x=120, y=160)

    fade_out_entry = tk.Entry(root, width=6, state='disabled')
    fade_out_entry.place(x=120, y=188)

    repeat_btn = tk.Button(root, borderwidth=0, text='Repeat', command=lambda: get_repeat(), width=4, state='disabled')
    repeat_btn.place(x=120, y=220)

    repeat_entry = tk.Entry(root, width=6, state='disabled')
    repeat_entry.place(x=120, y=248)

    save_btn = tk.Button(root, borderwidth=0, text='Save', command=lambda: get_save(), width=4, state='disabled')
    save_btn.place(x=120, y=280)

    var = tk.StringVar(value=song.history_stack)
    listbox = tk.Listbox(listvariable=var, width=30)
    listbox.place(x=350, y=100)

    scrollbar = tk.Scrollbar(orient="vertical", command=listbox.yview)
    scrollbar.place(x=605, y=105)

    root.mainloop()
