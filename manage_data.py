import jsonlines
import sys


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
                    # reddit_data = {}
                    # reddit_data['score'] = obj['score']
                    # reddit_data['body'] = obj['body']
                    # reddit_data['body'] = obj['body'] + obj['subreddit']
                    # reddit_data['body'] = obj['body'] + " [SEP] " + obj['subreddit']
                    # reddit_data['body'] = obj['body'] + " [SEP] " + obj['subreddit'] + " [SEP] " + obj['created_utc']
                    # obj = reddit_data
                    writer.write(obj)
                    idx+=1
               else:
                    break
def get_score_distribution(input_filepath, output_filepath):
      with jsonlines.open(input_filepath) as reader:
          writer = jsonlines.open(output_filepath, mode='w')
          distributions = {}
          distributions['-101_to_-inf'] = 0
          distributions['-100_to_-21'] = 0
          distributions['-20_to_-11'] = 0
          distributions['-10_to_-6'] = 0
          distributions['-5_to_-1'] = 0
          distributions['0'] = 0
          distributions['1'] = 0
          distributions['2'] = 0
          distributions['3'] = 0
          distributions['4'] = 0
          distributions['5'] = 0
          distributions['6_to_10'] = 0
          distributions['11_to_50'] = 0
          distributions['51_to_100'] = 0
          distributions['101_to_500'] = 0
          distributions['501_to_1000'] = 0
          distributions['1001_to_5000'] = 0
          distributions['5001_to_10000'] = 0
          distributions['10001_to_inf'] = 0
          for obj in reader:
               if obj['score'] <= -101:
                    distributions['-101_to_-inf'] += 1
               elif obj['score'] >= -100 and obj['score'] <= -21:
                    distributions['-100_to_-21'] += 1
               elif obj['score'] >= -20 and obj['score'] <= -11:
                    distributions['-20_to_-11'] += 1
               elif obj['score'] >= -10 and obj['score'] <= -6:
                    distributions['-10_to_-6'] += 1
               elif obj['score'] >= -5 and obj['score'] <= -1:
                    distributions['-5_to_-1'] += 1
               elif obj['score'] == 0:
                    distributions['0'] += 1
               elif obj['score'] == 1:
                    distributions['1'] += 1
               elif obj['score'] == 2:
                    distributions['2'] += 1
               elif obj['score'] == 3:
                    distributions['3'] += 1
               elif obj['score'] == 4:
                    distributions['4'] += 1
               elif obj['score'] == 5:
                    distributions['5'] += 1
               elif obj['score'] >= 6 and obj['score'] <= 10:
                    distributions['6_to_10'] += 1
               elif obj['score'] >= 11 and obj['score'] <= 50:
                    distributions['11_to_50'] += 1
               elif obj['score'] >= 51 and obj['score'] <= 100:
                    distributions['51_to_100'] += 1
               elif obj['score'] >= 101 and obj['score'] <= 500:
                    distributions['101_to_500'] += 1
               elif obj['score'] >= 501 and obj['score'] <= 1000:
                    distributions['501_to_1000'] += 1
               elif obj['score'] >= 1001 and obj['score'] <= 5000:
                    distributions['1001_to_5000'] += 1
               elif obj['score'] >= 1001 and obj['score'] <= 5000:
                    distributions['1001_to_5000'] += 1
               elif obj['score'] >= 5001 and obj['score'] <= 10000:
                    distributions['5001_to_10000'] += 1
               elif obj['score'] >= 10001:
                    distributions['10001_to_inf'] += 1
          writer.write(distributions)

#Example of how to load df from jsonlines
#df = pd.read_json('reddit_data_small.json', lines=True)

#split_data('D:\Datasets\RC_2015-01.json', 'D:\Datasets\\reddit_data')

#create_dataset_small('D:\Datasets\\reddit_data_part_0.json', 'reddit_data_small.json', 100000)

get_score_distribution("reddit_data_small.json", "reddit_data_small_distribution.json")