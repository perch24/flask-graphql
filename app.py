from database.base import db_session
from flask import Flask, request
from flask_graphql import GraphQLView
from functools import wraps
from schema import schema

app = Flask(__name__)

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        session = request.headers.get('AUTH_TOKEN', '')
        print("Foo Bar Baz")
        # Could implement some authentication here...
        return fn(*args, **kwargs)
    return wrapper

def graphql_view():
    view = GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        context={
            'session': db_session,
        }
    )
    return auth_required(view)

app.add_url_rule(
    '/graphql',
    view_func=graphql_view())


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(threaded=True, debug=True)