# Django DeepFace

A Django app for face recognition authentication using DeepFace and pgvector.

[![PyPI version](https://badge.fury.io/py/django-deepface.svg?version=0.0.2)](https://badge.fury.io/py/django-deepface)
[![Python Support](https://img.shields.io/pypi/pyversions/django-deepface.svg)](https://pypi.org/project/django-deepface/)
[![Django Support](https://img.shields.io/badge/django-4.2%20%7C%205.0%20%7C%205.1%20%7C%205.2-blue)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI-assisted](https://img.shields.io/badge/code%20origin-AI--assisted-blueviolet)](#ai-generated-code-disclosure)


## Features

- 🔐 Face recognition authentication alongside traditional password authentication
- 📸 Capture face images via webcam or file upload
- 🚀 Fast face matching using pgvector similarity search
- 👤 Support for multiple face images per user (up to 4)
- 🎨 Modern, responsive UI with Bootstrap 5
- 🔒 Secure storage and processing of biometric data

## Demo app

There is a [demo app](https://github.com/topiaruss/django-deepface-demo) that shows how you can get started with this library. The app adds the ability to count successful use of image upload, storing the browser agent string for analysis.  This helps check if users in your company can use image capture and on what devices, before making the decision to implement it.


## Requirements

- Python 3.8+ (less than 3.12 due to tensorflow wheels and instruction set issues)
- Django 4.2+
- PostgreSQL with pgvector extension
- A working webcam (for face capture features)

## Installation

1. Install the package (recommended with uv):
```bash
# Using uv (recommended)
uv pip install django-deepface

# Or using pip
pip install django-deepface
```

2. Install system dependencies for face recognition:
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev
sudo apt-get install -y python3-h5py
sudo apt-get install -y libopenblas-dev

# On macOS
brew install cmake
brew install hdf5
```

3. Install tf-keras (required for TensorFlow 2.19.0+):
```bash
uv pip install tf-keras
# or
pip install tf-keras
```

4. Set up PostgreSQL with pgvector:
```bash
# Install pgvector extension
sudo apt-get install postgresql-14-pgvector  # Adjust version as needed

# Create extension in your database
psql -U postgres -d your_database -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Quick Start

1. Add `django_deepface` to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'django_deepface',
    ...
]
```

2. Configure your database to use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Add URL patterns:
```python
from django.urls import path, include

urlpatterns = [
    ...
    path('auth/', include('django_deepface.urls')),
    ...
]
```

4. Run migrations:
```bash
python manage.py migrate django_deepface
```

5. Configure media files settings:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

6. Add media URL patterns (development only):
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Usage

### User Registration with Face

1. Navigate to `/auth/profile/`
2. Upload up to 4 face images for better recognition accuracy
3. Images are processed and stored as embeddings for fast matching

### Face Login

1. Navigate to `/auth/login/`
2. Enter your username
3. Check "Use Face Login"
4. Allow webcam access and capture your face
5. Click "Login"

### Management Commands

Add face images from a directory tree:
```bash
python manage.py add_image_tree /path/to/faces --clear
```

Directory structure should be:
```
/path/to/faces/
├── username1/
│   ├── face1.jpg
│   └── face2.jpg
└── username2/
    └── face1.jpg
```

## Configuration

### Settings

```python
# Maximum number of face images per user
DEEPFACE_MAX_FACES = 4

# Face recognition model (default: VGG-Face)
DEEPFACE_MODEL = "VGG-Face"

# Detection backend (default: retinaface)
DEEPFACE_DETECTOR = "retinaface"

# Similarity threshold (default: 0.3)
DEEPFACE_THRESHOLD = 0.3
```

### Models

The app provides two main models:

- `UserProfile`: Extends the User model (optional)
- `Identity`: Stores face embeddings and images

## API Reference

### Views

- `face_login`: Handle face-based authentication
- `profile_view`: Manage user's face images
- `delete_face`: Remove a specific face image

### Forms

- `FaceLoginForm`: Combined username/password/face login form
- `FaceImageUploadForm`: Face image upload form

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/topiaruss/django-deepface.git
cd django-deepface

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies (recommended with uv)
uv pip install -e ".[dev]"
# or
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=django_deepface
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=django_deepface --cov-report=html

# Run specific test
pytest django_deepface/tests/test_views.py::TestProfileView
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Considerations

- Face embeddings are stored as vectors, not actual images
- Always use HTTPS in production
- Consider privacy regulations (GDPR, etc.) when storing biometric data
- Implement proper access controls and audit logging
- Regular security updates for dependencies

## AI-Generated Code Disclosure

This project includes portions of code that were generated with the assistance of large language models—specifically , **Claude 3.7 Sonnet**, **Claude 4 Opus**. These tools were used to accelerate scaffolding, explore idiomatic patterns, and propose implementations for specific challenges.

All AI-generated code has been reviewed, integrated, and tested by the author. Transparency is important: this project makes no attempt to conceal the involvement of generative AI, and welcomes scrutiny and feedback.

If you're curious about the design, want to critique the use of AI in open-source development, or have experience with similar approaches, the author invites comments and contributions from both the AI and broader developer communities.

Your insights—technical, ethical, or otherwise—are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DeepFace](https://github.com/serengil/deepface) for face recognition
- [pgvector](https://github.com/pgvector/pgvector) for similarity search
- My friends in the Django and python community for soooo... much goodness

## Support

- Documentation: [https://django-deepface.readthedocs.io](https://django-deepface.readthedocs.io)
- Issues: [https://github.com/topiaruss/django-deepface/issues](https://github.com/topiaruss/django-deepface/issues)
- Discussions: [https://github.com/topiaruss/django-deepface/discussions](https://github.com/topiaruss/django-deepface/discussions)
- PyPI: [https://pypi.org/project/django-deepface/](https://pypi.org/project/django-deepface/)
