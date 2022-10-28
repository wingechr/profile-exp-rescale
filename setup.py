from setuptools import setup

if __name__ == "__main__":
    setup(
        packages=["profile_exp_rescale"],
        keywords=[],
        install_requires=["numpy", "scipy"],
        name="profile_exp_rescale",
        # description="DESCRIPTION",
        # long_description=long_description,
        # long_description_content_type="text/markdown",
        version="0.1.0",
        author="Christian Winger",
        author_email="c@wingechr.de",
        url="https://github.com/wingechr/profile-exp-rescale",
        platforms=["any"],
        license="Public Domain",
        classifiers=[
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        ],
    )
