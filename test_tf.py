import tensorflow as tf

print("This is a test, Version: ", tf.__version__)
print("GPU Available: ", tf.config.list_physical_devices('GPU'))

mnist = tf.keras.datasets.mnist
(x_train,y_train),(x_test, y_test) = mnist.load_data()
print("Tensor Flow is working")


