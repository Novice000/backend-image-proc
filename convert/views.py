from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from rembg import remove

class ImageProc(APIView):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if "image" not in request.FILES:
            return Response({"error": "No image provided"}, status=400)

        try:
            image = request.FILES["image"]
            img = Image.open(image)
        except UnidentifiedImageError:
            return Response({"error": "Invalid image file"}, status=400)
        
        # Process remove_bg (ensure it's a valid boolean)
        remove_bg: bool = request.data.get("remove_bg", "false").lower() == "true"

        if remove_bg:
            try:
                img = remove(img)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
            # Ensure output has transparency
            if img.mode != "RGBA":
                img = img.convert("RGBA")

        # Process quality
        try:
            quality = int(request.data.get("quality", 75))
            if not (0 <= quality <= 100):
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid quality value"}, status=400)

        # Process file format
        file_format = request.data.get("img_format", "png").lower()
        if file_format not in ["jpeg", "png", "webp", "tiff", "pdf"]:
            return Response({"error": "Invalid file_format value"}, status=400)

        # Save optimized image to memory
        img_io = BytesIO()
        save_kwargs = {"format": file_format}
        if file_format in ["jpeg", "png", "webp"]:
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
        
        img.save(img_io, **save_kwargs)
        img_io.seek(0)

        # Set correct content type
        content_type = "application/pdf" if file_format == "pdf" else f"image/{file_format}"
        file_extension = file_format if file_format != "jpeg" else "jpg"

        response = FileResponse(img_io, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{image.name.split(".")[0]}.{file_extension}"'
        return response
