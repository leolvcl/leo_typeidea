from setuptools import setup,find_packages

setup(
    name='leo_typeidea',
    version='0.1',
    description='blog system base on django',
    author='leolvcl',
    author_email='lvclleo@gmail.com',
    url='https://www.leolvcl.com',
    license='MIT',
    packages=find_packages('leo_typeidea'),
    package_dir={'': 'leo_typeidea'},
    package_data={'': [     # 方法一：打包数据文件
        'themes/*/*/*/*',   # 需要按目录层级匹配
    ]},
    # include_package_data=True,    # 方法二：配合MANIFEST.in文件
    install_requires=[
        'django~=1.11',
    ],
    extras_require={
        'ipython': ['ipython==6.2.1']
    },
    scripts=[
        'leo_typeidea/manage.py',
    ],
    entry_points={
        'console_scripts': [
            'leo_typeidea_manage = manage:main',
        ]
    },
    classifiers=[   # Option
        # 软件成熟度如何，可选
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # 指明项目受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # 选择项目许可证（license）
        'License :: OSI Approved :: MIT License',

        # 指定项目需要使用的python版本
        'Programing Language :: Python :: 3.6'
    ]
)