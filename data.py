import pandas as pd

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

    # parse features to input
    values = df.values
    input_values = values[:, 2:7]

    # shape : [#sample, #window, #feature]
    x = input_values.reshape(len(y), n_windows, n_features)

    return x, y


print(read_toy_data())
