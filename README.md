## apple_health_analysis

Notebooks and scripts for analyzing Apple Health data.

### Quick Start

First,
[clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
to your machine.

Next, make sure that the [uv Python package manager](https://docs.astral.sh/uv/getting-started/installation/)
is installed. This is an excellent alternative to `pip`, `poetry`, etc. and greatly simplifies the
setup process for projects like this.

Once this is installed, you will need to export your Apple Health data as a zip file from your
iPhone to your machine. **PLEASE NOTE that health data is extremely sensitive and can be subject to
various laws such as HIPAA, etc. depending on your jurisdiction, so DO NOT EXPORT this to any
untrusted computer, especially public ones!** If you are unsure, it is **far better to play it
safe** and not use this software. There is already quite a lot of analysis available directly
within Apple Health that likely already suits your needs and interests. This is just a passion
project to dig deeper into one's own health data.

If proceeding with export, follow the instructions
[here](https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios) under *"Share
your health and fitness data in XML format"* to export a `.zip` file containing your health data in
XML format. These instructions currently work for me as of July 7th, 2025 on an iPhone 13 Pro
running iOS 18.5 (build 22F76), and are not guaranteed to work for everyone. If you experience
issues with the format and/or this link no longer works, please
[file a GitHub issue](https://github.com/andrew-titus/apple_health_analysis/issues/new).

Once you tap "Export All Data", it may take several minutes to package all of the data into the
`.zip` file. Name the file `apple_health.zip` (**not whatever the default name is!**) and then use
your preferred method of secure file transfer (*e.g.*, using
[AirDrop](https://support.apple.com/guide/security/airdrop-security-sec2261183f4/web) from your
iPhone to a Mac) to place the file in the root directory of your cloned repository. Once in place,
unzip the file to a directory `apple_health/` in the same root directory. This can simply be done
with `unzip apple_health.zip` on Mac/Linux, or with whatever tool that you prefer.

**NOTE**: the [.gitignore](./.gitignore) file should take care of this automatically, but
nonetheless, for the same reasons mentioned earlier about sensitivity of health data, **DO NOT
ATTEMPT TO CHECK THE ZIP FILE, NOR THE EXTRACTED ARCHIVE AND ITS CONTENTS, INTO GITHUB!**

Once `uv` is installed and the `apple_health.zip` file has been unzipped to `apple_health/` in the
root directory of your cloned repository, simply run the following to run
[Jupyterlab](https://jupyter.org) using the virtual environment defined by [uv.lock](./uv.lock).
This will ensure that the proper Python version and package dependencies are installed and used
correctly in the notebooks. See [here](https://docs.astral.sh/uv/guides/integration/jupyter/) for
more information on using `jupyter` with `uv`.

```bash
uv run --with jupyter jupyter lab
```

### Notebooks

TODO

### Development

Use [ruff](https://docs.astral.sh/ruff/configuration/#jupyter-notebook-discovery) to format and
lint the Jupyter notebooks. For convenience, this can be run simply by calling:

```bash
./scripts/lint.sh
```

The same checks will run as part of any pull request, and will be required to pass in order for the
PR to be merged.
