

from data_loader import WikiNameEntities
# from data_loader import WikiNameEntities, hashabledict
# from data_loader import hashabledict
class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def coloring_sentences(annotation):
    part_before = '\033[1;37;40m{0}'.format(annotation[0][0:annotation[1][1][0]])
    part_after = '\033[1;37;40m{0}'.format(annotation[0][annotation[1][1][1]:])
    coloring = '\033[1;32;40m{0}'.format(annotation[0][annotation[1][1][0]:annotation[1][1][1]])
    category = '\033[1;31;47m{0}\033[1;37;40m\n'.format(annotation[1][2])
    # print(part_before)
    # print(coloring)
    # print(part_after)
    print(part_before + coloring + part_after + category)

import math

if __name__ == '__main__':
    dataset = WikiNameEntities()
    i = 0
    for annotation in dataset:
        # print(annotation[0])
        # if(not isinstance(annotation[0], str) and math.isnan(annotation[0])):
            # print(annotation)
        # i = i + 1
        # print(annotation[0][0:annotation[1][1][0]], annotation[1])
        # print(coloring_sentences(annotation))
        coloring_sentences(annotation)
    # print(i)
# print("\033[1;32;40m Bright Green  \n")

