from ae import Autoencoder
from keras.datasets import mnist
import tensorflow as tf

LEARNING_RATE = 0.0005
BATCH_SIZE = 32
EPOCHS = 20

# Check if GPU is available
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    print("GPU is available")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)  # Prevents TensorFlow from allocating all GPU memory at once
else:
    print("GPU is not available, training will use the CPU")

def load_mnist():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.astype("float32")/255 #normalize it to between 0 and 1
    x_train = x_train.reshape(x_train.shape + (1,))
    x_test = x_test.astype("float32")/255 #normalize it to between 0 and 1
    x_test = x_test.reshape(x_test.shape + (1,))

    return x_train, y_train, x_test, y_test

def train(x_train, learning_rate, batch_size, epochs):
    autoencoder = Autoencoder(
        input_shape=(28,28,1),
        conv_filters=(32,64,64,64),
        conv_kernels=(3, 3, 3, 3),
        conv_strides=(1, 2, 2, 1),
        latent_space_dim=2
    )
    autoencoder.summary()
    autoencoder.compile(learning_rate)
    autoencoder.train(x_train, batch_size, epochs)
    return autoencoder

if __name__ == "__main__":
    x_train, _, _, _ = load_mnist()
    autoencoder = train(x_train[:500], LEARNING_RATE, BATCH_SIZE, EPOCHS)
    autoencoder.save("model")
    autoencoder2 = Autoencoder.load("model")