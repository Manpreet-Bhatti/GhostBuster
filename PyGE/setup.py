from distutils.core import setup
setup (
  name = 'PyGE',         # How you named your package folder (MyLib)
  packages = ['PyGE'],   # Chose the same as "name"
  version = '0.1.0',      # Start with a small number and increase it with every change you make
  license='GNU General Public License',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python Game Engine',   # Give a short description about your library
  author = 'CPSuperstore',                   # Type in your name
  author_email = 'http://cpsuperstore.pythonanywhere.com/',      # Type in your E-Mail
  url = 'https://github.com/CPSuperstore-Inc/PyGE',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/CPSuperstore-Inc/PyGE/archive/0.1.0.tar.gz',    # I explain this later on
  keywords = ['PYTHON', 'GAME', 'ENGINE'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pygame',
          'math',
          'typing',
          'time',
          'screeninfo',
          'distutils',
          'matplotlib',
          'xmltodict',
          'threading',
          'os',
          'numpy'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: GNU General Public License',   # Again, pick a license    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)