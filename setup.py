from distutils.core import setup
setup(
  name = 'remove-bg',         # How you named your package folder (MyLib)
  packages = ['remove-bg'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "A Python API wrapper for removing background using remove.bg's API",   # Give a short description about your library
  author = 'Brian Lam',                   # Type in your name
  author_email = 'brian_lam@live.com',      # Type in your E-Mail
  url = 'https://github.com/brilam/remove-bg',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/brilam/remove-bg/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
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
  ],
)