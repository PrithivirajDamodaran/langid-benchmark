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

### Results - Run on a fresh GCP `e2-medium (2 vCPU;	4GB Memory)`
| algorithm    | mean   | max    | min    | median | mem         | accuracy |
| ------------ | ------ | ------ | ------ | ------ | ----------- | -------- |
| Langid       | 0.0009 | 0.0047 | 0.0003 | 0.0008 | 9.54 mb     | 0.9543   |
| Fasttext_ftz | 0.0002 | 0.0018 | 0.0000 | 0.0002 | 0.0 mb      | 0.9673   |
| Fasttext_bin | 0.0001 | 0.0005 | 0.0000 | 0.0001 | 124.26 mb   | 0.9751   |
| CLD3         | 0.0007 | 0.0022 | 0.0000 | 0.0006 | TBD         | 0.9557   |
| CLD2         | 0.0000 | 0.0006 | 0.0000 | 0.0000 | TBD         | 0.9308   |

