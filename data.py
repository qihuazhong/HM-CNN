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


def read_read_counts(EID):
    path = "data/rc/" + EID + ".rc"
    rc = pd.read_table(path, header=None,
                       names=["chrom", "chromStart", "chromEnd", "gene_id", "score", "strand", "H3K4me3", "H3K4me1",
                              "H3K36me3", "H3K9me3", "H3K27me3"])
    rc = rc.loc[:, ["gene_id", "H3K4me3", "H3K4me1", "H3K36me3", "H3K9me3", "H3K27me3"]]
    rc['EID'] = EID

    windows = [w for w in range(1, 1 + n_windows)] * int(len(rc) / n_windows)
    rc = rc.join(pd.DataFrame(windows, columns=['window']))

    return rc


def expr_to_binary(path="data/57epigenomes.RPKM.pc"):
    exprs = pd.read_table(path, index_col=False)

    for c in range(1, exprs.shape[1]):
        median = exprs.iloc[:, c].median()
        exprs.iloc[:, c] = [1 if (i > median) else 0 for i in exprs.iloc[:, c]]

    # melt(reshape) expressions
    exprs = exprs.melt(id_vars='gene_id', var_name='EID', value_name='expr')

    return exprs


def generate_featurs_and_labels(EIDs):
    """
    EIDs: a list of EIDs

    return: training set X, and label Y
    """

    # Get expression in binary form
    exprs_binary = expr_to_binary()

    rc = pd.DataFrame()
    for id in EIDs:
        # get read counts by EID
        rc = pd.concat([read_read_counts(id), rc])

    # append labels
    joined_table = rc.join(exprs_binary.set_index(['EID', 'gene_id']), on=['EID', 'gene_id'])
    assert joined_table["expr"].isna().any() == False

    raw_labels = joined_table['expr'].values
    y = []
    for i in range(0, len(raw_labels), n_windows):
        y.append(raw_labels[i])
    y = array(y)

    # parse features to proper input shape
    values = joined_table.set_index(['EID', 'gene_id', 'window']).values
    input_values = values[:, 0:n_features]

    # shape : [#sample, #window, #features]
    x = input_values.reshape(len(y), n_windows, n_features)

    return x, y

