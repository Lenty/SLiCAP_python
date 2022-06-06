# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 09:28:49 2020

@author: luc_e

Modified by Anton 16 May 2022:
Updated to version 1.3.0
"""

import os, shutil
from os.path import expanduser
import setuptools
from setuptools.command.install import install
import platform
import subprocess
import re
from shutil import copy

INSTALLVERSION="1.3.0"

class InstallWrapper(install):
    """
    Provides a install wrapper for SLiCAP.
    Contains private functions that are to be run.
    """
    _maxima_cmd = "None"
    _LTSpice_cmd = "None"
    _SLiCAP_version = None
    _library_location = None
    _doc_location = None
    _install_location = None

    def run(self):
        """
        Runs the SLiCAP installation.

        Returns
        -------
        None.
        """
        self._set_maxima_command()
        self._set_ltspice_command()
        self._set_version_config()
        self._set_install_location()
        self._gen_config_file()
        install.run(self)

    def _set_maxima_command(self):
        """
        Determining the Maxima command
        This contains two flows:
            Windows -   Searches the drive root dir (e.g. C:\) for a maxima directory and generates the full path
                        This path points to maxima.bat, which is found in the bin directory
                        Manual entry of the maxima path is also possible
            Linux -     test is the 'maxima' command is callable from the command line

        Returns
        -------
        None.
        """
        self._maxima_cmd="maxima"
        print("Acquiring Maxima Command")
        maxInput = '1+1;'
        if platform.system() == 'Windows':
            self._find_maxima_windows()
            result = 0
            try:
                result = subprocess.run([self._maxima_cmd, '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=3, text=True).stdout.split('\n')
                result = [i for i in result if i] # Added due to variability of trailing '\n'
                result = result[-1]
                if int(result) == 2:
                    print("Succesfully ran 'Maxima' command")
                else:
                    print("Could not successfully run the 'Maxima' command.")

            except:
                print("Not able to succesfully execute the 'Maxima' command, you need to edit the configuration file manually!")
        else:
            try:
                result = subprocess.run(['maxima', '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=3, text=True).stdout.split('\n')
                result = [i for i in result if i] # Added due to variability of trailing '\n'
                result = result[-1]
                if int(result) == 2:
                    print("Succesfully ran 'Maxima' command")
                else:
                    print("Could not successfully run the 'Maxima' command.")

            except:
                print("Not able to run the 'Maxima' command, verify Maxima is installed by typing 'Maxima' in the command line")
                print("In case Maxima is not installed, use your package manager to install it (f.e. 'sudo apt install maxima')")
                succes= succes + 2

    def _set_ltspice_command(self):
        """
        Determining the LTSPICE command
        This contains two flows:
            Windows -   Searches the program files dir (e.g. C:\Program Files) for the LTSpice Command
            Linux   -   Searches the wine drive directory for the LTSpice command
        """
        self._LTSpice_cmd = " "
        print("Acquiring LTSpice Command")
        self._find_ltspice()
        if self._LTSpice_cmd != " ":
            print("Found the LTSpice directory: ", self._LTSpice_cmd)
        else:
            print("Could not find LTspice command, you need to edit the configuration file manually!")

    def _set_version_config(self):
        """
        Sets the SLiCAP version variable to be set in the config file
        Can be appended to get the version variable from a website

        Returns
        -------
        None.

        """
        self._SLiCAP_version = INSTALLVERSION
        print("Slicap version:", self._SLiCAP_version)

    def _set_install_location(self):
        """
        Sets the SLiCAP library variable to be set in the config file
        Includes copying of the default libraries

        Returns
        -------
        None.

        """
        home = expanduser("~")
        slicap_home = os.path.join(home, 'SLiCAP')
        try:
            if os.path.exists(slicap_home):
                shutil.rmtree(slicap_home)
            def_lib_loc = os.path.join(slicap_home, 'lib')
            def_doc_loc = os.path.join(slicap_home, 'docs')
            shutil.copytree('files/', slicap_home)
            self._library_location = def_lib_loc
            shutil.copytree('docs/_build/html/', def_doc_loc)
            self._doc_location = def_doc_loc
            self._install_location = slicap_home
        except:
            print("ERROR: could not set install location.")

    def _gen_config_file(self):
        """
        Generates the SLiCAP configiguration file: SLiCAPsetting.py

        Returns
        -------
        None.

        """
        print("Generating the configuration file")
        fileloc = os.path.join("SLiCAPtemplate.py")
        filetarg = os.path.join("SLiCAP", "SLiCAPsetting", "SLiCAPsetting.py")       
        if os.path.isfile(fileloc):
            print("Found template file: ", fileloc)
            fi = open(fileloc, 'r')
            txt = fi.read()
            fi.close()
            txt = txt.replace("$VERSION", self._SLiCAP_version)
            txt = txt.replace("$SYSINSTALL", ' ')
            txt = txt.replace("$LIBCOREPATH", self._library_location)
            txt = txt.replace("$MAXIMAPATH", self._maxima_cmd)
            txt = txt.replace("$LTSPICE", self._LTSpice_cmd)
            txt = txt.replace("$DOCPATH", self._doc_location)  
            print(txt)
            fi = open(filetarg, 'w')
            fi.write(txt)
            fi.close()
        print("Created config file: ", filetarg)
        
    def _find_maxima_windows(self):
        """
        Searches for the maxima command under windows. If found it sets
        self._maxima_cmd.

        Returns
        -------
        None.
        """
        drive = os.sep.join(os.getcwd().split(os.sep)[:1])+os.sep
        winpath = os.environ['WINDIR'] + "\\System\\"
        drive = os.sep.join(winpath.split(os.sep)[:1]) + os.sep
        for root, dirs, files in os.walk(drive, topdown=True):
            for name in dirs:
                if re.match('maxima-*', name, flags=0):
                    print("found Maxima dir")
                    found = True
                    path = os.path.join(root,name, 'bin','maxima.bat')
                    print("Maxima command set as:", path)
                    self._maxima_cmd = path
                    return

    def _find_ltspice(self):
        """
        Searches for the LTspice command under windows. If found it sets
        self._maxima_cmd.

        Returns
        -------
        None.
        """
        if platform.system() == 'Windows':
            winpath = os.environ['WINDIR'] + "\\System\\"
            main_drive = os.sep.join(winpath.split(os.sep)[:1]) + os.sep
        else:
            home = expanduser("~")
            main_drive = os.path.join(home, '.wine', 'drive_c')
        drive = os.path.join(main_drive, 'Program Files')
        for root, dirs, files in os.walk(drive, topdown=True):
            for name in dirs:
                if re.match('LT(S|s)pice*', name, flags=0):
                    path = os.path.join(root,name,'XVIIx64.exe')
                    found = True
                    print("LTSpice command set as:", path)
                    self._LTSpice_cmd = path
                    return

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SLiCAP_python",
    version=INSTALLVERSION,
    author="Anton Montagne",
    author_email="anton@montagne.nl",
    description="Symbolic Linear Circuit Analysis Program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lenty/SLiCAP_python/",
    packages=setuptools.find_packages(),
    cmdclass={'install': InstallWrapper},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Attribution-NonCommercial-NoDerivatives 4.0 International",
        "Operating System :: OS Independent",
    ],
    #include_package_data=True,
    #package_data={'': ['newIlt.mac', 'det.mac']},
    python_requires='>=3.7',
)