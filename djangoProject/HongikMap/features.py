class Recommend:
    def __init__(self):
        self.recommends = dict()
        self.keywords = dict()

        with open("HongikMap/static/data/keywords.txt", "r", encoding='UTF8') as kw:
            for line in kw.readlines():
                entity, value = line.split(":")
                self.recommends[entity] = list(value.split(","))

        with open('HongikMap/static/data/recommends.txt', "r", encoding='UTF8') as rec:
            for line in rec.readlines():
                entity, value = line.split(":")
                self.keywords[entity] = value

        #print(self.recommends, self.keywords)

    def find(self, keyword: str):

        ret = []
        kw_length = len(keyword)
        if kw_length <= 0:
            return []

        if keyword[0].encode().isalpha():  # 첫 글자가 영어: I101
            ret = self.find_by_parsing(keyword)
        elif keyword.isdecimal():  # 전체가 숫자: 101
            ret = self.find_in_recommend(keyword)
        else:  # 한글 입력: 카나
            ret = self.find_in_recommend(keyword)
        return ret

    def find_by_parsing(self, keyword):

        return []

    def find_in_recommend(self, keyword):
        ret = []
        for k, v in self.recommends.items():
            if any([keyword in x for x in v]):
                ret.append(self.keywords[k].rstrip())

        if not ret:
            if keyword[0].isalpha() and keyword[0] != "Z":
                pass

        return ret


class Graph:
    def __init__(self, elevator:bool = True):
        with open("HongikMap/static/data/data.txt", "r") as f:
            for line in f.readlines():
                print(line)
