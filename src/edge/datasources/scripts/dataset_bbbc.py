import requests
from pathlib import Path
import zipfile
import skimage.io as skio
import matplotlib.pyplot as plt
import shutil
from edge.datamanagement.dml import create_dml, save_dml

# Create folder and write zip files if doesn't exist
data_path = Path("edge/datasources/data")
images_zip = data_path / "images.zip"
images_path = data_path / "images"

if not images_zip.exists():
    # Get zip data from url
    images = requests.get("https://data.broadinstitute.org/bbbc/BBBC039/images.zip")
    masks = requests.get("https://data.broadinstitute.org/bbbc/BBBC039/masks.zip")
    metadata = requests.get("https://data.broadinstitute.org/bbbc/BBBC039/metadata.zip")

    # Check if received successful
    assert images.ok
    assert masks.ok
    assert metadata.ok

    data_path.mkdir(parents=True, exist_ok=True)

    with open(images_zip,'wb') as f:
        f.write(images.content)

    with zipfile.ZipFile(images_zip, 'r') as myzip:
        for file in myzip.namelist():
            if file.startswith("images"):
                myzip.extract(file, data_path)
        myzip.close()    

    #for file in tmp_image_path.iterdir():
    #    shutil.move(file, images_path)
    #shutil.rmtree(tmp_image_path)

    # Show one sample image with pyplot
    sample_image = images_path / "IXMtest_A02_s1_w1051DAA7C-7042-435F-99F0-1E847D9B42CB.tif"
    image = skio.imread(sample_image)
    #plt.imshow(image)
    #plt.show()

# write yml meta info for experiment images (simulated by downloading BBBC039 dataset)
simulation_presets = {
    "p1": {"noise": "poisson", "blur": 1.1},
}

samples = list()
for file in images_path.glob('*.tif'):
    image_dict = dict()
    image_dict = {"path": file.as_posix(), "sim": "p1", "split": "none"}
    samples.append(image_dict)

dml = create_dml(simulation_presets, samples)
save_dml(dml, data_path / "dataset_meta.yaml")

