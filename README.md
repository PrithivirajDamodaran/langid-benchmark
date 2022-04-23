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
- Run on a fresh GCP `e2-medium (2 vCPU;	4GB Memory)`
- Result Table:

| algorithm    | mean   | max    | min    | median | mem          | accuracy |
| ------------ | ------ | ------ | ------ | ------ | ------------ | -------- |
| Langid       | 0.0004 | 0.0687 | 0.0001 | 0.0003 | 34.43 mb     | 0.9543   |
| Fasttext_ftz | 0.0001 | 0.0013 | 0.0000 | 0.0001 | <b><span style="color:green"> 0.81 mb </span></b> | 0.9673   |
| Fasttext_bin | 0.0001 | 0.0004 | 0.0000 | <b><span style="color:green"> 0.0001 </span></b> | 130.84 mb    | <b><span style="color:green"> 0.9751 </span></b> |
| CLD3         | 0.0003 | 0.0024 | 0.0000 | 0.0002 | TBD          | 0.9557   |
| CLD2         | 0.0000 | 0.0004 | 0.0000 | 0.0000 | TBD          | 0.9308   |

