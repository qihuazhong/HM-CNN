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


def read_read_counts(path="data/E003.rc"):
    rc = pd.read_table(path, header=None, names=["chrom", "chromStart", "chromEnd", "name", "score", "strand", "H3K4me3", "H3K4me1", "H3K36me3", "H3K9me3", "H3K27me3"])
    rc = rc.loc[:, ["name", "H3K4me3", "H3K4me1", "H3K36me3", "H3K9me3", "H3K27me3"]]

    return rc


def generate_labels(path="data/57epigenomes.RPKM.pc"):
    exprs = pd.read_table(path, index_col=False)

    for c in range(1, exprs.shape[1]):
        median = exprs.iloc[:, c].median()
        exprs.iloc[:, c] = [1 if (i > median) else 0 for i in exprs.iloc[:, c]]

    return exprs


def generate_set(rc, exprs):
    joined_table = rc.set_index("name").join(exprs.set_index("gene_id")['E003'])
    assert joined_table['E003'].isna().any() == False

    raw_labels = joined_table['E003'].values
    y = []
    for i in range(0, len(raw_labels), n_windows):
        y.append(raw_labels[i])

    y = array(y)

    # parse features to input
    values = joined_table.values
    input_values = values[:, 0:5]

    # shape : [#sample, #window, #features]
    x = input_values.reshape(len(y), n_windows, n_features)

    return x, y

