# Desert Dawn / menu music

The user supplied Desert Dawn.mp3 and assigned it to the menu. The unchanged
source is retained under artifacts/audio/suno/menu. Source duration is 189.73 s,
48 kHz stereo. Embedded title is Desert Dawn; artist is masoud.vafaei; the
comment identifies Suno creation. No service generation was performed here.

The runtime Vorbis asset retains the full composition, reduces gain by 1 dB and
adds 1 s / 3 s opening / closing fades to soften the repeat boundary. It repeats
in the main menu and uses the Music volume setting. This is a faded repeat, not
a beat-matched seamless loop. It pauses during video playback, stops on chapter
entry and resumes on return to the menu. Chapter music is still the existing
development score until the user supplies the remaining tracks.

The intro regression checks the selected clip name, duration, looping playback,
no overlap with video and playback resumption. Automated playback verification
does not constitute a human listening assessment.

Final validation: 0.4.3-dev built successfully; all four route, camp, spine and
intro regressions passed. The captured menu was inspected for text/layout.
The build setup no longer overwrites ProjectSettings.bundleVersion with an
older hard-coded value.

The build also includes in-progress language work: Persian/English text and
voice selectors, Persian menu and Chapter 1/2 catalog, display shaping and
language-specific dialogue asset lookup. Later chapter translations and recorded
dialogue are incomplete; no full bilingual-release claim is made.
