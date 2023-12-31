from setuptools import setup, find_packages
# https://setuptools.pypa.io/en/latest/userguide/quickstart.html

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='nflscraping',
    version='0.0.1',
    description='Package-for-doing-NFL-play-by-play-analysis',
    author='Benjamin-Kearsley-&-Zayne-Maughan',
    author_email='ben.kearsley@outlook.com',
    url='https://github.com/benkearsley/nfl_scraping_project.git',
    packages=find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    exclude=['Game Data Collection.ipynb', 'ben_testing.ipynb', 'Random_forest_test.ipynb'],
    package_data = {'mypackage': ['data/*.csv']}
)

