import array
import time

import jim.audio.note
import RPi.GPIO as GPIO

from threading import Thread

# Define the song
B3 = 246.94
C3 = 261.63
D3 = 293.66
Ds3 = 311.13
E3 = 329.63
F3 = 349.23
Fs3 = 369.99
G3 = 392.00
A4 = 440.00
B4 = 493.88
C4 = 523.25
D4 = 587.33

SONG_WHITE_CHRISTMAS = [ E3, F3, E3, Ds3, E3, F3, Fs3, G3, \
                         # I'm dreaming of a white Christmas
                         A4, B4, C4, D4, C4, B4, A4, G3, \
                         # Just like the ones I used to know
                         C3, D3, E3, E3, E3, G3, F3, \
                         # Where the treetops glisten and
                         C3, C3, C3, G3, F3, E3, \
                         # children listen to hear
                         F3, E3, D3, C3, D3, \
                         #sleigh bells in the snow.
                         \
                         E3, F3, E3, Ds3, E3, F3, Fs3, G3, \
                         # I'm dreaming of a white Christmas
                         A4, B4, C4, D4, C4, B4, A4, G3, \
                         # With every Christmas card I write.
                         C3, D3, E3, E3, E3, A4, G3, C4, \
                         # May your days be merry and bright
                         C3, D3, E3, E3, A4, G3, B3, \
                         # And may all your Christmases
                         D3, C3
                         # be white.
                       ]

# Init the GPIO ports
OUT_LIGHT_GREEN = 12
OUT_LIGHT_RED = 16
IN_BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUT_LIGHT_RED, GPIO.OUT)
GPIO.setup(OUT_LIGHT_GREEN, GPIO.OUT)

# Global variables
bProgramStopping = False
currentNoteIndex = 0
currentNote = None

class LightsController(Thread):
    def __init__(self, timeLightDelayInMS):
        ''' Constructor. ''' 
        Thread.__init__(self)
        self.timeLightDelayInMS = timeLightDelayInMS
        self.CurrentLight = OUT_LIGHT_RED
 
    def run(self):
        print('"%s" starting.' % self.getName())
        
        while (bProgramStopping == False):
            # Turn off the old current light
            GPIO.output(self.CurrentLight, 0)
            
            # Switch lights
            if (self.CurrentLight == OUT_LIGHT_RED):
                self.CurrentLight = OUT_LIGHT_GREEN
            elif (self.CurrentLight == OUT_LIGHT_GREEN):
                self.CurrentLight = OUT_LIGHT_RED
                
            # Turn on the new current light
            GPIO.output(self.CurrentLight, 1)
            
            time.sleep(self.timeLightDelayInMS / 1000)

        print('"%s" stopping.' % self.getName())

# Button callback function
def buttonPressed(channel):
    global currentNoteIndex
    global currentNote
    
    if (currentNote is not None):
        currentNote.stop()
        
    if (GPIO.input(IN_BUTTON)):
        print("Button rising")
        if (currentNote is None):
            currentNote = jim.audio.note.Note(SONG_WHITE_CHRISTMAS[currentNoteIndex])
            currentNoteIndex = currentNoteIndex + 1
            currentNote.play(-1)
        else:
            currentNote = None
    else:        
        print("Button falling")
        currentNote = None

# Main Function
if __name__ == '__main__':
    '''
    for n in SONG_WHITE_CHRISTMAS:
        print("Freq = " + str(n))
        note = jim.audio.note.Note(n)
        note.play(loops=-1)
        time.sleep(1)
        note.stop()
    '''
    # Add the button callback
    GPIO.add_event_detect(IN_BUTTON, GPIO.BOTH, callback=buttonPressed, bouncetime=50)
    lightsThread = LightsController(1000)
    lightsThread.setName('Lights Controller')
    lightsThread.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Ctrl-C pressed.")
    
    except:
        print("Other exception occurred.")
    
    finally:
        bProgramStopping = True
        lightsThread.join()
        GPIO.cleanup()