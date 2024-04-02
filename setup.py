from setuptools import setup, find_packages

setup(
    name='azure_pipeline',
    version='1',
    packages=find_packages(),
    package_data={
        '': ['requirements.txt'],
        'azure_pipeline': ['main.py', 'scripts/*'],  # 包含在根目录下的 main.py 文件
    },
    install_requires=[
        # List your project dependencies here
        'fastapi==0.104.1',
        'uvicorn==0.24.0.post1',
        'pyodbc==5.1.0',
        'azure-storage-blob==12.19.1',
        'azure-applicationinsights>=0.1.1'
    ],
)



