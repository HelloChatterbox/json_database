from setuptools import setup

setup(
    name='json_database',
    version='0.5.2',
    packages=['json_database', 'json_database.utils'],
    url='https://github.com/HelloChatterbox/json_database',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    install_requires=["pyxdg", "fasteners"],
    description='searchable json database with persistence'
)
