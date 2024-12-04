from django.shortcuts import render


class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            print(f"Unhandled exception: {e}")
            return render(request, "500.html", status=500)
        return response
