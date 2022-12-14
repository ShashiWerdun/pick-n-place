from fastai.vision import *
import os

TRAINING_DATASET_PATH = '../archive/256_ObjectCategories'

def train_cnn_classifier():

    # get transforms
    tfms = get_transforms(do_flip=False, flip_vert=False, max_rotate=0, max_lighting=0.3, max_zoom=1.01)

    # load data
    data = ImageDataBunch.from_folder(path, train=".", 
                                  valid_pct=0.2,
                                  ds_tfms=tfms,
                                  size=128,bs=64, 
                                  num_workers=0).normalize(imagenet_stats)

    # model architecture
    arch = models.resnet50

    # the learner
    learner = cnn_learner(data, arch, metrics=accuracy, model_dir='./save-model')

    # get optimal learning rate
    learner.lr_find()
    learner.recorder.plot()

    # 
    lr = 1e-01/2

    # train the model
    learner.fit_one_cycle(5, slice(lr))

    learner.save('stage1')
    learner.freeze()

    # export model
    learner.export('./export-model/cnn-1.pkl')