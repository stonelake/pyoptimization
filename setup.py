from distutils.core import setup
setup(name='pyopt',
      version='0.0.2',
      description='PyOpt package',
      long_description = "A set of utils to solve optimization and packing problems",
      author='Alex Baranov',
      author_email='aleksey.baranov@gmail.com',
      url='',
      packages=['pyopt','pyopt.discrete', 'pyopt.discrete.inequalities'],
      classifiers=(
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
        ),
      license="GPL-2", requires=['matplotlib', 'numpy']
     )