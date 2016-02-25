The preprocessing script listed in this folder focuses on efficiently handling large files.

### Main Scripts
- ```split.py``` Randomly splits lines from a given file into 2 new files, where the proportion to go to the first output file is determined by ```percent``` (optional, default=90%). A random seed can also be specified for reproducibility. This can be useful for spliting a dataset into a random cross-validation (train/test) split.
 ```
python split.py data.csv train test [probability] [random_seed]
```
- ```colstat.py``` Compute column means and standard deviations from data in csv file.
- ```count_lines.py``` Count lines in a file.
- ```del_cols.py``` Delete columns from file specified by their indexes.
- ```sample_lines.py``` Sample lines from input file with probability P, save them to output file.
 ```
sample_lines.py INPUT_FILE OUTPUT_FILE [P]
```
- ```standardise_features.py``` Standardises (shift and scale to zero mean and unit standard deviation) data from csv file.
 ```
python standardise_features.py STATS_FILE INPUT_FILE OUTPUT_FILE [LABEL_INDEX]
```
- ```tsv2csv.py``` Converts a .tsv file to a .csv file.
 ```
python tsv2csv.py INPUT_FILE OUTPUT_FILE
```

### Helper Scripts
- ```f_is_headers``` Automatically define if the [first] line in file contains headers.

Related:
- https://github.com/zygmuntz/phraug2
