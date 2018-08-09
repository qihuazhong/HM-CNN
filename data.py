import pandas as pd
from numpy import array
n_features = 5
n_windows = 100
bin_size = 100


def read_toy_data(path="data/toy/train.csv"):
    """

    :return: input x and labels y ready for
    """

    # Read toy data from the DeepChrome repo

    col_names = ['GeneID', 'Window', 'Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5', 'GeneExpression']

    df = pd.read_csv(path, header=None, names=col_names, dtype={'GeneID': str})

    # parse GeneExpression to labels (y)
    raw_labels = df['GeneExpression'].values
    y = []
    for i in range(0, len(raw_labels), n_windows):
        y.append(raw_labels[i])
    y = array(y)

    # parse features to input
    values = df.values
    input_values = values[:, 2:7]

    # shape : [#sample, #window, #features]
    x = input_values.reshape(len(y), n_windows, n_features)

    return x, y


# features, labels = read_toy_data()
# print(features[0])
# print(features.shape)
