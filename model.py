from data import read_toy_data
from keras import losses
from keras.models import Model, Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Dropout, Flatten


# Design Network
def build_model(n_filters=50, kernel_size=10, pool_size=5):
    n_features = 5
    n_windows = 100

    model = Sequential()
    model.add(
        Conv1D(filters=n_filters, kernel_size=(kernel_size), input_shape=(n_windows, n_features), activation='relu'))
    model.add(MaxPooling1D(pool_size=pool_size))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(625, activation='relu', name='Dense1'))
    model.add(Dense(125, activation='relu', name='Dense2'))
    model.add(Dense(1, activation='sigmoid', name='Dense3'))
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model


def train(model, x_train, y_train, x_valid, y_valid, epochs):
    # fit network
    history = model.fit(x_train, y_train, epochs=epochs,
                        validation_data=(x_valid, y_valid))

    model.save('my_model.h5')