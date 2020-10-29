# ひとこと掲示板の作成
今回はひとこと掲示板の作成について記載していきたいと思います。

# 準備すること

#### ①apache2のモジュール有効にする

```

$ sudo a2enmod

$ sudo service apache2 restart

```

#### ②public_htmlフォルダを作る

```

$ mkdir public_html

```

#### ③bbs.pyを①の中に挿入

```

$ touch bbs.py

```

#### ④pip3をインストールした後にmysqlclientをインストール

```

$ sudo python3 get-pip.py
 
$ pip3 install mysqlclient

```
 
#### ⑤userdir.confのOptionsにExecCGIを追加する

```

Options ExecCGI MultiViews Indexes

```

#### ⑥CGIモジュールを有効にする

```

$ sudo a2enmod cgi

$ sudo systemctl restart apache2

```

#### ⑦public_htmlに.htaccessを作成

```

AddHandler cgi-script.py

```

#### ⑧public_htmlに.envを作成し下記を記述

```

bbs_db_host=ホスト名

bbs_db_user=ユーザー名

bbs_db_pass=パスワード

bbs_db_name=db名

```

# 使い方

#### ブラウザで以下のアドレスを入力する

```

http://[ipアドレス]/~username/bbs.py

```

# 環境
```

Ubuntu Ver 20.04
MySQL　Ver 8.0.22
Python Ver 3.8.5
 
```

※それ以外は試してません

# 作成者
* SEKI YUTA
