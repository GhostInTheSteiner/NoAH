# NoAH

NoAH is a toolset around a script called "PyTextbox" which serves to animate text in in a Visual Novel esque way. As output it will deliver transparent .mov-videos, which can be used in any decent video editor. It mainly supports fading (left-to-right), appending multiple paragraphs and adjusting paragraph fade-in time to a voice track sample as core features while being highly configurable.

fun^10 x int^40 = Ir2 contains an Autohotkey-Script to ease up editing in Kdenlive. It adds a few convenient shortcuts to e.g. easily fade-in or fade-out images.

For an example of what content NoAH allows to generate see this playlist:

https://youtube.com/playlist?list=PLy_Bwyf7LCb5c73MCP0JRgVd2uovEYRoN

## Usage

This script requires a linux based system. Setup the following: 

- A spreadsheet containing the script lines **(./script_resources)**
- A .wav file and a corresponding .cue file indicating the timestamps where spoken lines begin **(./voice_track_resources)**
- A configuration **(./program/configurations)**
- An import to this configuration in *PyTextbox.py* **(./program)**

The spreadsheet allows for three switches to be used (by setting their fields to **"1"**):

- **V:** Voiced, will time a line to match the length of the corresponding audio timestamps defined in the .cue file.

- **A:** Appended, will cause the next line to be appended and preserves the previous line (resulting in a NVL-style presentation).

- **S:** Selected, if set only the selected lines will be generated.

This repo already contains several setups that were used for earlier projects, you can safely use those as examples.

Once the setup is complete, run the following:

`python3 PyTextbox.py`

By default, audio and video files will be generated to the **./voice_tracks** and **./animated_text** directories respectively.

The **customOutputFolderVideoClips** and **customOutputFolderVoiceTracks** directories will only be used if the **-c** switch is used:

`python3 PyTextbox.py -c`

In that case, any previously existing files will be overwritten. Therefore those folders should be where your video editor pulls the audio and video files from.

*Even though GitHub is intended for source control I'll just abuse it right there as storage for a dummy setup, blame me if you want to ('_v')*
