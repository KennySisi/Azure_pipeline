from setuptools import setup, find_packages

setup(
    name='azure_pipeline',
    version='1',
    packages=find_packages(),
    package_data={
        '': ['requirements.txt'],
        'azure_pipeline': ['main.py', 'scripts/*'], 
    },
    install_requires=[
        # List your project dependencies here
        'fastapi==0.104.1',
        'uvicorn==0.24.0.post1'
    ],
)



