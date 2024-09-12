# class `Music`

**Example**

Initialize

```python
# Import Music class
from bella_hat.music import Music

# Create a new Music object
music = Music()
```

Play sound

```python
# Play a sound
music.sound_play("file.wav", volume=50)
# Play a sound in the background
music.sound_play_threading("file.wav", volume=80)
# Get sound length
music.sound_length("file.wav")
```

Play Music

```python
# Play music
music.music_play("file.mp3")
# Play music in loop
music.music_play("file.mp3", loop=0)
# Play music in 3 times
music.music_play("file.mp3", loop=3)
# Play music in starts from 2 second
music.music_play("file.mp3", start=2)
# Set music volume
music.music_set_volume(50)
# Stop music
music.music_stop()
# Pause music
music.music_pause()
# Resume music
music.music_resume()
```

**API**

### *class* bella_hat.music.Music

Bases: [`_Basic_class`](api_basic_class.md#bella_hat.basic._Basic_class)

Play music, sound affect and note control

#### NOTE_BASE_FREQ *= 440*

Base note frequency for calculation (A4)

#### NOTE_BASE_INDEX *= 69*

Base note index for calculation (A4) MIDI compatible

#### NOTES *= [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'A0', 'A#0', 'B0', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7', 'C8']*

Notes name, MIDI compatible

#### \_\_init_\_()

Initialize music

#### time_signature(top: int = None, bottom: int = None)

Set/get time signature

* **Parameters:**
  * **top** (*int*) – top number of time signature
  * **bottom** (*int*) – bottom number of time signature
* **Returns:**
  time signature
* **Return type:**
  tuple

#### key_signature(key: int = None)

Set/get key signature

* **Parameters:**
  **key** (*int/str*) – key signature use KEY_XX_MAJOR or String “#”, “##”, or “bbb”, “bbbb”
* **Returns:**
  key signature
* **Return type:**
  int

#### tempo(tempo=None, note_value=0.25)

Set/get tempo beat per minute(bpm)

* **Parameters:**
  * **tempo** (*float*) – tempo
  * **note_value** – note value(1, 1/2, Music.HALF_NOTE, etc)
* **Returns:**
  tempo
* **Return type:**
  int

#### beat(beat)

Calculate beat delay in seconds from tempo

* **Parameters:**
  **beat** (*float*) – beat index
* **Returns:**
  beat delay
* **Return type:**
  float

#### note(note, natural=False)

Get frequency of a note

* **Parameters:**
  * **note_name** (*string*) – note name(See NOTES)
  * **natural** (*bool*) – if natural note
* **Returns:**
  frequency of note
* **Return type:**
  float

#### sound_play(filename, volume=None)

Play sound effect file

* **Parameters:**
  **filename** (*str*) – sound effect file name

#### sound_play_threading(filename, volume=None)

Play sound effect in thread(in the background)

* **Parameters:**
  * **filename** (*str*) – sound effect file name
  * **volume** (*int*) – volume 0-100, leave empty will not change volume

#### music_play(filename, loops=1, start=0.0, volume=None)

Play music file

* **Parameters:**
  * **filename** (*str*) – sound file name
  * **loops** (*int*) – number of loops, 0:loop forever, 1:play once, 2:play twice, …
  * **start** (*float*) – start time in seconds
  * **volume** (*int*) – volume 0-100, leave empty will not change volume

#### music_set_volume(value)

Set music volume

* **Parameters:**
  **value** (*int*) – volume 0-100

#### music_stop()

Stop music

#### music_pause()

Pause music

#### music_resume()

Resume music

#### music_unpause()

Unpause music(resume music)

#### sound_length(filename)

Get sound effect length in seconds

* **Parameters:**
  **filename** (*str*) – sound effect file name
* **Returns:**
  length in seconds
* **Return type:**
  float

#### get_tone_data(freq: float, duration: float)

Get tone data for playing

* **Parameters:**
  * **freq** (*float*) – frequency
  * **duration** (*float*) – duration in seconds
* **Returns:**
  tone data
* **Return type:**
  list

#### play_tone_for(freq, duration)

Play tone for duration seconds

* **Parameters:**
  * **freq** (*float*) – frequency, you can use NOTES to get frequency
  * **duration** (*float*) – duration in seconds
