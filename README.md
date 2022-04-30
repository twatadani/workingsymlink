# workingsymlink
create symbolic links for working directory

---

## WorkingSymlink

Python等のスクリプトをソースディレクトリ以外のディレクトリで実行するためにシンボリックリンクをワーキングディレクトリに作成するスクリプト。

---

## Usage

```sh
$ cd working_directory
$ python workingsymlink.py source_directory
```

---

## Config

実行するワーキングディレクトリ内に`workingsymlink_config.json`というコンフィグ用のJSONファイルを作成しておく。  

このコンフィグファイルの書き方は

```json
{
    "SymLink_EXT": [ ".py", ".env" ],
    "EXCLUDE": [ ".git" ],
    "ABSPATH": false
}
```

のようにする。"SymLink_EXT"はシンボリックリンクを作成するファイルの拡張子のリスト。
"EXCLUDE"は明示的にシンボリックリンク作成の対象としないファイルやディレクトリのリストを書いておく。  
"ABSPAH"はシンボリックリンクを絶対パスで作成するか相対パスで作成するか。trueの場合絶対パス、falseの場合相対パス。
