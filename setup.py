from setuptools import setup

setup(name="cuckoofilter",
      version="0.0.1",
      description="Python implementation of Cuckoo filter.",
      url="www.github.com/fastforwardlabs/cuckoofilter",
      author="Julius Adebayo, Fast Forward Labs",
      license="MIT",
      packages=["cuckoofilter"],
      install_requires=["mmh3",
                        "numpy",
                        "json",
                        "shutil",
                        "matplotlib"
                        ],
      include_package_data=True,
      zip_safe=False
      )
