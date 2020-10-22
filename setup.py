# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 09:28:49 2020

@author: luc_e
"""

import os, shutil
from os.path import expanduser
import setuptools
from setuptools.command.install import install
import platform
import subprocess
import re
import in_place
from shutil import copy

INSTALLVERSION="0.9.0"

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
        # Run this first so the install stops in case
        # these fail otherwise the Python package is
        # successfully installed
        self._set_maxima_command()
        self._set_ltspice_command()
        self._set_version_config()
        self._set_install_location()
        # self._set_lib_location()
        # self._set_doc_location()
        self._gen_config_file()
        # Run the standard PyPi copy
        install.run(self)

    def _set_maxima_command(self):
        """
        Determining the Maxima command
        This contains two flows:
            Windows -   Searches the drive root dir (e.g. C:\) for a maxima directory and generates the full path
                        This path points to maxima.bat, which is found in the bin directory
                        Manual entry of the maxima path is also possible
            Linux -     test is the 'maxima' command is callable from the command line
        """
        self._maxima_cmd="maxima"
        print("Acquiring Maxima Command")
        succes = False
        maxInput = '1+1;'
        if platform.system() == 'Windows':
            self._maxima_cmd = self._find_maxima_windows()

        while not(succes):
            result = 0
            if platform.system() == 'Windows':
                string = "The Maxima path found is '"+self._maxima_cmd+"', press enter to continue with this path or type the full maxima path to override this value:"
                ret_val = input(string)
                # print(repr(ret_val))
                if not ret_val:
                    print("Using found Maxima path")
                else:
                    if os.path.exists(ret_val):
                        print("Using entered Maxima path")
                        self._maxima_cmd = ret_val
                    else:
                        print("Entered path does not seem to exist, make sure you entered the path correctly")
                try:
                    result = subprocess.run([self._maxima_cmd, '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=3, text=True).stdout.split('\n')
                    result = [i for i in result if i] # Added due to variability of trailing '\n'
                    result = result[-1]
                    if int(result) == 2:
                        succes = True
                        print("Succesfully ran Maxima command")
                except:
                    print("Not able to succesfully execute the maxima command, please make sure the full path points to 'maxima.bat'")
            else:
                try:
                    result = subprocess.run(['maxima', '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=3, text=True).stdout.split('\n')
                    result = [i for i in result if i] # Added due to variability of trailing '\n'
                    result = result[-1]
                    if int(result) == 2:
                        succes = True
                        print("Succesfully ran Maxima command")

                except:
                    print("Not able to run the maxima command, verify maxima is installed by typing 'maxima' in the command line")
                    print("In case maxima is not installed, use your package manager to install it (f.e. 'sudo apt install maxima')")



    def _set_ltspice_command(self):
        """
        Determining the LTSPICE command
        This contains two flows:
            Windows -   Searches the program files dir (e.g. C:\Program Files) for the LTSpice Command
            Linux   -   Searches the wine drive directory for the LTSpice command
        """
        self._LTSpice_cmd=" "
        print("Acquiring LTSpice Command")
        succes = False
        self._LTSpice_cmd = self._find_ltspice()
        print("Found the LTSpice directory: ", self._LTSpice_cmd)
        string = "The LTSpice directory is defined as: \n'"+self._LTSpice_cmd+"'\n press enter to continue with this command or type the full LTspice command to override this value:"
        ret_val = input(string)
        if not ret_val:
            print("Using found LTSpice directory")
        else:
            if os.path.exists(ret_val):
                print("Using entered LTSpice directory")
                self._LTSpice_cmd = ret_val
            else:
                print("Entered path does not seem to exist, make sure you entered the path correctly")


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
        succes = False
        while not(succes):
            home = expanduser("~")
            slicap_home = os.path.join(home, 'SLiCAP')

            string = "Select a location for the SLiCAP installation, press enter for the default location('"+slicap_home+"'), otherwise type a full path to override this value:"
            ret_val = input(string)
            # print(repr(ret_val))
            if not ret_val:
                print("Using ", slicap_home)
            else:
                print("Using valid path", ret_val)
                slicap_home = ret_val
            try:
                if os.path.exists(slicap_home):
                    shutil.rmtree(slicap_home)
                def_lib_loc = os.path.join(slicap_home, 'lib')
                def_doc_loc = os.path.join(slicap_home, 'docs')
                # os.makedirs(slicap_home)
                shutil.copytree('files/', slicap_home)
                self._library_location = def_lib_loc
                shutil.copytree('docs/_build/html/', def_doc_loc)
                self._doc_location = def_doc_loc
                self._install_location = slicap_home
                succes = True
            except:
                print("could not set install location, make sure a correct path is entered.")


    def _set_lib_location(self):
        """
        Sets the SLiCAP library variable to be set in the config file
        Includes copying of the default libraries

        Returns
        -------
        None.

        """
        succes = False
        while not(succes):
            home = expanduser("~")
            slicap_home = os.path.join(home, 'SLiCAP', 'lib')

            string = "Select a location for the default libraries, press enter for the default location('"+slicap_home+"'), otherwise type a full path to override this value:"
            ret_val = input(string)
            # print(repr(ret_val))
            if not ret_val:
                print("Using ", slicap_home)
            else:
                print("Using valid library path", ret_val)
                slicap_home = ret_val
            try:
                if os.path.exists(slicap_home):
                    shutil.rmtree(slicap_home)
                shutil.copytree('lib/', slicap_home)
                self._library_location = slicap_home
                succes = True
            except:
                print("could not set library location")


    def _set_doc_location(self):
        """
        Sets the SLiCAP documentation path variable to be set in the config file
        Includes copying of the documentation

        Returns
        -------
        None.

        """
        succes = False
        while not(succes):
            home = expanduser("~")
            slicap_home = os.path.join(home, 'SLiCAP', 'docs')

            string = "Select a location for the documentation, press enter for the default location('"+slicap_home+"'), otherwise type a full path to override this value:"
            ret_val = input(string)
            # print(repr(ret_val))
            if not ret_val:
                print("Using ", slicap_home)
            else:
                print("Using valid documentation path", ret_val)
                slicap_home = ret_val
            try:
                if os.path.exists(slicap_home):
                    shutil.rmtree(slicap_home)
                shutil.copytree('docs/_build/html/', slicap_home)
                self._doc_location = slicap_home
                succes = True
            except:
                print("could not set documentation location.")

    def _gen_config_file(self):
        print("Generating the configuration file")
        fileloc = os.path.join("SLiCAPtemplate.py")
        filetarg = os.path.join("SLiCAP", "SLiCAPsetting", "SLiCAPsetting.py")
        if os.path.isfile(fileloc):
            print("Found template file: ", fileloc)
            copy(fileloc, filetarg)
            with in_place.InPlace(filetarg) as file:
                for line in file:
                    line = line.replace("$VERSION", self._SLiCAP_version)
                    line = line.replace("$SYSINSTALL", ' ')
                    line = line.replace("$LIBCOREPATH", self._library_location)
                    line = line.replace("$MAXIMAPATH", self._maxima_cmd)
                    line = line.replace("$LTSPICE", self._LTSpice_cmd)
                    line = line.replace("$DOCPATH", self._doc_location)
                    # print(line)
                    file.write(line)
        print("Created config file: ", filetarg)


    def _find_maxima_windows(self):
        drive = os.sep.join(os.getcwd().split(os.sep)[:1])+os.sep
        print(drive)
        for root, dirs, files in os.walk(drive, topdown=True):
            for name in dirs:
                if re.match('maxima-*', name, flags=0):
                    print("found Maxima dir")
                    path = os.path.join(root,name, 'bin','maxima.bat')
                    print("Maxima path set as:", path)
                    return path

    def _find_ltspice(self):
        if platform.system() == 'Windows':
            main_drive = os.sep.join(os.getcwd().split(os.sep)[:1])+os.sep
            drive = os.path.join(main_drive, 'Program Files')
        else:
            home = expanduser("~")
            drive = os.path.join(home, '.wine', 'drive_c')
        # print(drive)
        for root, dirs, files in os.walk(drive, topdown=True):
            for name in dirs:
                if re.match('LT(S|s)pice*', name, flags=0):
                    # print("found LTspice dir")
                    path = os.path.join(root,name,'XVIIx64.exe')
                    # print("LTSpice path set as:", path)
                    return path
        return ' '

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SLiCAP_python", # Replace with your own username
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
    python_requires='>=3.7',
)
