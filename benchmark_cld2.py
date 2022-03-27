import psutil
import os
import pycld2 as cld2
import regex
import time
import math
import numpy as np
import sys
import pandas as pd 
from language_dictionary import lang_dict
from object_size import getsize
from tqdm.auto import tqdm
pd.set_option("max_colwidth", None)
tqdm.pandas()
from typing import List

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')


class BenchmarkCLD2():

      def __init__(self):
           """ dummy run to load the model and get memory usage """
           p = psutil.Process(os.getpid())
           mem_before = p.memory_info().rss
           cld2.detect('Hello World')
           mem_after = p.memory_info().rss
           self.mem_usage = mem_after - mem_before
           logger.info('Default model for CLD2 loaded ...')

      def _detect_language(self, row):
              """Detects language for the given text"""
              text = row['Text']
              gt = row['language']
              start = time.time()
              pred = cld2.detect(text)[2][0][1]
              end = time.time() - start
              match = gt == pred      
              return pd.Series([pred, end, match])

      def __call__(self) -> List[pd.DataFrame]:
          """ detects language for all the texts and calculates benchmark """
          logger.info('Benchmark for CLD2 started ...')
          MB = 1024 * 1024
          df = pd.read_csv("data/dataset.csv")  
          df['language'] = df['language'].apply(lambda x:lang_dict[x])
          # https://github.com/mikemccand/chromium-compact-language-detector/issues/22#issuecomment-707999784
          RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")
          df['Text'] = df['Text'].apply(lambda x:RE_BAD_CHARS.sub("", x))
          df[['pred_lang', 'time_taken', 'ismatch']] = df.progress_apply(self._detect_language ,axis=1)
          time_taken = df["time_taken"].to_list()
          correct_predictions = df[df['ismatch'] == True].shape[0]
          total_predictions = df.shape[0]

          d = {"algorithm": "CLD2",
               "mean": np.mean(time_taken),
               "max" : np.max(time_taken),
               "min" : np.min(time_taken),
               "median" : np.median(time_taken),
               "mem": str(round(self.mem_usage/ MB,2)) + " mb",
               "accuracy":correct_predictions/ total_predictions
               }
          
          df.to_csv("data/predictions_cld2.csv", index = False)
          summary_df = pd.DataFrame([d]) 

          logger.info('Benchmark for CLD2 ended ...')
          logger.info('See predictions_cld2.csv files...')

          return [summary_df]
