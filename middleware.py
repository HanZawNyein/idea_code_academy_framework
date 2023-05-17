class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, *args, **kwargs):
        self.handle_request(*args, **kwargs)

    def handle_request(self, request, client_address, server):
        self.app(request, client_address, server)

    def process_request(self, request):
        print("Processing request...")  # Example pre-processing logic

    def process_response(self, response):
        print("Processing response...")  # Example post-processing logic

