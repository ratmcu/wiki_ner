# from data_loader import WikiNameEntities
from data_loader import WikiNameEntities, hashabledict
# from data_loader import hashabledict
class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
if __name__ == '__main__':
    dataset = WikiNameEntities()
    for annotation in dataset:
        print(annotation)
