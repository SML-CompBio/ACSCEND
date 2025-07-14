with open('README.md', 'r') as f:
    long_description = f.read()

from setuptools import setup, find_packages

setup(
    name='ACSCeND',
    version='1.1',    
    url='https://github.com/SML-CompBio/ACSCEND',
    author='Shreyansh Priyadarshi',
    author_email='shreyansh.priyadarshi02@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    package_data={'ACSCeND': ['lr_model.joblib', 'lr_scaler.joblib']},
    include_package_data=True,
    install_requires=['pandas==2.3.1',
                      'numpy==2.3.1',
                      'torch==2.7.1',
                      'scikit-learn==1.7.0',
                      'joblib==1.5.1',
                      'scipy==1.16.0'
                      ],
    description='A deep learning tool for bulk RNA-seq deconvolution and Stem Cells Sub-Class prediction.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)

