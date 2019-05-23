# wikipedia name entity annotation dataset

## requirements
```
pip install wget
pip install pandas
```
## usage
- make sure data_loader.py is located in the working directory
- once the data_loader.py is available in the working directory
- Please refer to the load_ex.py for the usage

```
from data_loader import WikiNameEntities, hashabledict

dataset = WikiNameEntities()

for annotation in dataset:
    print(annotation)
```
