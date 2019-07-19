import melody as mel
import chords as cho
import music21
import copy

def generateSong(verses) -> music21.stream.Score:
    score = music21.stream.Score()
    melody = mel.generatePoemMelody(verses)
    chords = cho.generateComping(melody)   
    
    score.append(melody)
    score.append(chords)
    #key = score.analyze('key')
    #melody.insert(0, copy.deepcopy(key))
    #chords.insert(0, copy.deepcopy(key))
    return score.makeNotation()

def curateSong(verses, n) -> music21.stream.Score:
    song = generateSong(verses)
    score = song.analyze('key').correlationCoefficient
    print('Start Curation with score {}.'.format(score))
    for i in range(n):
        pot_song = generateSong(verses)
        pot_score = pot_song.analyze('key').correlationCoefficient
        print('Song {}/{} has score {}.'.format(i+1, n, pot_score))
        if pot_score >= score:
            print('Accepted.')
            song = pot_song
            score = pot_score
    return song