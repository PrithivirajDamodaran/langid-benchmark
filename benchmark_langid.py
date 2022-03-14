import py3langid as langid
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
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')


class BenchmarkLangid():

      def __init__(self):
           """ dummy run to load the model and IDENTIFIER global variable has the model loaded """
           langid.classify("hello")
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
          langid_df = pd.read_csv("./dataset.csv")  
          langid_df['language'] = langid_df['language'].apply(lambda x:lang_dict[x])
          langid_df[['pred_lang', 'time_taken', 'ismatch']] = langid_df.progress_apply(self._detect_language ,axis=1)
          time_taken = langid_df["time_taken"].to_list()
          correct_predictions = langid_df[langid_df['ismatch'] == True].shape[0]
          total_predictions = langid_df.shape[0]
          from py3langid.langid import IDENTIFIER
          d = {"algorithm": "Langid",
               "mean": np.mean(time_taken),
               "max" : np.max(time_taken),
               "min" : np.min(time_taken),
               "median" : np.median(time_taken),
               "mem": str(round(getsize(IDENTIFIER) / math.pow(10,6),2)) + " mb",
               "accuracy":correct_predictions/ total_predictions
               }
          summary_langid_df = pd.DataFrame([d]) 
          langid_df.to_csv("./predictions_langid.csv", index = False)
          summary_langid_df.to_csv("./benchmark_langid.csv", index = False)
          logger.info('Benchmark for Langid ended ...')
          logger.info('See benchmark_langid.csv and predictions_langid.csv files...')
