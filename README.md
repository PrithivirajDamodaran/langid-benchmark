# langid-benchmark
A benchmark of off-the-shelf models that detects language in text - Contributions welcome

### Goal
- To measure the speed, accuracy and memory usage of language detection algorithms for online usecases. Batch usecases are out of scope.

### Dataset options
- [Kaggle language detection dataset](https://www.kaggle.com/martinkk5575/language-detection)
  - Languages supported ```{'Chinese', 'Romanian', 'Persian', 'Korean', 'Pushto', 'Thai', 'Japanese', 'Indonesian', 'Portugese', 'Urdu', 'Swedish', 'Turkish', 'Latin', 'Hindi', 'Arabic', 'Spanish', 'English', 'Dutch', 'Estonian', 'Tamil', 'French', 'Russian'}```
  - 22K records
  - There is a known issue 17 of the GT labels are wrong, but it is negligible.

### Dataset EDA
- TBD

### How contribute?
- Add a new class for each algorithm implementation, use benchmark_langid.py as reference.
- Reuse the Language Dictionary
- Follow the csv file formats for results so it will be easy to collate later.
- Use psutil resident set size (RSS) for memory usage during load + dummy predict (see usage examples in any of the algorithms)
- Please submit a PR so we can follow the review process.
- Collaborators can serve as peer reviewers.

### Results
| algorithm    | mean   | max    | min    | median | mem       | accuracy |
| ------------ | ------ | ------ | ------ | ------ | --------- | -------- |
| Langid       | 0.0005 | 0.0145 | 0.0001 | 0.0004 | 34.46 mb  | 0.9543   |
| Fasttext_ftz | 0.0002 | 0.0014 | 0.0000 | 0.0001 | 0.71 mb   | 0.9673   |
| Fasttext_bin | 0.0001 | 0.0031 | 0.0000 | 0.0001 | 131.11 mb | 0.9751   |

