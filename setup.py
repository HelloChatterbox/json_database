from setuptools import setup

setup(
    name='json_database',
    version='0.2.8',
    packages=['json_database'],
    url='https://github.com/OpenJarbas/json_database',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    install_requires=["xdg", "fasteners"],
    description='searchable json database with persistence'
)
