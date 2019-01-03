# Install Replace Files

## Install from Git
git clone https://github.com/niio972/data-integration-utils.git
Go to the directory:
 - ```{path}/data-integration-utils/PythonScripts/replaceTextinfiles```
 - 

## Install conda
Get the latest version of miniconda at [miniconda](https://www.anaconda.com/download/#linux)
```bash Miniconda3-latest-Linux-x86_64.sh```

### Set environment

```env-setup-conda```

### Command to activate environment
```source activate replacetext```

## Run script

**usage** : ```replaceStrings.py [-h] -i I -o O -c C [-v]```

**optional arguments**:
  ```
  -h, --help     show this help message and exit
  -i I           The path of the directory which contains the files to Format
  -o O           The path of the directory which will contains the formatted
                 files
  -c C           The path of yml vocabulary file
  -v, --verbose  increase output verbosity
  ```

**Example** : 

```python replaceStrings.py -i ./transf -o ./output -c ./vocabulary.yml```
