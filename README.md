# wikipedia name entity annotaion dataset


## make sure data_loader.py is located in the working directory
## Please refer to the load_ex.py for the usage

```
from data_loader import WikiNameEntities, hashabledict

dataset = WikiNameEntities()

for annotation in dataset:
    print(annotation)
```
