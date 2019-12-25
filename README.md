# opencv-interactive

A simple tool to annotate 3d files online.

### Prerequisites

To start install opencv in a conda environment.
```
conda install -c conda-forge opencv
conda install gnutools-python
conda install iyo-cad
```

### How to
You should split each case into a folder. Change the code in the ImageGenerator (l17) to load the desired files to annotate
```
...
setmesh = NMesh(list=[crown, prepa])
...
```

Then run
```
python main.py --root [root_path]
```

Use left, right keys to rotate; up, down keys to switch the cases.

The results will be written into a `annoation.txt` file.

## Authors

* **CADIC Jean Maximilien**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
