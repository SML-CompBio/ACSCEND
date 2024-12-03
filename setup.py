with open('README.md', 'r') as f:
    long_description = f.read()

from setuptools import setup, find_packages

setup(
    name='ACSCeND',
    version='1.0',    
    url='https://github.com/SML-CompBio/ACSCEND',
    author='Shreyansh Priyadarshi',
    author_email='shreyansh.priyadarshi02@gmail.com',
    license='MIT License',
    packages=find_packages(),
    package_data={'ACSCeND': ['lr_model.joblib']},
    include_package_data=True,
    install_requires=['pandas==2.2.0',
                      'numpy==1.26.3',
                      'torch==2.1.2',
                      'scikit-learn==1.5.0',
                      'joblib==1.4.2',
                      'scipy==1.11.4'
                      ],
    description='A deep learning tool for bulk RNA-seq deconvolution and Stem Cells Sub-Class prediction.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)

