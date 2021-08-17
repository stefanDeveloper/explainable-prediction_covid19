with import <nixpkgs> { };

let
  pythonPackages = python37Packages;
in pkgs.mkShell rec {
  venvDir = "./.venv";
  name = "python-env";

  buildInputs = [
    pythonPackages.setuptools
    pythonPackages.virtualenv # run virtualenv .
    pythonPackages.pip
    pythonPackages.pyqt5 # avoid installing via pip
    pythonPackages.pyusb # fixes the pyusb 'No backend available' when installed directly via pip
    (pythonPackages.opencv4.override { enableGtk2 = true; })
    # This execute some shell code to initialize a venv in $venvDir before
    # dropping into the shell
    pythonPackages.venvShellHook

    # Those are dependencies that we would like to use from nixpkgs, which will
    # add them to PYTHONPATH and thus make them accessible from within the venv.
    pythonPackages.numpy
    pythonPackages.requests

    # In this particular example, in order to compile any binary extensions they may
    # require, the python modules listed in the hypothetical requirements.txt need
    # the following packages to be installed locally:
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
  ];
  shellHook = ''
    # fixes libstdc++ issues and libgl.so issues
    LD_LIBRARY_PATH=${stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/
    # fixes xcb issues :
    QT_PLUGIN_PATH=${qt5.qtbase}/${qt5.qtbase.qtPluginPrefix}
    SOURCE_DATE_EPOCH=$(date +%s)

    if [ -d "${venvDir}" ]; then
      echo "Skipping venv creation, '${venvDir}' already exists"
    else
      echo "Creating new venv environment in path: '${venvDir}'"
      # Note that the module venv was only introduced in python 3, so for 2.7
      # this needs to be replaced with a call to virtualenv
      ${pythonPackages.python.interpreter} -m venv "${venvDir}"
    fi

    # Under some circumstances it might be necessary to add your virtual
    # environment to PYTHONPATH, which you can do here too;
    # PYTHONPATH=$PWD/${venvDir}/${pythonPackages.python.sitePackages}/:$PYTHONPATH

    source "${venvDir}/bin/activate"

    # Updating pip
    python -m pip install --upgrade pip

    # As in the previous example, this is optional.
    pip install -r requirements.txt

    # Install kaggle
    pip install -q kaggle
    if [ ! -d ~/.kaggle ]; then
        mkdir ~/.kaggle
        cp ~/Nextcloud/keys/kaggle.json ~/.kaggle/
        chmod 600 ~/.kaggle/kaggle.json
        pip install --upgrade --force-reinstall --no-deps kaggle
        kaggle datasets list
    fi

    if [ ! -d data/covid-chestxray-dataset ]; then
        git clone https://github.com/ieee8023/covid-chestxray-dataset.git data/covid-chestxray-dataset
    fi

    if [ ! -d data/Figure1-COVID-chestxray-dataset ]; then
        git clone https://github.com/agchung/Figure1-COVID-chestxray-dataset data/Figure1-COVID-chestxray-dataset
    fi

    if [ ! -d data/rsna ]; then
        mkdir data/rsna
        kaggle competitions download -c rsna-pneumonia-detection-challenge -p data/rsna
        unzip -q data/rsna/rsna-pneumonia-detection-challenge.zip -d data/rsna
    fi
  '';
}