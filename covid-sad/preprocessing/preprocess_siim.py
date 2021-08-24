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
from sklearn.model_selection import train_test_split
import click


@click.command()
@click.option('--configPath', default='config.yml', help='Covid CXR config to use for output paths')
def preprocess_siim(configpath):
    """Prepares the siim dataset for training, run after CXR to add images to CSVs"""
    siim = SIIM(yaml.full_load(open(os.getcwd() + configpath, 'r')))
    siim.filter()
    trainDF, valDF, testDF = siim.get_splits()
    print(trainDF.head)


class SIIM:

    def __init__(self, cfg) -> None:
        path = cfg['PATHS']['SIIM_DATA']
        self.cfg = cfg
        self.df = pd.read_csv(path + 'train.csv')
        self.df['filename'] = path + self.cfg['SIIM']['RESOLUTION'] + \
            os.path.sep + 'train' + os.path.sep + 'train' + os.path.sep + self.df['StudyInstanceUID'] + '_' + self.df['ImageInstanceUID'] + '.jpg'
        n_classes = len(cfg['DATA']['CLASSES'])
        class_dict = {cfg['DATA']['CLASSES'][i]: i for i in range(n_classes)}  # Map class name to number
        label_dict = {i: cfg['DATA']['CLASSES'][i] for i in range(n_classes)}  # Map class name to number
        self.df['label'] = [class_dict[cfg['SIIM']['MAPPING'][label]] for label in self.df['label_id']]

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


if __name__ == '__main__':
    preprocess_siim()
