import os
import warnings
import pickle

warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=RuntimeWarning)

# Third party imports
import click

import numpy as np

import pandas as pd

import imageio

from texttable import Texttable

from PIL import Image
from PIL.ImageFilter import MedianFilter, GaussianBlur

from sklearn.externals import joblib
from skimage.measure import regionprops

from mahotas.features import surf

from sklearn.preprocessing import MinMaxScaler


FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_FOLDER_PATH = os.path.join(FOLDER_PATH, 'models')



# ###############
# ACTUAL COMMANDS
# ###############

@click.group()
def cli():
    pass


@click.command()
@click.argument('image_path')
def info(image_path):

    # Printing the file path
    text_table = Texttable()
    text_table.set_deco(Texttable.HEADER)

    # Loading the image from the file
    image_dict = load_image(image_path)

    # Meta info about shape and size of the image
    shape = image_dict['gray'].shape
    meta_info_dict = {
        '': '',
        'file size (KB)':       os.path.getsize(image_path) / 1028,
        'width':                shape[1],
        'height':               shape[0]
    }
    text_table.add_rows(list(meta_info_dict.items()))

    # Calculating the mean values for all the color channels
    image_info_dict = {
        'mean grayscale':       np.mean(image_dict['gray']),
        'mean red channel':     np.mean(image_dict['red']),
        'mean green channel':   np.mean(image_dict['green']),
        'mean blue channel':    np.mean(image_dict['blue'])
    }
    text_table.add_rows(list(image_info_dict.items()))

    text_table.header(['Info', 'Value'])
    click.echo('{}'.format(text_table.draw()))


@click.command()
@click.argument('image_path')
@click.option('--percent', is_flag=True)
def exist(image_path, percent):
    # First of all, we need to format the image into the correct format, so that the features can be extracted properly
    # later on.
    temp_path = os.path.join(FOLDER_PATH, '_temp.jpeg')
    pil_image = Image.open(image_path)

    # We need to cut the borders because the time stamps will be an issue
    pil_image = pil_image.crop((0, 100, 1280, 680))

    pil_image = pil_image.resize((640, 360))

    pil_image.save(temp_path, 'jpeg')

    # Here we extract the features from the image and then delete the temporary file again.
    # The features are returned as a dict, but they need to have the form of a pandas dataframe
    features_dict = extract_features(temp_path)
    features_dataframe = pd.DataFrame([features_dict])

    # Scaling the features and removing the most unimportant ones
    scaler = joblib.load(os.path.join(MODEL_FOLDER_PATH, 'scaler.pkl'))
    features_dataframe = scaler.transform(features_dataframe)
    features_dataframe.drop(['surf bin 15','surf bin 0','surf bin 12','surf bin 19','blue bin 4','surf bin 6'], axis=1, inplace=True)

    # click.echo(features_dataframe)
    # Load the classification model and let it make a prediction
    model_path = '/home/jonas/Nextcloud/Programmieren/PyCharm/aragats/ml/clean/forest_model.pkl' # os.path.join(MODEL_FOLDER_PATH, 'forest_model.pkl')
    classification_model = joblib.load(model_path)

    prediction = classification_model.predict(features_dataframe)

    if percent:
        # Make a prediction, that will display the percentages
        probability_prediction = classification_model.predict_proba(features_dataframe)
        click.echo('no lightning probability:        {0:.2f} %'.format(probability_prediction[0][0] * 100))
        click.echo('lightning detected probability:  {0:.2f} %'.format(probability_prediction[0][1] * 100))
        click.echo('')

    if prediction[0] == 1:
        click.echo('lightning detected!')
    else:
        click.echo('no lightning.')


# ####################
# SUPPORTING FUNCTIONS
# ####################

def contains_lightning(image_path):
    # First of all, we need to format the image into the correct format, so that the features can be extracted properly
    # later on.
    temp_path = os.path.join(FOLDER_PATH, '_temp.jpeg')
    pil_image = Image.open(image_path)
    # We need to cut the borders because the time stamps will be an issue
    pil_image = pil_image.crop((0, 100, 1280, 680))
    pil_image = pil_image.resize((640, 360))
    pil_image.filter(MedianFilter(3))
    pil_image.save(temp_path, 'jpeg')

    # Here we extract the features from the image and then delete the temporary file again.
    # The features are returned as a dict, but they need to have the form of a pandas dataframe
    features_dict = extract_features(temp_path)
    features_dataframe = pd.DataFrame([features_dict])

    # Scaling the features and removing the most unimportant ones
    scaler = joblib.load(os.path.join(MODEL_FOLDER_PATH, 'scaler.pkl'))
    features_dataframe = scaler.transform(features_dataframe)
    features_dataframe.drop(['surf bin 15', 'surf bin 0', 'surf bin 12', 'surf bin 19', 'blue bin 4', 'surf bin 6'],
                            axis=1, inplace=True)

    # click.echo(features_dataframe)
    # Load the classification model and let it make a prediction
    model_path = os.path.join(MODEL_FOLDER_PATH, 'forest_model.pkl')
    classification_model = joblib.load(model_path)

    prediction = classification_model.predict(features_dataframe)
    print(prediction)

    if prediction[0] == 1:
        return True
    else:
        return False


def extract_surf_vector(cluster_model, image, k=20):
    # Extracting the surf vectors from the image
    surf_image = surf.dense(image, spacing=10)

    labels = cluster_model.predict(surf_image)
    vbow = np.bincount(labels, minlength=k)
    features = {}
    for value, index in zip(vbow, range(0, k)):
        features['surf bin {}'.format(index)] = value
    return features


def high_blue(image_gray, image_blue, threshold=180):
    # Counting how many pixles are above the given intensity value for the gray scale
    # and the blue channel
    gray_count = np.sum(image_gray > threshold)
    blue_count = np.sum(image_blue > threshold)

    # There We only need to see the special case of the gray scale count being zero
    # because this would cause a zero division.
    # that case means that the image doesnt contain gray scale values above the
    # threshold at all, which in turn means its probably not a lightning.
    if gray_count == 0:
        return 0
    else:
        return blue_count / gray_count


def n_top_values(array, n):
    array_copy = np.copy(array)
    array_copy[0, 0] = 0
    array_flattened = array_copy.flatten()
    index_array = array_flattened.argsort()
    index_array[:-n] = 0
    index_array_aligned = np.zeros(index_array.shape, dtype=index_array.dtype)
    for i in range(-(n+1), -1, 1):
        value = index_array[i]
        index_array_aligned[value] = value
    array_result = array_flattened[index_array_aligned]
    array_result = array_result.reshape((array.shape[0], array.shape[1]))
    return array_result


def histogram_n_bins(image, n=10, name='image'):
    bins = np.histogram(image, n, (0, 255))[0]
    features = {}
    for value, index in zip(bins, range(0, n)):
        features['{} bin {}'.format(name, index)] = value
    return features


def extract_features(image_path, blue_threshold=180, top_percent=0.05):
    # Loading the image in all color channels and gray scale value
    image_dict = load_image(image_path)
    area = image_dict['gray'].shape[0] * image_dict['gray'].shape[1]

    # Basic statistical info about the gray scale picture
    mean = np.mean(image_dict['gray'])
    top = np.max(image_dict['gray'])

    # High blue value
    high_blue_factor = high_blue(image_dict['gray'], image_dict['blue'], blue_threshold)

    # Creating the image, that only contain the top n intensity pixels
    n = int(area * top_percent)
    image_top = n_top_values(image_dict['gray'], n)

    # The mean value for the top pixels and the variance along the axes
    mean_top = np.mean(image_top)
    region_properties = regionprops((image_top > 1).astype(int), image_top)[0]
    x_variance = region_properties.weighted_moments_normalized[2, 0]
    y_variance = region_properties.weighted_moments_normalized[0, 2]

    features = {
        'max': top,
        'mean': mean,
        'mean_top': mean_top,
        'high_blue': high_blue_factor,
        'x_variance': x_variance,
        'y_variance': y_variance
    }

    # Extracting the surf features
    cluster_model_path = os.path.join(MODEL_FOLDER_PATH, 'surf_cluster.pkl')
    cluster_model = joblib.load(cluster_model_path)
    surf_features = extract_surf_vector(cluster_model, image_dict['gray'])

    features.update(surf_features)

    # Histogram binning
    features_histogram_gray = histogram_n_bins(image_dict['gray'], name='gray')
    features_histogram_blue = histogram_n_bins(image_dict['blue'], name='blue')

    #features.update(features_histogram_gray)
    features.update(features_histogram_blue)

    return features


def load_image(image_path):
    click.echo('')
    image_gray = imageio.imread(image_path, pilmode='L')

    image_color = imageio.imread(image_path)
    image_red, image_green, image_blue = image_split_colors(image_color)
    return {
        'gray':     image_gray,
        'red':      image_red,
        'green':    image_green,
        'blue':     image_blue
    }


def image_split_colors(image_color):
    image_red = image_color[:, :, 0]
    image_green = image_color[:, :, 1]
    image_blue = image_color[:, :, 2]
    return image_red, image_green, image_blue


class FeatureScaler:

    def __init__(self):
        self.scalers = {}

    def fit(self, dataframe):
        for key in list(dataframe.keys()):
            self.scalers[key] = MinMaxScaler()
            self.scalers[key].fit_transform(dataframe[[key]])

    def transform(self, dataframe):
        for key in list(dataframe.keys()):
            dataframe[key] = self.scalers[key].transform(dataframe[[key]])
        return dataframe

    def save(self, path):
        for key, scaler in self.scalers.items():
            scaler_path = os.path.join(path, key + "_scaler.pkl")
            joblib.dump(scaler, scaler_path)

    def load(self, path):
        for root, dirs, files in os.walk(path):

            for file in files:
                if '_scaler.pkl' in file:
                    key = file.replace('_scaler.pkl', '')
                    scaler_path = os.path.join(root, file)
                    self.scalers[key] = joblib.load(scaler_path)

            break


# ##############
# MAIN EXECUTION
# ##############

# Adding the commands to the command group
cli.add_command(info)
cli.add_command(exist)


if __name__ == '__main__':
    cli()
