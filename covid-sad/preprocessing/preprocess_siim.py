from typing import Tuple
import numpy as np
import pandas as pd
import pydicom as dicom
import yaml
import os
import pathlib
import shutil
import cv2
from tqdm import tqdm
import tensorflow as tf
from sklearn.model_selection import train_test_split
import click



@click.command()
@click.option('--configPath', default='config.yml', help='Covid CXR config to use for output paths')
@click.option('--append', is_flag=True, help='Append file information to existing covid cxr csvs.')
def preprocess_siim(configpath, append):
    """Prepares the siim dataset for training, run after CXR to add images to CSVs"""
    cfg = yaml.full_load(open(os.getcwd() + os.path.sep + configpath, 'r'))
    siim = SIIM(cfg)
    siim.filter()
    trainDF, valDF, testDF = siim.get_splits()
    
    if not os.path.exists(cfg['PATHS']['PROCESSED_DATA']):
        os.makedirs(cfg['PATHS']['PROCESSED_DATA'])

    trainPath = cfg['PATHS']['TRAIN_SET']
    valPath = cfg['PATHS']['VAL_SET']
    testPath = cfg['PATHS']['TEST_SET']

    if append:
        fileDFTrain = pd.read_csv(trainPath, index_col=0)
        fileDFVal = pd.read_csv(valPath, index_col=0)
        fileDFTest = pd.read_csv(testPath, index_col=0)

        fileDFTrain = pd.concat([fileDFTrain, trainDF])
        fileDFVal = pd.concat([fileDFVal, valDF])
        fileDFTest = pd.concat([fileDFTest, testDF])
    else:
        fileDFTrain = trainDF
        fileDFVal = valDF
        fileDFTest = testDF

    fileDFTrain.to_csv(trainPath)
    fileDFVal.to_csv(valPath)
    fileDFTest.to_csv(testPath)


class SIIM:

    def __init__(self, cfg) -> None:
        self.cfg = cfg
        path = self.cfg['PATHS']['SIIM_DATA']
        csvDF = pd.read_csv(path + 'train.csv')
        self.df = pd.DataFrame(tf.io.gfile.glob(path + self.cfg['SIIM']['RESOLUTION'] + \
            '/' + 'train' + '/' + 'train' + '/' + '*.jpg'), columns=['filename'])
        self.df['filename'] = os.getcwd() + '/' + self.df['filename']
        self.df['ImageInstanceUID'] = self.df.apply(lambda row: add_id_to_row(row), axis=1)
        n_classes = len(cfg['DATA']['CLASSES'])
        class_dict = {cfg['DATA']['CLASSES'][i]: i for i in range(n_classes)}
        csvDF['label'] = [class_dict[cfg['SIIM']['MAPPING'][label]] for label in csvDF['label_id']]
        self.df = self.df.merge(csvDF, on='ImageInstanceUID', suffixes=('', '_y'))
        self.df = self.df[['filename', 'label']]
        self.df['label_str'] = self.df.apply(lambda row: get_label_str(row), axis=1)

    def filter(self) -> None:
        pass

    def get_splits(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        val_split = self.cfg['DATA']['VAL_SPLIT']
        test_split = self.cfg['DATA']['TEST_SPLIT']
        file_df_train, file_df_test = train_test_split(
            self.df, test_size=test_split, stratify=self.df['label'])
        relative_val_split = val_split / (1 - test_split)
        file_df_train, file_df_val = train_test_split(file_df_train, test_size=relative_val_split,
                                                      stratify=file_df_train['label'])
        return file_df_train, file_df_val, file_df_test


def add_id_to_row(row):
    tmp = row['filename'].split("/")[-1]
    tmp = tmp.split(".")[0]
    tmp = tmp.split("_")[-1]
    return tmp
def get_label_str(row):
    if row['label'] == 0:
        return 'non-COVID-19'
    else:
        return 'COVID-19'

if __name__ == '__main__':
    preprocess_siim()
