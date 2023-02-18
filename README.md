# ImageDiff

GoogleCloudVisionAPIを利用した画像内テキストの比較を行うWebアプリケーション

## 機能
1. 比較対象を撮影し，撮影画像内のテキストを抽出する
2. 抽出されたテキストデータを比較し，一致した文字列を提示する
3. 提示された一致文字列に対して，ユーザーが設定したコメントを付与する

## 使い方
https://sigmawind.pythonanywhere.com/imagediff/

## 環境
Python
Django
MySQL

## 利用方法
1. settings_sample.pyをsettings.pyにリネームして
   「SECRET_KEY」および「DATABASES」を設定
2. GoogleCloudVisionAPIを利用しているためGoogleCloudPlatformにて
   プロジェクトを作成し，サービスアカウントキーをダウンロードする
3. ダウンロードしたサービスアカウントキー(jsonファイル)へのパスを
   wsgi.pyに入力

## pip list
| Package                          | Version   |
| -------------------------------- | --------- |
| asgiref                          | 3.3.0     |
| astroid                          | 2.4.2     |
| cachetools                       | 4.1.1     |
| certifi                          | 2020.6.20 |
| chardet                          | 3.0.4     |
| colorama                         | 0.4.4     |
| Django                           | 3.1.3     |
| django-bootstrap-datepicker-plus | 3.0.5     |
| django-environ                   | 0.4.5     |
| django-ipware                    | 3.0.2     |
| django-structlog                 | 2.1.0     |
| django-user-sessions             | 1.7.1     |
| django-widget-tweaks             | 1.4.8     |
| dnspython                        | 2.0.0     |
| google-api-core                  | 1.23.0    |
| google-auth                      | 1.23.0    |
| google-cloud-vision              | 2.0.0     |
| googleapis-common-protos         | 1.52.0    |
| grpcio                           | 1.33.2    |
| idna                             | 2.10      |
| isort                            | 5.6.4     |
| lazy-object-proxy                | 1.4.3     |
| libcst                           | 0.3.13    |
| mccabe                           | 0.6.1     |
| mojimoji                         | 0.0.11    |
| mypy-extensions                  | 0.4.3     |
| mysqlclient                      | 2.0.1     |
| Pillow                           | 8.0.1     |
| pip                              | 20.2.4    |
| proto-plus                       | 1.11.0    |
| protobuf                         | 3.13.0    |
| pyasn1                           | 0.4.8     |
| pyasn1-modules                   | 0.2.8     |
| pylint                           | 2.6.0     |
| python-dateutil                  | 2.8.1     |
| pytz                             | 2020.4    |
| PyYAML                           | 5.3.1     |
| requests                         | 2.24.0    |
| rsa                              | 4.6       |
| setuptools                       | 49.2.1    |
| six                              | 1.15.0    |
| sqlparse                         | 0.4.1     |
| stripe                           | 2.55.0    |
| structlog                        | 20.1.0    |
| toml                             | 0.10.2    |
| typing-extensions                | 3.7.4.3   |
| typing-inspect                   | 0.6.0     |
| urllib3                          | 1.25.11   |
| wrapt                            | 1.12.1    |
