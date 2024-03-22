## 環境セットアップ

### データベースの初期化

`sqlite`の想定。

1. `alembic`でmigrationを実行する
    ```bash
    $ cd orders
    $ poetry run alembic init migrations
    $ poetry run alembic upgrade heads
    ```

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

### Unit of Workパターン 

トランザクションの原子性を保証するデザインパターン  
すべてのトランザクションがまとめてコミットされるか、トランザクションが1つでも失敗した場合は  
すべてのトランザクションがロールバックされるかのどちらかになる

SQLAlcheyｍの`Session`オブジェクトは、データベーストランザクションに対して`Unit of Workパターン`をすでに実装している（[Session Basic](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#:~:text=This%20is%20known%20as%20the%20unit%20of%20work%20pattern.)）。


### SQLAlchemy
- `mapped_column()`は、`nullable=True`としないとデフォルトで`False`が設定されてしまう

#### カスケード設定

`delete-orphan`とする。理由は以下。
- 注文が削除されれば、注文のアイテムも削除される  
- 注文のアイテムが単独で存在することはない


`delete`と`delete-orphan`がある。  
`relationship()`は、親オブジェクトに記載する。

- `delete`: 親オブジェクトが削除されたときのみ子オブジェクトが削除される
- `delete-orphan`: 親オブジェクトが削除されたとき + 親オブジェクトから関連付けを削除されたときにも削除される
- `save-update`: 親オブジェクトがSessionに加えられた場合、`relationship`で関連するオブジェクトも同じSessionに入れられる。
- `backref`: 双方向のリレーションを自動的に結んでくれる
- `back_populates`: 双方向リレーションを手動で設定する必要がある ※populate: 投入する
    ```python
    class Event(Base):
    __tablename__ = ‘event’
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    tickets = relationship("Ticket",back_populates="event")
    
    class Ticket(Base):
        __tablename__ = ‘ticket’
        id = Column(Integer,primary_key=True)
        title = Column(String(255))
        value = Column(Integer)
        event_id = Column(Integer,ForeignKey(‘event.id’))
        event = relationship("Event",back_populates="tickets")

    event = Event(title="test")
    ticket = Ticket(title="test_ticket",value=5000)
    # ↓ 手動でeventのticketsプロパティに設定する必要がある
    event.tickets = [ticket] event.tickets #Ticket Objects
    ticket.event #Event Object
    ```
- `backref`, `back_populates`のどちらも指定しない場合、トランザクション内で紐づかない
    - トランザクション内
        ```python
        event.tickets = [ticket] event.tickets #Ticket Objects
        ticket.event #None ← 紐づいていない
        ```
    - トランザクション後
        ```python
        event = self.session.query(Event).filter(Event.id==1).one()
        ticket = self.session.query(Ticket).filter(Ticket.id==1).one()
        event.tickets #Ticket Objects
        ticket.event #Event Object  ← 紐づいている
        ```

## GraphQL

GraphQLは単一のエンドポイントを持つ。操作（Query / Mutation）にかかわらず一定。（例. http://xxx.xxx.xxx/graphql）  
リクエスト送信は、GETまたはPOSTメソッド。  
- GET: URLクエリパラメータにクエリを追加
- POST: リクエストペイロードにクエリを追加

### Mockサーバー
[graphql-faker | Usage Docker](https://github.com/graphql-kit/graphql-faker?tab=readme-ov-file#usage-with-docker)

## Kong

## JWT Plugin

[Kong | JWT Plugin](https://docs.konghq.com/hub/kong-inc/jwt/)

[JWT Debugger](https://jwt.io/#:~:text=SEE%20JWT%20LIBRARIES-,Debugger,-Warning%3A%20JWTs)
    - 参考: https://qiita.com/ike_dai/items/5a14ced48c6ec7d80d70
    - `secret base64 encoded`はチェックしない。エンコードされた値ではないため
    - 参考: https://future-architect.github.io/articles/20221006a/

## APIモックサーバー

[httpbin.org](https://httpbin.org/)というサイトがある。  
[httpbun.com](https://httpbun.com)というサイトもある。`httpbin`の改良。


## OAuth

### 許可フロー

- 認可コードフロー
    - バックエンドでレンダリングされる従来のWebアプリケーションなど、
    コードが公開されないアプリケーションにのみ適している。
    - OAuth2.1では、PKCEとの組み合わせで使うことが推奨されている。
- PKCEフロー
    - モバイルアプリやSPAなど、コードが公開されるアプリケーションを保護するために設計された認可コードフロー。
    - セキュリティ上の利点があるため、サーバー側のアプリケーションでも推奨される。
- クライアントクレデンシャルフロー
    - サーバー間の通信が目的
    - セキュアなネットワークを介してマイクロサービス間の通信を実現するのに適している
- 更新トークンフロー
    - アクセストークンの期限が切れた後も、通信できる必要があるため、
    新しいトークンを取得するために更新トークンフローが使われる。

OAuthのフロー  
クライアントアプリケーションがAPIへのアクセスを認可するために用いる戦略。  
ベストプラクティスは[OAuth 2.0 Security Best Current Practice](https://oauth.net/2/oauth-best-practice/)で説明されている。  