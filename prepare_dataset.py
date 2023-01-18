from datetime import datetime
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np
import itertools
import argparse
import json
import re
import os

tqdm.pandas()

def string_to_float(time_):
    time = datetime.strptime(time_, '%M:%S.%f')
    return round(time.minute * 60. + time.second * 1. + time.microsecond * 1e-6, 5)

def refine_sentence(sentence, lang='ko'):
    if lang=='ko':
        pattern = '[^가-힣a-zA-Z0-9 \.\,]'
    else:
        pattern = '[^a-zA-Z0-9 \.\,\'\-]'

    return re.sub(pattern, '', sentence)


def refine_timestamps_sentences(row):
    row 

    row['duration'] = float(row['duration'])
    row['start'] = string_to_float(row['start'])
    row['end'] = string_to_float(row['end'])

    is_start = row['start'] > row['duration']
    if is_start:
        row['start'] = row['duration']

    is_end = row['end'] > row['duration']
    if is_end:
        row.loc['end'] = row.loc['duration']

    err_timestamp = row['start'] >= row['end'] or is_start
    if not err_timestamp:
        row['timestamps'] = [row['start'], row['end']]
        row['sentences_ko'] = refine_sentence(row['sentences_ko'])
        row['sentences_en'] = refine_sentence(row['sentences_en'], 'en')

    row['drop'] = err_timestamp
    return row

def refine_data(json_folder):
    file_list = list(set(glob(os.path.join(json_folder,'**/**.json'), recursive=True)))

    datas = []
    print('Loading data...')
    for file in file_list:
        try:
            datas.append(json.load(open(file)))
        except:
            datas.append(json.load(open(file, encoding='utf-8-sig')))

    df_jsons = pd.DataFrame(datas)

    df_sentences = []
    for i in tqdm(range(len(df_jsons))):
        duration = df_jsons.loc[i, 'duration']
        video_name = df_jsons.loc[i, 'video_name']
        domain_id = df_jsons.loc[i, 'domain_id'][:2]
        df = pd.DataFrame(df_jsons.loc[i, 'sentences'])
        df['duration'] = duration
        df['video_name'] = video_name
        df['domain_id'] = domain_id
        df_sentences.append(df.copy())

    df_sentences = pd.concat(df_sentences, axis=0, ignore_index=True)
    
    df_sentences[['start', 'end']] = pd.DataFrame(df_sentences['timestamps'].tolist(), index=df_sentences.index)
    df_sentences['drop'] = False

    print('Preprocessing data.....')
    df_sentences = df_sentences.progress_apply(refine_timestamps_sentences, axis=1)
    df_sentences = df_sentences[~df_sentences['drop']]

    return df_sentences

def split_datasets(data, split_file):

    if not os.path.exists('data/dense_video_caption'):
        os.makedirs('data/dense_video_caption', exist_ok = True)

    if split_file:
        split_list = json.load(open(split_file))
    else:
        video_names = data['video_name'].unique()
        np.random.shuffle(video_names)
        train_list = video_names[:int(len(video_names)*0.8)]
        valid_list = video_names[int(len(video_names)*0.8):int(len(video_names)*0.9)]
        test_list = video_names[int(len(video_names)*0.9):]
        split_list = {'train':train_list, 'valid':valid_list, 'test':test_list}

    for mode in ['train','valid', 'test']:
        print('Parsing', mode, 'dataset...')
        tmp_file = {'ko':{}, 'en':{}}

        for video_name in tqdm(split_list[mode]):
            tmp_df = data.query(f'video_name=="{video_name}"')
            duration = tmp_df['duration'].iloc[0]

            for lang in ['ko', 'en']:
                tmp_file[lang][os.path.splitext(video_name)[0]] = {'duration' : duration, 'timestamps': tmp_df['timestamps'].tolist(), 'sentences': tmp_df[f'sentences_{lang}'].to_list()}

        json.dump(tmp_file['ko'], open(f'data/dense_video_caption/dense_video_caption_{mode}_korean.json','w'), indent=4, ensure_ascii=False)
        json.dump({key : ' '.join(value['sentences']) for key, value in tmp_file['ko'].items()}, open(f'data/dense_video_caption/dense_video_caption_{mode}_korean_para.json','w'), indent=4, ensure_ascii=False)
        json.dump(tmp_file['en'], open(f'data/dense_video_caption/dense_video_caption_{mode}_english.json','w'), indent=4, ensure_ascii=False)
        json.dump({key : ' '.join(value['sentences']) for key, value in tmp_file['en'].items()}, open(f'data/dense_video_caption/dense_video_caption_{mode}_english_para.json','w'), indent=4, ensure_ascii=False)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', type=str, required=True)
    parser.add_argument('--split_list', type=str, default=None)
    args = parser.parse_args()

    data = refine_data(args.data_folder)
    print('Collecting data...')
    split_datasets(data, args.split_list)
