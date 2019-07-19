import japscales
import seasonclass
import vowels
import music21
import random
import copy

vowel_order = ['o', 'a', 'u', 'e', 'i']
season_order = ['winter', 'autumn', 'spring', 'summer']
tonalities = ['B3', 'F3', 'C3', 'G3', 'D3']
consonant_order = ['h', 'w', 'v', 's', 'z', 'f', 'l', 'm', 'n', 'x', 'j', 'b', 'p', 'd', 'g', 'r', 'c', 'k', 'q', 't']

def generateVerseMelody(verse, root) -> music21.stream.Stream:
    if isinstance(root, str): root = music21.pitch.Pitch(root)
    
    classifier = seasonclass.SeasonClassifier()
    classifier.init_words()
    classifier.init_classifier()
    season = classifier.classify_verse(verse)
    
    scale = japscales.getJapScale(root, season_order.index(season))
    
    vowel_list = vowels.decomposeToVowels(verse)[:8]
    pitches = scale.pitches
    melody = music21.stream.Stream()
    octave = 4 if vowel_list[0] == 'o' or vowel_list[0] == 'u' else 5
    last_vowel = ''
    for vowel in vowel_list:
        note = music21.note.Note(pitches[vowel_order.index(vowel) +  + random.randint(-1, 1)])
        if last_vowel == 'i' and vowel == 'o': octave -= 1
        if last_vowel == 'o' and vowel == 'i': octave += 1
        octave = max(min(octave, 5), 4)
        last_vowel = vowel
        note.pitch.octave = octave
        if random.randint(0, 3) == 0:
            interval = random.randint(-2, 2)
            if interval != 0: pitch = scale.next(note.pitch, interval)
            else: pitch = copy.deepcopy(note.pitch)
            extra_note = music21.note.Note(pitch)
            note.duration.quarterLength = 0.5
            extra_note.duration.quarterLength = 0.5
            if random.randint(0, 1) == 0:
                melody.append(note)
                melody.append(extra_note)
                note = extra_note
            else:
                melody.append(extra_note)
                melody.append(note)
        else: melody.append(note)
    note.duration.quarterLength = 8 - melody.duration.quarterLength + note.duration.quarterLength
    return melody

def generatePoemMelody(verses) -> music21.stream.Part:
    vowel_list = []
    for verse in verses:
        vowel_list += vowels.decomposeToVowels(verse)
    tonality = 'C3'
    count = 0
    for vowel in vowel_order:
        if vowel_list.count(vowel) > count:
            tonality = tonalities[vowel_order.index(vowel)]
            count = vowel_list.count(vowel)
    
    melody = music21.stream.Part()
    
    speed_val = 0
    for verse in verses:
        for l in verse:
            if l in consonant_order:
                speed_val += consonant_order.index(l)
    speed_val /= len(verses[0]) + len(verses[1]) + len(verses[2])
    tempo = 20 + 15 * speed_val
    mark = music21.tempo.MetronomeMark(None, tempo, music21.duration.Duration('quarter'))
    melody.append(mark)     
    
    for i in range(random.randint(3, 5)):
        for verse in verses:
            melody.append(generateVerseMelody(verse, tonality))
    return melody.flat.makeNotation()