# standard library imports
# Python2 and Python3 inter compatibility regarding the print syntax
from __future__ import print_function
import getopt
import json
import math
import os

# third party imports
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import numpy
import click

# local package imports
# Importing the main lightning image processing library
from lightnimage.image import LightningImage
from lightnimage.engine import SimpleAreaSegmentationEngine
from lightnimage.engine import SimpleAreaGroupingEngine
from lightnimage.engine import CustomSequenceAreaSegmentationEngine
from lightnimage.engine import SimpleLightningPreprocessingEngine
from lightnimage.util import draw_areas

from classify import contains_lightning, FeatureScaler


@click.group()
def cli():
    pass


@click.command()
@click.argument('image_path')
@click.argument('reference_path')
@click.option('--save', '-s', type=str, required=True)
def box(image_path, reference_path, save):
    click.echo('Localizing lightnings within the images and calculating the bounding boxes')
    # First of all we need to classify, whether the image actually contains a lightning or not
    lightning_detected = contains_lightning(image_path)
    click.echo('The classification model evaluated the existence of a lightning to: {}'.format(str(lightning_detected).upper()))

    if lightning_detected:
        # Executing the whole detection pipeline on the image
        detection_lightning_image = LightningImage(imageio.imread(image_path, pilmode='L'))
        reference_lightning_image = LightningImage(imageio.imread(reference_path, pilmode='L'))
        detection(reference_lightning_image, detection_lightning_image, save)

    else:
        # If there was no lightning detected, then we can just end the whole process there
        click.echo('No lightning detected on the image. Nothing to localize')


@click.command()
@click.argument('json_path', type=str)
@click.argument('data_path')
@click.argument('save_path')
def all(json_path, data_path, save_path):

    with open(json_path, mode='r') as file:
        STRUCTURE = json.load(file)
    file_mask = STRUCTURE['filemask']
    for sequence in STRUCTURE['seqlist']:

        click.echo('\nPROCESSING SEQUENCE {}'.format(sequence['id']))

        # Using one reference picture for each picture in a sequence
        reference_file_name = file_mask % str(sequence['ref']).zfill(4)
        reference_file_path = os.path.join(data_path, reference_file_name)
        reference_image_array = imageio.imread(reference_file_path, pilmode='L')
        reference_image = LightningImage(reference_image_array)

        # Executing the detection script for each image in a sequence
        for image_id in sequence['images']:
            image_id = str(image_id)
            # Loading the image
            image_file_name = file_mask % str(image_id).zfill(4)
            image_file_path = os.path.join(data_path, image_file_name)
            image_array = imageio.imread(image_file_path, pilmode='L')
            image = LightningImage(image_array)

            lightning_detected = contains_lightning(image_file_path)
            if not lightning_detected:
                click.echo('NO LIGHTNING IN THE IMAGE. SKIPPING!')
                continue

            # Creating the save path for the figure
            image_save_path = os.path.join(save_path, image_file_name).replace('.jpg', '.svg')

            # Executing the script
            click.echo('PROCESSING IMAGE "{}"'.format(image_file_name))
            type_area_tuples = detection(
                reference_image,
                image,
                image_save_path
            )

            if type_area_tuples is None:
                type_area_tuples = []
            # Saving the calculated areas as additional properties to the files
            STRUCTURE['detection'][image_id] = {}
            STRUCTURE['detection'][image_id]['areas'] = []
            for lightning_type, area in type_area_tuples:
                # for each image there will be a list that contains Tuple(Tuple(int, int), Tuple(int, int), str)
                # objects, where the first element ist the tuple that contains the x index range, the second element
                # the tuple, that contains the y index range within the picture and the third element is the guessed
                # type of lightning, that is described by the area
                STRUCTURE['detection'][image_id]['areas'].append((area[0], area[1], lightning_type))

            # memory management
            del image.array
            del image

        # Saving the main structure after each sequence is finished
        with open(json_path, mode='w') as file:
            json.dump(STRUCTURE, file, indent=4, sort_keys=True)

# ####################
# SUPPORTING FUNCTIONS
# ####################

def detection(reference_lightning_image, detection_lightning_image, save_path, show=False):

    detection_mean = numpy.mean(detection_lightning_image.array)
    reference_mean = numpy.mean(reference_lightning_image.array)
    mean_difference = detection_mean - reference_mean

    # Calculating the difference of the two to get rid of the timestamps and most of the background
    difference_lightning_image = detection_lightning_image - reference_lightning_image  # type: LightingImage

    # The timestamps on the images are a white color, that has nothing to do with the actual lightning/scenery
    # Thus they need to be removed from the image, as to not influence the calculation of the max/mean gray scale value,
    # as it is done in the pre processing engine later on
    def remove_timestamp_mask(v, i, j):
        height = difference_lightning_image.height
        if height * 0.93 <= i or height * 0.05 >= i:
            return 0
        else:
            return v

    difference_lightning_image.transform_element_wise(remove_timestamp_mask)

    # A value a bit over the mean of the image will be used as static threshold
    static_threshold = numpy.mean(difference_lightning_image.array)
    # Using the pre processing engine to create a binary mask dynamically based on the difference image
    # TODO: Make the preprocessing also use a coefficient, that tells the spacial coverage of optical mass
    pre_processing_config = {
        'static_threshold': static_threshold,
        'threshold_function': lambda m, a: m - m * (0.43 + 0.0005 * (255 - m))
    }
    pre_processing_engine = SimpleLightningPreprocessingEngine(pre_processing_config)

    binary_lightning_image = pre_processing_engine(difference_lightning_image)

    # Running the Area segmentation engine on the final result of the pre processing,
    # which is essentially a binary picture
    # Where the lightning pixels have a value of 255 and the others a value of 0.
    # TODO: Sequencing function based on the floating average of the derivative of the sume function?
    def sequence_function(array):
        m = numpy.amax(array)
        factor = 0.02
        return CustomSequenceAreaSegmentationEngine.sequence_function_generator(
            lambda i, v, a: v >= m * factor,
            lambda i, v, a: v < m * factor
        )(array)

    # We first run the detection algorithm without validity checks to illustrate the working principle
    detection_config = {
        'sequence_function': sequence_function,
        'checking': True
    }
    segmentation_engine = CustomSequenceAreaSegmentationEngine(detection_config)
    areas = segmentation_engine(binary_lightning_image)

    # Now we group the areas together
    grouping_config = {
        'weight_function': lambda d, s: 0.0047 * d ** 2 + s ** (0.4),
        'threshold': 200
    }
    grouping_engine = SimpleAreaGroupingEngine(grouping_config)
    grouped_areas = grouping_engine(areas)
    # EXPERIMENTAL
    grouped_areas = grouping_engine(grouped_areas)

    if show:
        f, ax = plt.subplots(1, 1)
        ax.imshow(detection_lightning_image.array, cmap='gray')
        draw_areas(ax, grouped_areas)
        plt.show()
        plt.clf()
        # print(save_path)

    f, ax = plt.subplots(1, 1)
    ax.imshow(detection_lightning_image.array, cmap='gray')
    draw_areas(ax, grouped_areas)
    plt.savefig(save_path, dpi=600)
    plt.clf()
    plt.close()

    return grouped_areas


cli.add_command(all)
cli.add_command(box)


if __name__ == '__main__':
    cli()
