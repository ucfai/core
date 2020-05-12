# AI@UCF/core

These meetings are offered every semester, and are tailored for the newcomers to the club. These are what, initially, [@flxsosa][felix-git], [@ionlights][john-git], and [@dibaccory][richard-git], offered at club meetings.

[felix-git]: https://github.com/flxsosoa
[john-git]: https://github.com/ionlights
[richard-git]: https://github.com/dibaccory

The goal of this `course` is to compensate for the lack of UCF undergraduate coursework in intelligence and related fields (e.g. machine learning, computational neuroscience, etc.). As a semester offering, the overarching idea is that the course material won't change much, but each semester will entail a slight twist on the presentation, as expected with rotating instructors.

## Getting it locally and making use
Within each `<sem><year>` (e.g. `sp19`) folder, there's an `env.yml` file, which can be used with [Anaconda](anaconda.org). These have only been tested on Linux systems, so version numbers may not be up-to-date on platforms which don't use the Linux Kernel. However, the usage of such `env.yml` files will be detailed below.

### Installing the environment
```bash
$ conda env create -f <sem><year>/env.yml
```

### Using the environment
```bash
$ conda activate ucfai-<sem><year>
```

**NOTE:** We assume the use of GPU versions of Deep Learning libraries (e.g. PyTorch, TensorFlow, etc.). If you *do not* have a GPU, then you should install the *CPU* versions of said libraries.
