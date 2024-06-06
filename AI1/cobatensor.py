import tensorflow as tf

# Defining two constant tensors
a = tf.constant(15)
b = tf.constant(3)

# Performing addition using TensorFlow operation
hasil = tf.divide(a, b)

# Running the operation
output = hasil.numpy()
print("Hasil pembagian:", output)
