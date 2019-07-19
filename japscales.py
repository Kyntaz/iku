import music21

def getJapTetrachord(root, ty):
    if isinstance(root, str): root = music21.pitch.Pitch(root)
    p1 = root.transpose(['m2', 'M2', 'm3', 'M3'][ty])
    p2 = root.transpose('P4')
    return [root, p1, p2]

def getJapScale(root, ty) -> music21.scale.ConcreteScale:
    if isinstance(root, str): root = music21.pitch.Pitch(root)
    if isinstance(ty, int): ty = (ty, ty)
    c1 = getJapTetrachord(root, ty[0])
    r2 = root.transpose('P5')
    c2 = getJapTetrachord(r2, ty[1])
    return music21.scale.ConcreteScale(pitches=c1 + c2)