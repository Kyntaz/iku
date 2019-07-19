import song
import re

def load_songs(file):
    songs = []
    with open(file, 'r') as f:
        verses = []
        for v in f:
            if v != '\n':
                verses += [v]
            else:
                songs += [verses]
                verses = []
    
    if len(verses) > 0:
        songs += [verses]
    print('Loaded {} haikus.'.format(len(songs)))
    return songs

def generate_ikus(file, n):
    songs = load_songs(file)
    i = 1
    for verses in songs:
        prepared_verse = verses[0].replace(' ', '_')
        name = re.search(r'\w*', prepared_verse).group()
        print('Starting a new iku, {}.'.format(name))
        output = song.curateSong(verses, n)
        output.write('midi', fp = 'output\\' + str(i) + '_' + name + '.mid')
        i += 1
        
if __name__ == '__main__':
    n = eval(input('Curation loops: '))
    generate_ikus('haikus\\haikus.txt', n)