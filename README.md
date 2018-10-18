# intro2python
Scripts for the Digitial Methods module: Introduction to coding

To get started on this module, you will need to install python and a few modules. Follow these steps to set up the necessary python environment.

(a) Navigate to https://conda.io/miniconda.html and download the appropriate Miniconda installer for your operating system. Most modern laptops require the 64-bit version. Double click on the downloader install and install following the default settings.

(b) Your Start menu (or similar in Mac or Linux), should now have a program called conda prompt. Double click on this and a console screen will appear.

(c) We can now install the final few things needed by typing this command in the conda prompt window:

conda install numpy, matplotlib, spyder, pandas

Type “y” when asked to proceed with installation.

(d) Close the conda prompt window. You should now have a program called Spyder available in your start menu. Spyder provides a good graphical interface to Python and will allow you to open the river catchment model and make modifications to the variables.

---------------------------
### Instructions for mac
https://stackoverflow.com/questions/38080407/how-can-i-install-the-latest-anaconda-with-wget

1. Open the 'Terminal' app on your Mac.

The easiest way is hitting (spotlight finder):
`cmd + Enter`

and typing:
`terminal`

and it should be the first application that appears.

2. Copy and paste the following commands one line at a time.

Paste them into your terminal prompt.
Hit Enter after EACH LINE.

```bash
cd ~
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

-- wait while it installs & follow on screen prompts --

```bash
conda install numpy matplotlib pandas spyder
```

A long and terrifying list of things will appear.

Just type `y` to accept the installation of these packages.

Let these install.
