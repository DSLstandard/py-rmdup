import distutils.core
import setuptools
import io

distutils.core.setup(
  name="rmdup",
  version="1.0.0",
  packages=setuptools.find_packages(),
  install_requires=io.open("requirements.txt").read().splitlines(),
  entry_points={
    "console_scripts": [
      "rmdup = rmdup.cli:main"
    ]
  }
)
