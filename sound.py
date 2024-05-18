from pydub import AudioSegment
from tkinter import filedialog


class Sound:
    def __init__(self):
        self.filePath = None
        self.track = None
        self.queue = []
        self.stack = []
        self.history_stack = []
        self.history_queue = []
        self.overlayTrack = None

    def speed_change(self, speed=1.0):
        sound_with_altered_frame_rate = self.track._spawn(self.track.raw_data, overrides={
            "frame_rate": int(self.track.frame_rate * speed)
        })
        self.stack.append(self.track)
        self.history_stack.append(f'Speed changed to {speed}x')
        self.track = sound_with_altered_frame_rate.set_frame_rate(self.track.frame_rate)

    def save(self):
        save_path = filedialog.asksaveasfilename(initialdir = "/home/", title=
        "Where do you want to save the modified file?", filetypes = (("mp3 files", "*.mp3"), ("all files", "*.*")))
        self.track.export(save_path, bitrate="320k", format="mp3")

    def volume_change(self, vol):
        self.stack.append(self.track)
        self.history_stack.append(f'Volume changed to {vol} db')
        self.track = self.track + vol

    def slice(self, begin, end):
        ms1 = begin * 1000
        ms2 = end * 1000
        self.stack.append(self.track)
        self.history_stack.append(f'Sliced from {begin} to {end}')
        self.track = self.track[ms1:ms2]

    def reverse_sound(self):
        self.stack.append(self.track)
        self.history_stack.append('Reversed')
        self.track = self.track.reverse()

    def repeat_sound(self, count):
        self.stack.append(self.track)
        self.history_stack.append(f'Repeat {count} times')
        self.track = self.track * 2

    def merge(self):
        path = filedialog.askopenfilename(initialdir="/home/", title="What file do you want to import?",
                                                   filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
        track = AudioSegment.from_mp3(path)
        s = str(path.split('/')[-1])
        self.stack.append(self.track)
        self.history_stack.append(f'Merge with {s}')
        self.track = self.track + track

    def fade_in(self, seconds):
        ms = int(seconds * 1000)
        self.stack.append(self.track)
        self.history_stack.append(f'Fade in {seconds}s')
        self.track = self.track.fade_in(ms)

    def fade_out(self, seconds):
        ms = int(seconds * 1000)
        self.stack.append(self.track)
        self.history_stack.append(f'Fade out {seconds}s')
        self.track = self.track.fade_out(ms)

    def overlay(self):
        self.stack.append(self.track)
        self.filePath = filedialog.askopenfilename(initialdir="/home/", title="What file do you want to import?", filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
        self.overlayTrack = AudioSegment.from_mp3(self.filePath)
        name = self.filePath.split('/')[-1]
        self.history_stack.append(f'Overlay by {name}')
        self.track = self.track.overlay(self.overlayTrack)

    def undo(self):
        if len(self.stack) != 0:
            self.queue.insert(0, self.track)
            self.track = self.stack.pop()
            self.history_queue.insert(0, self.history_stack.pop())

    def redo(self):
        if len(self.queue) != 0:
            self.stack.append(self.track)
            self.track = self.queue[0]
            self.queue.pop(0)
            self.history_stack.append(self.history_queue[0])
            self.history_queue.pop(0)