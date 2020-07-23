#
# This short example is based on the fastai GitHub Repository of vision examples
# https://github.com/fastai/fastai/blob/master/examples/vision.ipynb
# Modified here to show mlflow.fastai.autolog() capabilities
#
import argparse
from fastai.vision import untar_data, ImageDataBunch, models, URLs, imagenet_stats, rand_pad, cnn_learner, accuracy
import mlflow.fastai

def parse_args():
    parser = argparse.ArgumentParser(description='Fastai example')
    parser.add_argument('--lr', type=float, default=0.01,
                       help='learning rate to update step size at each step (default: 0.01)')
    parser.add_argument('--epochs', type=int, default=5,
                       help='number of epochs (default: 5). Note it takes about 1 min per epoch')
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()

    # Download and untar the MNIST data set
    path = untar_data(URLs.MNIST_SAMPLE)

    # Prepare, transform, and normalize the data
    data = ImageDataBunch.from_folder(path, ds_tfms=(rand_pad(2, 28), []), bs=64)
    data.normalize(imagenet_stats)

    # Train and fit the Learner model
    learn = cnn_learner(data, models.resnet18, metrics=accuracy)

    # Enable auto logging
    mlflow.fastai.autolog()

    # Start MLflow session
    with mlflow.start_run():
        # Train and fit with default or supplied command line arguments
        learn.fit(args.epochs, args.lr)

if __name__ == '__main__':
    main()
