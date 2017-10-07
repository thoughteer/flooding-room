import setuptools


configuration = {
    "name": "floodingroom",
    "version": "0.0.1",
    "description": "Flooding Room game",
    "classifiers": [
        "Development Status :: 4 - Beta",
    ],
    "url": "https://github.com/thoughteer/flooding-room",
    "author": "Tigran Valerievich Sitdikov",
    "author_email": "thoughteer@yandex-team.ru",
    "license": "FU",
    "packages": setuptools.find_packages(exclude=["tests", "tests.*"]),
    "include_package_data": True,
    "install_requires": [
        "eventlet >= 0.21.0",
        "flask >= 0.12.2",
        "flask-socketio >= 1.8.1",
    ],
    "zip_safe": False,
}
setuptools.setup(**configuration)
