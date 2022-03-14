import py3langid as langid
from py3langid.langid import IDENTIFIER
import time
import math
import numpy as np
import sys
from numbers import Number
from collections import deque
from collections.abc import Set, Mapping
import pandas as pd 
from language_dictionary import lang_dict
from tqdm.auto import tqdm
pd.set_option("max_colwidth", None)
tqdm.pandas()
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')


class BenchmarkLangid():

      def __init__(self):
           """ dummy run to load the model and IDENTIFIER global variable has the model loaded """
           langid.classify("hello")
           self.ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)
           logger.info('Default model for Langid loaded ...')

      def _detect_language(self, row):
              """Detects language for the given text"""
              text = row['Text']
              gt = row['language']
              start = time.time()
              pred, _ = langid.classify(text)
              end = time.time() - start
              match = gt == pred      
              return pd.Series([pred, end, match])

      def _getsize(self, obj_0):
          # https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
          """Recursively iterate to sum size of object & members."""
          _seen_ids = set()
          def inner(obj):
              obj_id = id(obj)
              if obj_id in _seen_ids:
                  return 0
              _seen_ids.add(obj_id)
              size = sys.getsizeof(obj)
              if isinstance(obj, self.ZERO_DEPTH_BASES):
                  pass # bypass remaining control flow and return
              elif isinstance(obj, (tuple, list, Set, deque)):
                  size += sum(inner(i) for i in obj)
              elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
                  size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
              # Check for custom object instances - may subclass above too
              if hasattr(obj, '__dict__'):
                  size += inner(vars(obj))
              if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
                  size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
              return size
          return inner(obj_0)                

      def __call__(self):
          """ detects language for all the texts and calculates benchmark """
          logger.info('Benchmark for Langid started ...')
          langid_df = pd.read_csv("./dataset.csv")  
          langid_df['language'] = langid_df['language'].apply(lambda x:lang_dict[x])
          langid_df[['pred_lang', 'time_taken', 'ismatch']] = langid_df.progress_apply(self._detect_language ,axis=1)
          time_taken = langid_df["time_taken"].to_list()
          correct_predictions = langid_df[langid_df['ismatch'] == True].shape[0]
          total_predictions = langid_df.shape[0]
          d = {"algorithm": "Langid",
               "mean": np.mean(time_taken),
               "max" : np.max(time_taken),
               "min" : np.min(time_taken),
               "median" : np.median(time_taken),
               "mem": str(round(self._getsize(IDENTIFIER) / math.pow(10,6),2)) + " mb",
               "accuracy":correct_predictions/ total_predictions
               }
          summary_langid_df = pd.DataFrame([d]) 
          langid_df.to_csv("./predictions_langid.csv", index = False)
          summary_langid_df.to_csv("./benchmark_langid.csv", index = False)
          logger.info('Benchmark for Langid ended ...')
          logger.info('See benchmark_langid.csv and predictions_langid.csv files...')
