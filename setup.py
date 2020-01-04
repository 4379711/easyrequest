# coding = utf-8
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6, 0):
    raise RuntimeError("EasyRequest requires Python 3.6.0+")

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='EasyRequest',
    version="1.0.1",
    description=(
        "A easy use request frame !"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='liuyalong',
    author_email='4379711@qq.com',
    maintainer='liuyalong',
    maintainer_email='4379711@qq.com',
    license='MIT License',
    packages=find_packages(exclude=["*.log", "*.tests.*", "tests.*", "tests"]),
    platforms=["all"],
    python_requires='>=3.6.0',
    url='https://github.com/4379711/easyrequest',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    # 指定入口
    entry_points={
        'console_scripts': [
            'EasyRequest=easyrequest.cmdline:execute',
            'easyrequest=easyrequest.cmdline:execute',
            'Easyrequest=easyrequest.cmdline:execute'
        ],
    },

    install_requires=['colorama',
                      'click',
                      'requests',
                      'gevent',
                      'lxml',
                      'psutil'
                      ],
    include_package_data=True
)

# python setup.py check                 检查错误
# python setup.py sdist bdist_wheel     编译
# twine upload dist/*                   上传到pypi
