# opencv-interactive
![alt text](https://raw.githubusercontent.com/JeanMaximilienCadic/opencv-stl-interactive/master/imgs/opencv-annotate.png)

A simple tool to annotate 3d files online.

### Prerequisites

To start install opencv in a conda environment.
```
conda install -c conda-forge opencv
conda install -c ninedw gnutools-python
conda install -c ninedw iyo_cad
```

### How to
You should split each case into a folder. Change the code in the ImageGenerator (l24) to load the desired files to annotate
```
...
setmesh = NMesh(self.files['model'])
...
```

Then run
```
python main.py --root [root_path]
```

Use left, right keys to rotate; up, down keys to switch the cases.

The results will be written into a `annotation.txt` file.

## Authors

* **CADIC Jean Maximilien**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
