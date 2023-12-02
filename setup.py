from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nfl_scraping',
    version='0.0.1',
    descrption='Package-for-doing-NFL-play-by-play-analysis',
    author='Benjamin-Kearsley-&-Zayne-Maughan',
    author_email='ben.kearsley@outlook.com',
    url='https://github.com/benkearsley/nfl_scraping_project.git',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'numpy',
        'bs4',
        're',
        'time'
        # Do I need to include thins like sphinx?  Or setuptools?  Also is bs4 included in the right way?
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)

