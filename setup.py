from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-deepface",
    version="0.0.3",
    author="Your Name",
    author_email="your.email@example.com",
    description="Django app for face recognition authentication using DeepFace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/django-deepface",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Django Applications",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.0",
        "deepface>=0.0.75",
        "pgvector>=0.4.1",
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
        "device-detector==5.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-django>=4.5",
            "pytest-cov>=4.0",
            "ruff>=0.3.0",
            "django-stubs>=1.12",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
