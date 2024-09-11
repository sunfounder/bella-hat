class ``Music``
========================================

**Example**

Initialize

.. code-block:: python

    # Import Music class
    from bella_hat.music import Music

    # Create a new Music object
    music = Music()

Play sound

.. code-block:: python

    # Play a sound
    music.sound_play("file.wav", volume=50)
    # Play a sound in the background
    music.sound_play_threading("file.wav", volume=80)
    # Get sound length
    music.sound_length("file.wav")

Play Music

.. code-block:: python

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

**API**

.. currentmodule:: bella_hat.music

.. autoclass:: Music
    :show-inheritance:
    :special-members: __init__
    :members:
