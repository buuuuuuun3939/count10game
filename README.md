# count10 game

## 目的
- WASM を利用するための簡単なサンプルゲーム。

## build
```
$ docker build -t wasm-timer-export -f Dockerfile.timer .
$ docker run --rm -p 8000:8000 -v $(pwd)/out:/export wasm-timer-export
```
