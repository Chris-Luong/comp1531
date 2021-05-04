import operator
import pickle

def most_common():
    data = pickle.load(open("shapecolour.p", "rb"))

    common = {}
    for d in data:
        key = (d['colour'], d['shape'])
        if key not in common:
            common[key] = 0
        common[key] += 1

    colour, shape = max(common.items(), key=operator.itemgetter(1))[0]

    return {
        "Colour": colour,
        "Shape": shape,
    }
