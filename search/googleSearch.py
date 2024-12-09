from googlesearch import search
import random

random.seed(42)

class Google:
    def __init__(self, search_term = '', count = 10):
        self.search_term = search_term
        self.count = count

    def search(self, search_term = '', count = 10):
        try:
            res = list(search(search_term, num_results=count))
            random.shuffle(res)
            return res
        except Exception as e:
            print(e)
        