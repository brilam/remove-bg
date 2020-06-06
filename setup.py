from distutils.core import setup
setup(
  name = 'removebg',         # How you named your package folder (MyLib)
  packages = ['removebg'],   # Chose the same as "name"
  version = '0.04',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "A Python API wrapper for removing background using remove.bg's API",   # Give a short description about your library
  author = 'Brian Lam',                   # Type in your name
  author_email = 'brian_lam@live.com',      # Type in your E-Mail
  url = 'https://github.com/brilam/remove-bg',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/brilam/remove-bg/archive/v_004.tar.gz',    # I explain this later on
  keywords = ['remove-bg', 'remove', 'background'],   # Keywords that define your package best
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which Python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)