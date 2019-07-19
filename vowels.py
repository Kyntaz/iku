import re

def decomposeToVowels(line):
    vowels = re.findall(r'[aeiouy]+', line.lower())
    vowels = [v[-1] for v in vowels]
    return [v if v != 'y' else 'i' for v in vowels]