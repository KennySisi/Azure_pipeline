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
        'annotated-types==0.6.0',
        'anyio==3.7.1',
        'click==8.1.7',
        'colorama==0.4.6',
        'fastapi==0.104.1',
        'h11==0.14.0',
        'idna==3.6',
        'pydantic==2.5.2',
        'pydantic_core==2.14.5',
        'sniffio==1.3.0',
        'starlette==0.27.0',
        'typing_extensions==4.8.0',
        'uvicorn==0.24.0.post1'
    ],
)



