class Recommend:
    def __init__(self):
        self.keywords = dict()
        self.recommends = dict()

        with open("static/data/keywords.txt", "r") as kw:
            for line in kw.readlines():
                entity, value = line.split(":")
                self.keywords[entity] = list(value.split(","))

        with open('static/data/recommends.txt', "r") as rec:
            for line in rec.readlines():
                entity, value = line.split(":")
                self.recommends[entity] = value

        print(self.keywords)
        print(self.recommends)

    def find(self, keyword: str):
        ret = []
        for k, v in self.keywords.items():
            if any([keyword in x for x in v]):
                ret.append((k, self.recommends[k]))

        if not ret:
            if keyword[0].isalpha() and keyword[0] != "Z":
                pass

        return ret


class Graph:
    def __init__(self):
        with open("static/data/data.txt", "r") as f:
            for line in f.readlines():
                print(line)
