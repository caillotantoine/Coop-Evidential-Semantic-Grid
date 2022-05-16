import argparse

# Manage the arguments
argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument(
    '--algo',
    metavar='A',
    default='Dempster',
    help='Choose between Dempster, Conjunctive and Disjunctive (default Dempster).')
argparser.add_argument(
    '--mean',
    metavar='M',
    type=bool,
    default=False,
    help='Compute the mean (default False).')
argparser.add_argument(
    '--gui',
    metavar='G',
    type=bool,
    default=True,
    help='Show the GUI (default False).')
argparser.add_argument(
    '--save_img',
    type=bool,
    default=False,
    help='Save maps as images (default False).')
argparser.add_argument(
    '--loopback_evid',
    type=bool,
    default=False,
    help='Loop back the t-1 evidential map as an entry of the agents (default False).')
argparser.add_argument(
    '--start',
    metavar='S',
    type=int,
    default=10, #10
    help='Starting point in the dataset (default 10).')
argparser.add_argument(
    '--pdilate',
    type=int,
    default=-1, #-1
    help='Pedestrian Dilation Factor. -1: Off, Choose a value between 0 and 5. (default -1)')
argparser.add_argument(
    '--cooplvl',
    type=int,
    default=2, #2
    help='Number of observation to be a valid measure. -1: All, Choose a value between 0 and N users. (default 2)')
argparser.add_argument(
    '--gdilate',
    type=int,
    default=-1, #-1
    help='Dilation Factor for every object at mask level. -1: Off, Choose a value between 0 and 5. (default -1)')
argparser.add_argument(
    '--end',
    metavar='E',
    type=int,
    default=500,
    help='Ending point in the dataset (default 500).')
argparser.add_argument(
    '--dataset_path',
    default='/home/caillot/Documents/Datasets/CARLA_Dataset_original', # _intersec_dense _original _B
    help='Path of the dataset.')
argparser.add_argument(
    '--save_path',
    default='/home/caillot/Documents/output_algo/',
    help='Saving path.')

argparser.add_argument(
    '--json_path',
    default='./Sources/configs/test_config/full_NN_1.json',
    help='Configuration json file path.')