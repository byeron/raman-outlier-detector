# raman-outlier-detector
ラマンスペクトルを指定すると、外れ値を持つサンプルを教えてくれる

## 使い方
```bash
poetry run python main.py run data/testdata.csv --sigma 2.0 --row A --column col_1 --column col_2
```

これで、testdata.csvのA行のcol_1, col_2のデータに対して、外れ値を持つサンプル番号が表示される

