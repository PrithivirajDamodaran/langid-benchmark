import psutil
import os
import gcld3
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


class BenchmarkCLD3():

      def __init__(self):
           """ dummy run to load the model and get memory usage """
           p = psutil.Process(os.getpid())
           mem_before = p.memory_info().rss
           self.model = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)
           self.model.FindLanguage(text="Hello World")
           mem_after = p.memory_info().rss
           mem_model = getsize(self.model)
           self.mem_usage = (mem_after - mem_before) + mem_model
           logger.info('Default model for CLD3 loaded ...')

      def _detect_language(self, row):
              """Detects language for the given text"""
              text = row['Text']
              gt = row['language']
              start = time.time()
              pred = self.model.FindLanguage(text=text).language
              end = time.time() - start
              match = gt == pred      
              return pd.Series([pred, end, match])

      def __call__(self) -> List[pd.DataFrame]:
          """ detects language for all the texts and calculates benchmark """
          logger.info('Benchmark for CLD3 started ...')
          MB = 1024 * 1024
          df = pd.read_csv("data/dataset.csv")  
          df['language'] = df['language'].apply(lambda x:lang_dict[x])
          df[['pred_lang', 'time_taken', 'ismatch']] = df.progress_apply(self._detect_language ,axis=1)
          time_taken = df["time_taken"].to_list()
          correct_predictions = df[df['ismatch'] == True].shape[0]
          total_predictions = df.shape[0]

          d = {"algorithm": "CLD3",
               "mean": np.mean(time_taken),
               "max" : np.max(time_taken),
               "min" : np.min(time_taken),
               "median" : np.median(time_taken),
               "mem": str(format(self.mem_usage/ MB,'f')) + " mb",
               "accuracy":correct_predictions/ total_predictions
               }
          
          df.to_csv("data/predictions_cld3.csv", index = False)
          summary_df = pd.DataFrame([d]) 

          logger.info('Benchmark for CLD3 ended ...')
          logger.info('See predictions_cld3.csv files...')

          return [summary_df]
