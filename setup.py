from setuptools import setup, find_packages

setup(
    name='personal_assistant',
    version='1.0.0',
    description='Multitool',
    url='https://github.com/VolodymyrKukharets/personal_assistant',
    author='KOLYBA team',
    author_email='vladimir.kuharets.kiev@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'personal_assistant=personal_assistant.main:main'
        ]
    },
)
