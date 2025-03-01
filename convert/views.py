from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from io import BytesIO
from rembg import remove

class ImageCompress(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if "image" not in request.FILES:
            return Response({"error": "No image provided"}, status=400)

        image = request.FILES["image"]
        img = Image.open(image)

        width = request.data.get("width")
        height = request.data.get("height")

        try:
            width = int(width) if width else None
            height = int(height) if height else None
        except ValueError:
            return Response({"error": "Invalid width or height"}, status=400)

        # Resize image
        if width and height:
            img = img.resize((width, height), Image.LANCZOS)
        else:
            img = img.resize((int(img.width * 2 / 3), int(img.height * 2 / 3)), Image.LANCZOS)

        # Save optimized image to memory
        img_io = BytesIO()
        img.save(img_io, format="PNG", optimize=True)
        img_io.seek(0)

        response = FileResponse(img_io, content_type="image/png")
        response["Content-Disposition"] = f'attachment; filename="{image.name}"'
        return response


class ImageRemoveBg(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if "image" not in request.FILES:
            return Response({"error": "No image provided"}, status=400)

        image = Image.open(request.FILES["image"])
        output = remove(image)

        # Ensure output has transparency
        if output.mode != "RGBA":
            output = output.convert("RGBA")

        img_io = BytesIO()
        output.save(img_io, format="PNG", optimize=True)
        img_io.seek(0)

        response = FileResponse(img_io, content_type="image/png")
        response["Content-Disposition"] = f'attachment; filename="{request.FILES["image"].name}"'
        return response
