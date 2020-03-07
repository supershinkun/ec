ec風のサイトを作りました。

dockerでmysqlを起動させます。
requirements.txtに記載されているモジュールをpip installしてください。

・python manage.py migrate

DBマイグレート後に下記コマンドでデータをロードしてください。
・python manage.py loaddata first_data.json
・python manage.py loaddata second_data.json
・python manage.py loaddata third_data.json

・python manage.py runserver
