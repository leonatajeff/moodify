from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'pandas',
    'pathlib',
    'google-cloud-datastore'
]

setup(
    name='Moodify',
    version="1.0",
    description="What if you could see your sounds?",
    author="group-g",
    author_email="leonatajeff@gmail.com",
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
