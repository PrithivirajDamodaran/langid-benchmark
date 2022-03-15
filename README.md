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


