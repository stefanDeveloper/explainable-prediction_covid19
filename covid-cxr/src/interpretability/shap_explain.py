
import shap
import yaml
import os
import numpy as np
from tensorflow.keras.models import load_model

# Load relevant constants from project config file
cfg = yaml.full_load(open(os.getcwd() + "/config.yml", 'r'))
lime_dict = {}
# Load trained model's weights
lime_dict['MODEL'] = load_model(cfg['PATHS']['MODEL_TO_LOAD'], compile=False)
# Create ImageDataGenerator for test set
test_img_gen = ImageDataGenerator(preprocessing_function=remove_text,
                                samplewise_std_normalization=True, samplewise_center=True)
test_generator = test_img_gen.flow_from_dataframe(dataframe=lime_dict['TEST_SET'], directory=cfg['PATHS']['RAW_DATA'],
x_col="filename", y_col='label_str', target_size=tuple(cfg['DATA']['IMG_DIM']), batch_size=1,
class_mode='categorical', validate_filenames=False, shuffle=False)
lime_dict['TEST_GENERATOR'] = test_generator

# select a set of background examples to take an expectation over
background = x_train[np.random.choice(x_train.shape[0], 100, replace=False)]

# explain predictions of the model on four images
e = shap.DeepExplainer(lime_dict['MODEL'], background)
# ...or pass tensors directly
# e = shap.DeepExplainer((model.layers[0].input, model.layers[-1].output), background)
shap_values = e.shap_values(x_test[1:5])

# plot the feature attributions
shap.image_plot(shap_values, -x_test[1:5])