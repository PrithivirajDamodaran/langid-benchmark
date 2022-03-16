import psutil
import os
import fasttext
import requests
import time
import math
import numpy as np
import sys
import os
import pandas as pd 
from language_dictionary import lang_dict
from tqdm.auto import tqdm
pd.set_option("max_colwidth", None)
tqdm.pandas()
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')


class BenchmarkFasttext():

    def __init__(self):
        """ Load the model """
        # https://fasttext.cc/docs/en/language-identification.html
        base_url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176'

        self.models = {}
        self.mem_usage = {}
        p = psutil.Process(os.getpid())
        for ext in ['ftz', 'bin']:
            fname = f'models/lid.176.{ext}'
            if not os.path.isfile(fname): 
                logger.info(f'Downloading the fastext {ext} model')
                response = requests.get(f'{base_url}.{ext}')
                open(fname, 'wb').write(response.content)

            logger.info(f'Loading the fastext {ext} model')
            mem_before = p.memory_info().rss
            self.models[ext] = fasttext.load_model(fname)
            self.models[ext].predict("Hello World")
            mem_after = p.memory_info().rss
            self.mem_usage[ext] = mem_after - mem_before

        logger.info('Fasttext models loaded ...')

    def _detect_language(self, row, model):
        """Detects language for the given text"""
        text = row['Text']
        gt = row['language']
        start = time.time()
        (pred,), _ = model.predict(text)  
        end = time.time() - start
        pred = pred[-2:]
        match = gt == pred      
        return pd.Series([pred, end, match])

    def __call__(self):
        """ detects language for all the texts and calculates benchmark """
        MB = 1024 * 1024
        df = pd.read_csv("data/dataset.csv")
        df['language'] = df['language'].apply(lambda x:lang_dict[x])

        for ext in ['ftz', 'bin']:
            logger.info(f'Benchmark for Fasttext {ext} started ...')
            df[['pred_lang', 'time_taken', 'ismatch']] = df.progress_apply(self._detect_language, model=self.models[ext], axis=1)
            time_taken = df["time_taken"].to_list()
            correct_predictions = df[df['ismatch'] == True].shape[0]
            total_predictions = df.shape[0]

            d = {
                "algorithm": f"Fasttext_{ext}",
                "mean": np.mean(time_taken),
                "max": np.max(time_taken),
                "min": np.min(time_taken),
                "median": np.median(time_taken),
                "mem": f'{str(round(self.mem_usage[ext] / MB,2))} mb',
                "accuracy": correct_predictions / total_predictions,
            }

            summary_df = pd.DataFrame([d])
            df.to_csv(f"data/predictions_fasttext_{ext}.csv", index = False)
            summary_df.to_csv(f"data/benchmark_fasttext_{ext}.csv", index = False)

            logger.info(f'Benchmark for Fasttext {ext} ended ...')
            logger.info(f'See benchmark_fasttext_{ext}.csv and predictions_fasttext_{ext}.csv files...')
