from Tkinter import *
import echonest.audio as audio

usage = """
Usage: 
    python ui.py <input_filename> <output_filename>

Example:
    python test.py EverythingIs.mp3 EverythingIsOneandTwo.mp3
"""

class Application(Frame):
    def analyze(self):
        print "analyzing %s" % input_filename
        audiofile = audio.LocalAudioFile(input_filename)
        self.segments = audiofile.analysis.segments

        self.timbre_max = 0
        self.timbre_min = 0
        for segment in self.segments:
            if segment.timbre[0] > self.timbre_max:
                self.timbre_max = segment.timbre[0]
            if segment.timbre[0] < self.timbre_min:
                self.timbre_min = segment.timbre[0]

    def render(self):
        collect = audio.AudioQuantumList()
        print "Let's go:"
        current_max = self.timbre_max.get()
        current_min = self.timbre_min.get()
        for segment in self.segments:
            if segment.timbre[0] >= current_min and segment.timbre[0] <= current_max:
                collect.append(segment)
        out = audio.getpieces(audiofile, collect)
        out.encode(output_filename)

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})

        self.analyze = Button(self, text="Analyze", command=self.analyze)
        self.analyze.pack({"side": "left"})

        self.render = Button(self, text="Render", command=self.render)
        self.render.pack({"side": "left"})

        self.timbre_max = Scale(self, from_=100, to=0)
        self.timbre_min = Scale(self, from_=100, to=0)
        self.timbre_max.pack()
        self.timbre_min.pack()  

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

if __name__ == '__main__':
    import sys
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
