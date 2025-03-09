# Image Processing API (Django Version)

## Overview
This is a Django-based image processing API that allows users to upload an image, process it, and download the modified version. The API supports background removal using `rembg` and allows users to specify image quality and format.

A Flask version was later developed for a more lightweight and microservice-friendly approach.

## Features
- Accepts image uploads via `multipart/form-data`
- Supports PNG, JPG, JPEG, WEBP, TIFF, and TIF formats
- Background removal using `rembg`
- Adjustable image quality (0-100)
- Allows output format conversion
- Returns the processed image as a downloadable file

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/backend-image-proc.git
   cd backend-image-proc
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```sh
   python manage.py migrate
   ```

## Running the Application

1. Start the Django development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints
### 1. Process Image
- **Endpoint:** `POST /api/image-proc/`
- **Request Type:** `multipart/form-data`
- **Parameters:**
  - `image` (file, required): The image to be processed
  - `quality` (integer, optional): Image quality (0-100, default: 75)
  - `format` (string, optional): Output format (`png`, `jpg`, `jpeg`, `webp`, `tiff`, default: `png`)
  - `removebg` (boolean, optional): Whether to remove the background (default: `false`)

#### Example Request (Using `cURL`):
```sh
curl -X POST http://127.0.0.1:8000/api/image-proc/ \
     -F "image=@sample.jpg" \
     -F "quality=80" \
     -F "format=png" \
     -F "removebg=true" \
     -o output.png
```

## Technologies Used
- **Django** - Web framework
- **Django REST Framework (DRF)** - API handling
- **Pillow (PIL)** - Image processing
- **rembg** - Background removal
- **io.BytesIO** - In-memory file handling

## Future Improvements
- Add authentication
- Support for additional image transformations
- Deploy as a Dockerized microservice

