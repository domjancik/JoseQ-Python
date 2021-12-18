"""
Sequencer deals with
- managing play state
  - playing/not playing
  - tempo
  - current step
- managing step state
- sending MIDI messages at each step update
- sending Step updates to Arduino

^ not happy about the mix of serial and midi responsibilities into the sequencer logic, might consider factoring those out later
"""