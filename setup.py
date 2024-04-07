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
        'uvicorn==0.24.0.post1',
        'pyodbc==5.1.0',
        'azure-storage-blob==12.19.1',
        'azure-applicationinsights>=0.1.1',
        'aiohttp==3.9.3',
        'azure-servicebus==7.12.1',
        'azure-identity==1.15.0'
    ],
)



