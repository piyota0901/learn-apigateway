from ariadne.asgi import GraphQL

from Web.schema import schema

server = GraphQL(schema, debug=True)