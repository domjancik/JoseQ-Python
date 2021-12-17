pip install mido python-rtmidi pyserial
https://stackoverflow.com/questions/17553543/pyserial-non-blocking-read-loop


# Protocol
## Overview
Following needs to be communicated:

### Arduino > RPi
- Start (git history player - see animation of file development) Down/Up
- Stop Down/Up
- Change Tempo
- Steps State Index, Down/Up

(All buttons can be treated the same with Index, State fields... or maybe not, since)(maybe I should focus MAINLY on readability - this could be also YES YES YES be displayed on the screen permanently - a console view from the pi - did I get an update on the order? music*CLAUDE DEBUSSY: CLAIR DE LUNE -> "
Fri, 17 Dec, 11:12 (12 hours ago)
to me" "Dobrý den,

Vaše zásilka číslo 251179905 z internetového obchodu rpishop.cz je pro Vás připravena" YES "Otevírací doba:
Po–Ne 08:00–19:00
24.12.2021 08:00–12:00
25.12.2021–26.12.2021 zavřeno
01.01.2022 zavřeno" YES (low (high?) level sidenotes kept in secure location)) 

So aim for readability -> log can be displayed permanently on the attached screen.
Together with the log, the screen can also host debugging and troubleshooting tools.

Message examples:
#### Button update
```
STEP-BUTTON 4(Bucket):5 ON
PLAY-BUTTON OFF
STOP-BUTTON ON
```

#### All update (ASCII Art)
```
v ^ 134
^vv^ v^^^ v^v^ ^^^^
...
vvvv v^^^ v^v^ vvvv 
```

#### All update (key:value)
```
PLAY:ON STOP:OFF TEMPO:134
ROW1:0110 1000 1010 0000
...
ROW6:1111 1000 1010 1111 
```

### RPi > Arduino
- Current Step

## Message Format
Byte based messages are used for compactness (reducing delay, hopefully nullyfing need to deal with async/multithreading in python which I have little experience with and which always brings fun quirks with it).

This is mainly due to the largest message of `Steps State` which contains nearly a 100 boolean values (6*16=96) representing 6 stepper tracks of 16 steps each. (Sidenote: If a button needs to be disconnected or is misbehaving, it should be possible to mask that button in the consuming application, low priority)

If we used a textual string representation, composed of 0s and 1s
we would always need 96 bytes per one status update. Now, there are also other methods how to cut down on this waste. Biggest savings could be achieved by sending only changes on a single switch. This would give more opportunities for things to go out of sync. However, if used in combination with the full state update, it might actually help to avoid the need to implement (on both sides) a binary protocol and retain the readability of a string based approach.

Let's remind ourselves th(e cat is destroying my sweater but it seems fin)at the goal is to get it just working somehow again and if I can manage to set up remote access (even if it means having a contact at the location), I can really start as simple as possible. Both the micro and RPi can then be readily reprogrammed for improvements, repairs and unforeseen experiences. This feels like it could bring more value than an optimized binary protocol that shaves off a couple micros when we actually have [1s/BPM(60-150)]6.6_ms to work with between each step. In which we're able to --- scratch that (this is way too little, compare to 16ms which we get for a 60 frames per second animation)--- It's beats per minute so 60s/BPM, getting us to the minimum of X with 150BPM (can AI fill the X which is , lemme calc it, but I'd say 396ms or so with 6.6_*60, let's see...>_ says straight up 400. (Markdown+inlineevaluator half/half with preview)
(double taps/holds can be used for special functions -> both on and off messages needed)

So we have 400ms in which to deal with our communication between (bein) the RPi, Arduino and MIDI Device (most likely dadamachines smth, lemme check, chrome is stuck, lets see in vivaldi, or can I remember? Kontakt? No... dadamachines machine? no... dadamachines rig? nah... let's see... AUTOMAT!) (most likely the dadamachines Automat, we have a spare one and we all believe it's built better and more resilient than the current solution composed primarily of breadboard, jumper cables and hot glue)

So 400ms it is, nearly half a second, the time it takes us to react on the road (maaaybe, let me fact check that :D, yahoo driver reaction time (why yahoo, cuz vivaldi), "This article should not be interpreted to mean that human perception-reaction time is 1.5 seconds. There is no such thing as the human perception-reaction time. Time to respond varies greatly across different tasks and even within the same task under different conditions. It can range from .15 second to many seconds. It is also highly variable. In many cases, the very concept of perception-reaction time simply doesn't apply2.". A baseline driving reaction threshold seems to float somewhere around one and a half seconds - this is not very fast)

So we have about a third of what's considered an adequate human perception to reaction time. This may not sound like a lot but for a today's microcomputer, it's basically eons. Flipping a couple of bytes here and there should take only a mere fraction.

Yes, there is also the issue of timing the note triggers - the drum hits - exactly right, to stay unaffected by the background processing required to bring the experience to life. Is it really a requirement (fastest development is no development - thinking the problem through and writing a single paragraph may save hours) though? Are the mechanics precise enough that this optimization would make a difference? Is a little swing (experiment with artificial swing) a bad thing? And the swing will be affected by user action - how much they're interacting with the device - maybe interesting slowdowns could occur and if not... we'll make them occur.

Anyways, I think that the decision here is to:
- Use strings for communication (easier readability in Serial monitors, less wasted effort, easier to mock)
- Send single control changes (to reduce load) together with occassional (idea: reveal format - able to assign details levels to parts of text (names: sidenot, sidenote, derail, explain, ...)) full state update to avoid state drift (single control changes should be pretty easy to implement with the object/callback based approach used in JoseQ)