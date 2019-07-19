import music21
import copy
import random

def generateChord(m: music21.stream.Measure, pc: music21.chord.Chord) -> music21.chord.Chord:
    pps = m.pitches + list(pc.pitches)
    ps = []
    for p in pps:
        p.octave = 3
        p2 = p.transpose('P4')
        p3 = p.transpose('P5')
        p2.octave = 3
        p3.octave = 3
        ps += [copy.deepcopy(p), p2, p3]
    cho = []
    for i in range(3):
        cho += [random.choice(ps)]
        ps = list(filter(lambda x: not x in cho, ps))
    for i in range(random.randint(5,10)):
        for p in cho:
            stabilizePitch(p, cho)
    c = music21.chord.Chord(cho)
    c.duration.quarterLength = m.duration.quarterLength
    return c

def stabilizePitch(p, ps):
    for op in ps:
        if 0 < abs(music21.interval.Interval(p, op).cents) <= 200:
            p.octave += random.choice([1, -1])

def generateComping(poem: music21.stream.Part) -> music21.stream.Part:
    comp = music21.stream.Part()
    c = music21.chord.Chord()
    for m in poem.makeMeasures():
        c = generateChord(m, c)
        comp.append(c)
    return comp