from data import *
from model import *
from sklearn.utils import shuffle


X, Y = generate_featurs_and_labels(['E003', 'E004'])
X_shuffled, Y_shuffled = shuffle(X, Y)

print(X.shape)
print(Y.shape)


model = build_model()
print(model.summary())

split_trainval = int(len(Y) / 3 * 2)


history = train(model, X_shuffled[:split_trainval, :, :], Y_shuffled[:split_trainval], batch_size=256, epochs=30)


# plot train history
import matplotlib.pyplot as plt

# summarize history for accuracy
plt.subplot(1, 3, 1)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')

# summarize history for auc
plt.subplot(1, 3, 2)
plt.plot(history.history['auc_roc'])
plt.plot(history.history['val_auc_roc'])
plt.title('model auc')
plt.ylabel('auc')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')

# summarize history for loss
plt.subplot(1, 3, 3)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
