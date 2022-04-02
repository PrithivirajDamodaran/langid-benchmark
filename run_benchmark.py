import argparse
from argparse import ArgumentParser
import logging
import logging.config
from mdtable import MDTable
import pandas as pd
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
from benchmark_cld3 import BenchmarkCLD3
from benchmark_cld2 import BenchmarkCLD2
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
    
    summary_df_list = []
    if "Langid" in algorithm_list or "*" in algorithm_list:
        benchmark_langid = BenchmarkLangid()
        summary_df_list.extend(benchmark_langid())
    if "Fasttext" in algorithm_list or "*" in algorithm_list:
        benchmark_fasttext = BenchmarkFasttext()
        summary_df_list.extend(benchmark_fasttext())
    if "CLD3" in algorithm_list or "*" in algorithm_list:
        benchmark_cld3 = BenchmarkCLD3()
        summary_df_list.extend(benchmark_cld3())
    if "CLD2" in algorithm_list or "*" in algorithm_list:
        benchmark_cld2 = BenchmarkCLD2()
        summary_df_list.extend(benchmark_cld2())

    summary_df = pd.concat(summary_df_list)
    summary_df.to_csv("data/benchmark_results.csv", index=False, float_format='%.4f')        

    ### ADD YOUR IMPLEMENTATIONS HERE ###        
    

    logger.info('Writing Results')
    markdown = MDTable('data/benchmark_results.csv')
    markdown_string_table = markdown.get_table()

    with open('README.md', 'r') as f:
        file_content = f.read()

    new_file_content = file_content.split('### Results\n')[0] + '### Results\n' + markdown_string_table

    with open('README.md', 'w') as f:
        print(new_file_content, file=f)

    logger.info('Benchmarking ended.....')