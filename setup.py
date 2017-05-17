from setuptools import setup


setup(
    name='feedMeBackBot',
    version='0.0.2',
    packages=['feedMeBackBot'],
    description='feedMeBack bot beta',
    author='Basile Douillet',
    author_email='basiledouillet@gmail.com',
    url='https://github.com/Barz0u/feedMeBackBot',
    install_requires=['slacker >= 0.9.42',
                     'slackeventsapi'],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='slack bot feedmeback'
)
