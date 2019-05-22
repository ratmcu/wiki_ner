# from data_loader import WikiNameEntities, hashabledict
from data_loader import WikiNameEntities, hashabledict
# from data_loader import hashabledict

dataset = WikiNameEntities()

for annotation in dataset:
    print(annotation)
