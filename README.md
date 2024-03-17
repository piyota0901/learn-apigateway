
## Alembic 

[Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

## Microservice
[参考](https://github.com/abunuwas/microservice-apis)

`marshalling`
インメモリのデータ構造をネットワーク経由での送信やストレージに適したフォーマットに変換するプロセスのこと  
Web APIでのマーシャリングでは、オブジェクトの属性を明示的にマッピングした上で、オブジェクトをXMLやJSONの
ようなコンテントタイプにシリアライズできるデータ構造に変換する

## Open API
- [Open API はじめました](https://zenn.dev/peraichi_blog/articles/01ges56ak79g2rket9wm27w9pc)
- [書き方](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md)
- [swagger editor](https://github.com/swagger-api/swagger-editor?tab=readme-ov-file#docker)
- モックサーバー
    - [Prism](https://github.com/stoplightio/prism)
    - [Docker](https://docs.stoplight.io/docs/prism/f51bcc80a02db-installation#docker)


## 勉強用
- [CodeZin | マイクロサービス](https://codezine.jp/article/detail/11305)

### Repositryパターン

実装上の注意！
制約: `リポジトリによって事項される操作をリポジトリによってコミットすることはできない`

具体例

注文オブジェクトをリポジトリに追加すると、リポジトリはその注文をデータベースセッションに追加するが
変更内容のコミットはしない。  
変更をコミットする責任は`OrdersService`（API層）のコンシューマにある。

リポジトリ内でコミットできない理由
- リポジトリはデータのインメモリリスト表現のように機能するため、データベースセッションやトランザクションのような概念はない
- データベーストランザクションを実行するのに適した場所ではない
    - リポジトリが呼び出されるコンテキストにより、トランザクションを実行するのに適したコンテキストが提供される
    - 多くの場合、アプリケーションは1つ以上のリポジトリやほかのサービスの呼び出しを伴う複数の操作を実行する。
    例. 支払い処理の場合に、支払いサービス・厨房サービスとのやり取りが発生し、これらすべての操作がまとめて成功・失敗
    しなければならず、それに応じてAPI層がコミットorロールバックを実行しなければならない。
    - 実行コンテキストの単位として、すべての変更がコミットまたはロールバックされるようにする責任はAPI層にある。


リポジトリの返却するオブジェクト

多くの場合は、データベースモデル（`orders/repository/models.py`で定義されているクラス）のインスタンスを返す。  
今回は、ビジネス層のドメインの注文を表すオブジェクトを返す。理由は、データベースモデルのインスタンスを返すのが良くないのは  
ビジネス層をデータ層から切り離すというリポジトリの目的に反しているから。永続化ストレージテクノロジーやORMフレームワークを  
変更する場合に、`orders/repository/models.py`のクラスは使えなくなる（`sqlalchemy`固有の実装のため）。