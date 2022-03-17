# Tweet取得 API

指定したハッシュタグのツイートが取得できるAPIです。

オープンデータAPIプロジェクトのフロントエンドで使用するために作成しました。



## API 仕様
- https://opendata.yamanashi.dev/api/tweets-api/docs を参照

## ライセンス
- 本ソフトウェアは、[MITライセンス](./LICENSE.txt)の元提供されています。

## 実行例
``` bash
curl -X 'GET' \
  'https://opendata.yamanashi.dev/api/tweets-api/富士山?max_result=10&has_image=true' \
  -H 'accept: application/json'
```

``` bash
[
  [
    {
      "attachments": {
        "media_keys": [
          "x_xxxxxxxxxxxxxxxxx"
        ]
      },
      "id": xxxxxxxxxxxxxxxxxxxx,
      "text": "今日はは富士山🗻が綺麗に見える!(^^)! #富士山"
    },
    {
      "media": [
        {
          "media_key": "x_xxxxxxxxxxxxxxxxx",
          "type": "photo",
          "url": "https://pbs.twimg.com/media/xxxxxxxxxxxxx.jpg"
        }
      ]
    },
    [],
    {}
  ],
  [
    {
      ...
    },
    ...
  ]
]
```

## 開発者向け情報

### 環境構築の手順

- 必要となるPythonバージョン: 3.8以上

**起動方法**

起動時に下記の環境変数にTwitter APIの認証情報(トークン)を登録しておきます.

- bearer_token
- consumer_key
- consumer_secret
- access_token
- access_token_secret

Twitter APIの詳細はこちら
https://developer.twitter.com/en/docs/twitter-api

起動

``` bash
$ pip install -r requirements.txt
$ uvicorn app.main:app --reload
```

