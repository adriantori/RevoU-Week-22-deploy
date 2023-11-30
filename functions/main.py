from app import app
from firebase_functions import https_fn


@https_fn.on_request(max_instances=1)
def adriantori(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()


if __name__ == "__main__":
    app.run()