# raman-outlier-detector
ラマンスペクトルを指定すると、外れ値を持つサンプルを教えてくれる

## 使い方
```bash
poetry run python main.py run data/testdata.csv --n_rate 2.0 --row A --column col_1 --column col_2
```

これで、testdata.csvのA行のcol_1, col_2のデータに対して、外れ値を持つサンプル番号が表示される

```bash
poetry run python main.py testdata
```
これで、動作確認用のランダムなデータが生成される

## 原理
3シグマの外側には0.3%のデータしか含まれない。という正規分布の経験則に基づく外れ値検知の手法を用いる。
`n_rate`のパラメータは初期値が3で3シグマ法を実施でき、任意にパラメータを変更して外れ値を評価できる。

- (3シグマ法)[https://ja.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7%E5%89%87]
