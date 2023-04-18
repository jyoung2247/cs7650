import jsonlines
import sys
from datasets import load_dataset


def split_data(input_filepath, output_filepath):
     max_file_size = 3e+9
     current_file_size = 0
     current_file_number = 0

     with jsonlines.open(input_filepath) as reader:
          writer = jsonlines.open(output_filepath + f'_part_{current_file_number}.json', mode='w')
          for obj in reader:
                    if not obj['edited'] and not obj['score_hidden'] and obj['body'] != '[deleted]':
                         reddit_data = {}
                         reddit_data['score'] = obj['score']
                         reddit_data['body'] = obj['body']
                         reddit_data['ups'] = obj['ups']
                         reddit_data['downs'] = obj['downs']
                         reddit_data['controversiality'] = obj['controversiality']
                         reddit_data['subreddit'] = obj['subreddit']
                         reddit_data['created_utc'] = obj['created_utc']
                         obj = reddit_data
                         current_file_size += sys.getsizeof(obj)
                         if current_file_size > max_file_size:
                              writer.close()
                              current_file_number+=1
                              print("current file number: ", current_file_number)
                              writer = jsonlines.open(output_filepath + f'_part_{current_file_number}.json', mode='w')
                              current_file_size = 0
                         writer.write(obj)

def create_dataset_small(input_filepath, output_filepath, dataset_len):
     with jsonlines.open(input_filepath) as reader:
          writer = jsonlines.open(output_filepath, mode='w')
          idx = 0
          for obj in reader:
               if idx < dataset_len:
                    writer.write(obj)
                    idx+=1
               else:
                    break
def load_data():
     access_token = "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"
     dataset = load_dataset("jyoung2247/reddit_data_small", use_auth_token=access_token)
     return dataset

#Example of how to load df from jsonlines
#df = pd.read_json('reddit_data_small.json', lines=True)

#split_data('D:\Datasets\RC_2015-01.json', 'D:\Datasets\\reddit_data')

#create_dataset_small('D:\Datasets\\reddit_data_part_0.json', 'reddit_data_small.json', 100000)