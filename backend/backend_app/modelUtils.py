from tensorflow.keras.optimizers import Adam
from tensorflow.keras import models
from tensorflow import keras
import tensorflow as tf

# define iou or jaccard loss function
def iou_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    # print('iou_loss ->', y_true.shape, y_pred.shape)
    y_true = tf.reshape(y_true, [-1])
    y_pred = tf.reshape(y_pred, [-1])
    # print('iou_loss(1) ->', y_true.shape, y_pred.shape)
    intersection = tf.reduce_sum(y_true * y_pred)
    score = (intersection + 1.) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) - intersection + 1.)
    return 1 - score

# combine bce loss and iou loss
def iou_bce_loss(y_true, y_pred):
    # print('iou_bce_loss ->', y_true.shape, y_pred.shape)
    return 0.5 * keras.losses.binary_crossentropy(y_true, y_pred) + 0.5 * iou_loss(y_true, y_pred)

# mean iou as a metric
def mean_iou(y_true, y_pred):
    # print('mean_iou ->', y_true.shape, y_pred.shape)
    y_pred = tf.round(y_pred)
    intersect = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    union = tf.reduce_sum(y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    smooth = tf.ones(tf.shape(intersect))
    return tf.reduce_mean((intersect + smooth) / (union - intersect + smooth))

def __load_model(saved_model):
    optimizer = Adam(learning_rate=1e-4, beta_1=0.9,
                     beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model = keras.models.load_model(saved_model, compile=False)
    model.compile(optimizer=optimizer, loss=iou_bce_loss, metrics=['accuracy', mean_iou])
    return model