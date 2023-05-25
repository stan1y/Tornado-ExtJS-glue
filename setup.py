try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='teg',
    version='0.1.0',
    description="Tornado-ExtJS glue with RESTfull Ext.Store filtering, sorting and pagging support and other goodies",
    author="Stanislav Yudin",
    author_email="stan@endlessinsomnia.com",
    url="http://endlessinsomnia.com",
    include_package_data=True,
    install_requires=[ 
    	"tornado==6.3.2",  
    	"SQLAlchemy==0.7.0",  
    	"nose>=1.1",
    	"cdecimal>=2.2"
    ],
    packages=['teg'],
    setup_requires=[],
    zip_safe=True
)
