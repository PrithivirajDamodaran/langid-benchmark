import py3langid as langid
import psutil
import os
import time
import math
import numpy as np
import sys
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
           """ dummy run to load the model and get memory usage """
           p = psutil.Process(os.getpid())
           mem_before = p.memory_info().rss
           langid.classify("Hello World")
           mem_after = p.memory_info().rss
           self.mem_usage = mem_after - mem_before
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

      def __call__(self):
          """ detects language for all the texts and calculates benchmark """
          logger.info('Benchmark for Langid started ...')
          MB = 1024 * 1024
          langid_df = pd.read_csv("data/dataset.csv")  
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
               "mem": str(round(self.mem_usage/ MB,2)) + " mb",
               "accuracy":correct_predictions/ total_predictions
               }
            
          summary_langid_df = pd.DataFrame([d]) 
          langid_df.to_csv("data/predictions_langid.csv", index = False)
          summary_langid_df.to_csv("data/benchmark_langid.csv", index = False)
          logger.info('Benchmark for Langid ended ...')
          logger.info('See benchmark_langid.csv and predictions_langid.csv files...')
