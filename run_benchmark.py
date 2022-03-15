import argparse
from argparse import ArgumentParser
import logging
import logging.config
import sys

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


from benchmark_langid import BenchmarkLangid
from benchmark_fasttext import BenchmarkFasttext
### ADD YOUR IMPLEMENTATIONS HERE ###




if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='run_benchmark.py',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    parser.add_argument('-al', nargs='+', default=["*"], help="""
                            You can pass one or more of the supported algorithms:
                            Langid,
                            Fasttext,
                            CLD2,
                            CLD3      
                            """)
    args = parser.parse_args()
    algorithm_list = set(args.al)

    logger.info('Benchmarking started.....')
    
    if "Langid" in algorithm_list or "*" in algorithm_list:
        benchmark_langid = BenchmarkLangid()
        benchmark_langid()
    if "Fasttext" in algorithm_list or "*" in algorithm_list:
        benchmark_fasttext = BenchmarkFasttext()
        benchmark_fasttext()

    ### ADD YOUR IMPLEMENTATIONS HERE ###        

    logger.info('Benchmarking ended.....')