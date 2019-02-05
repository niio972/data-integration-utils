# Install Replace Text in Files

## Install from Git
Clone the directory :

```git clone https://github.com/niio972/data-integration-utils.git```

Go to the directory:
 - ```{path}/data-integration-utils/PythonScripts/replaceTextinfiles```C

## Install conda
Get the latest version of miniconda at [miniconda](https://www.anaconda.com/download/#linux)

**Go to the directory that you have download. Run in a shell**
```bash Miniconda*-Linux-x86_64.sh```

### Set environment

```. env-setup-conda```

### Command to activate environment
```source activate replacetext```

## Run script

**usage** : ```python replaceStrings.py [-h] -i I -o O -c C [C ...] [-p] [-v]```

**optional arguments**:
  ```bash
  optional arguments:
  -h, --help            show this help message and exit
  -i I                  The path of the file or the directory which contains
                        the files to Format
  -o O                  The path of the directory which will contains the
                        formatted files
  -c C [C ...]          The path of yaml vocabulary file(s)
  -p, --nostrictpattern
                        if pattern is use to replace complex string, true by
                        default
  -v, --verbose         increase output verbosity
  ```

### Example :
**Exemple of text file :**
```
object, type, type_sol
plantOne, plant, clay
```
**Exemple of vocabulary file** :

Transform **type_sol** and  **type_sol3** in __**SoilType**__.

```yaml
soilType:
  - type_sol # soil type of plant
  #- type_sol3
```
**Exemple of result :**
```
object, type, soilType
plantOne, plant, clay
```
**Command line examples** : 

```python replaceStrings.py -i ./transf -o ./output -c ./vocabulary1.yml ```

```python replaceStrings.py -i ./file.csv -o ./output -c ./vocabulary1.yml ```

```python replaceStrings.py -i ./transf -o ./output -c ./vocabulary1.yml ./vocabulary2.yml```
