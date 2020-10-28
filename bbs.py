#!/usr/bin/env python3

#日本語でもエラーが出ないようにする
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#CGIとして実行した際のフォーム情報を取り出す
import cgi
form_data = cgi.FieldStorage(keep_blank_values = True)

# MySQLデーターベース接続用ライブラリ
import MySQLdb
con = None
cur = None

#設定情報を外部設定ファイル（.env）から読み取るライブラリ
#（今回はデータベースに接続するための各情報を設定ファイルから読み取るために使用）
import os
from pathlib import Path
env_path = Path('.') / '.env'
from dotenv import load_dotenv
load_dotenv( dotenv_path = env_path, verbose = True )

#トップ画面のHTMLを出力する関数

def print_html():
    # html 開始
    print( '<!DOCTYPE html>' )
    print( '<html>' )

    # head 出力
    print( '<head>' )
    print( '<meta charset="UTF-8">' )
    print( '</head>' )

    # body 開始
    print( '<body>' )
    print( '<p>ひとこと掲示板</p>' )

    # 書き込みフォームを出力
    print( '<form action="" method="POST">' )
    print( '<input type="hidden" name="method_type" value="tweet">' )
    print( '<input type="text" name="poster_name" value=""placholder="なまえ">' )
    print( '<br>' )
    print( '<textarea name="body_text" value"" placeholder="本文"></textarea>' )
    print( '<input type="submit" value="投稿">' )
    print( '</form>' )

    #罫線を出力
    print( '<hr>' )

    # 書き込みの一覧を取得するSQL文を作成
    sql = "select * from posts"

    # SQLを実行
    cur.execute( sql )

    # 取得した書き込みの一覧の全レコードを取り出し
    rows = cur.fetchall()

    # 全レコードから1レコードずつ取り出すループ処理
    for row in rows:
        print( '<div class="meta">' )
        print( '<span class="id">' + str(row[ 'id' ]) + '</span>' )
        print( '<span class="name">' + str(row[ 'name' ]) + '</span>' )
        print( '<span class="date">' + str(row[ 'created_at' ]) + '</span>' )
        print( '</div>' )
        print( '<div class="message"><span>' + str(row[ 'body' ]) + '</span></div>' )

    # body 閉じ
    print( '</body>' )

    # html 閉じ
    print( '</html>' )

# フォーム経由のアクセスを処理する関数
def proceed_methods():

    # フォームの種類を取得（今のところ書き込みのみ）
    method = form_data[ 'method_type' ].value

    # tweet （書き込み）だったら
    if( method == 'tweet' ):

        # 名前を取り出し
        poster_name = form_data[ 'poster_name' ].value

        # 投稿内容を取り出し
        body_text = form_data[ 'body_text' ].value

        # 投稿をデーターべースに書き込むSQL文を作成
        sql = 'insert into posts ( name, body ) values ( %s, %s )'

        # 取り出した名前と投稿内容をセットしてSQLを実行
        cur.execute( sql, ( poster_name, body_text ) )
        con.commit()

        # 処理に成功したらトップ画面に自動移するページを出力
        print( '<!DOCTYPE html>' )
        print( '<html>' )
        print( ' <head>' )
        print( '   <meta http-equiv="refresh" content="5; url=./bbs.py">' )
        print( ' </head>' )
        print( '      <body>')
        print( '          処理が成功しました。５秒後に元のページに戻ります。' )
        print( '      </body>' )
        print( '</html>' )

# メイン処理を実行する関数
def main():
    # CGIとして実行するためのおまじない
        print( 'Content-Type: text/html; charset=utf-8' )
        print( '' )

        #ここでデーターベースに接続しておく
        global con, cur
        try:
            con = MySQLdb.connect(
                    host = os.environ.get( 'bbs_db_host' ),
                    user = str(os.environ.get( 'bbs_db_user' )),
                    passwd = str(os.environ.get( 'bbs_db_pass')),
                    db = str(os.environ.get( 'bbs_db_name')),
                    use_unicode = True,
                    charset = 'utf8'
                    )

        except MySQLdb.Error as e:
            print( 'データベース接続に失敗しました。' )
            print( e )
            #データーベースに接続できなかった場合はここで処理終了
            exit()


        cur = con.cursor( MySQLdb.cursors.DictCursor )


        #フォーム経由のアクセスか判定
        if( 'method_type' in form_data ):
            #フォーム経由のアクセスである場合はフォームの種類に従って処理を実行
                proceed_methods()
        else:
            #フォーム経由のアクセスではない場合は通常トップ画面を表示
                print_html()

        #一通りの処理が完了した最後にデーターベースを切断しておく
        cur.close()
        con.close()

if __name__ == "__main__":
    # main() を実行
        main()

