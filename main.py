import pandas as pd
import numpy as np
import click


@click.group()
def cmd():
    pass


def is_in_sigma(value, mean, std, sigma):
    return mean - sigma * std <= value <= mean + sigma * std


@cmd.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--row", "-r", multiple=True, type=str, default=[])
@click.option("--col", "-c", multiple=True, type=str, default=[])
@click.option("--n_rate", "-n", type=float, default=3.0, show_default=True)
@click.option("--robust", "-rb", is_flag=True, default=False, show_default=True)
@click.option("--threshold", "-t", type=float, default=0.5, help="Threshold for outlier sample rate", show_default=True)
def run(path, row, col, n_rate, robust, threshold):
    if len(set(col)) != len(col):
        click.echo("Error: Duplicate column names")

    df = pd.read_csv(path, index_col=0, header=0)
    if row:
        df = df.loc[row, :]

    if col:
        df = df.loc[:, col]

    click.echo(df)
    if robust:
        median = df.median(axis=0)
        # median absolute deviation
        mad = (df - median).abs().median(axis=0)

        # rename
        mean = median
        std = mad
    else:
        mean = df.mean(axis=0)
        std = df.std(axis=0)

    for group, data in df.groupby(level=0):
        click.echo(f"Group: {group}'s Outlier")
        outlier_samples = 0
        for i, (index, row) in enumerate(data.iterrows()):
            counter = 0
            for (colname, value) in row.items():

                # σ法を用いた外れ値の評価
                if not is_in_sigma(value, mean[colname], std[colname], n_rate):
                    counter += 1

            # if the number of outliers is greater than the threshold, print the sample id
            error_rate = counter / len(data.columns)
            if error_rate >= threshold:
                click.echo(f"Sample ID:\t{i}")
                outlier_samples += 1
        outlier_samples_rate = outlier_samples / len(data)
        click.echo(f"Outlier Rate:\t{outlier_samples_rate:.2f}%, {outlier_samples}/{len(data)}")
        print()


# 動作確認用のテストデータの生成
@cmd.command()
@click.option("--path", "-o", type=click.Path(), default="data/testdata.csv")
@click.option("--row", "-r", type=int, default=100)
@click.option("--col", "-c", type=int, default=10)
def testdata(path, row, col):
    df = pd.DataFrame(
        np.random.rand(row, col),
        columns=[f"col_{i}" for i in range(col)],
        index=np.random.choice(["A", "B", "C"], row, p=[0.5, 0.3, 0.2])
    )
    df = df.sort_index()
    click.echo(df)
    df.to_csv(path)
    click.echo(f"Saved to {path}")


def main():
    cmd()


if __name__ == "__main__":
    main()
