import numpy as np
import matplotlib.pyplot as plt
from cellpose import models, io
from cellpose.io import imread
from cellpose import plot
from pathlib import Path 

io.logger_setup()

# Create model instance with gpu
model = models.CellposeModel(gpu=True)

# Temporary: get all images (BBBC039) from relative path
images_dir = Path("edge/datasources/data/images")
imgs = [imread(file) for file in images_dir.glob("*tif")]

print(imgs[0].shape)
print(imgs[0])
print(imgs[0].max())
print(len(imgs))

# Eval images with cellpose
masks, flows, styles = model.eval([imgs[0], imgs[1]])

# Print predictions
for idx in range(len(masks)):
    img = imgs[idx]
    mask = masks[idx]
    flow = flows[idx][0]

    fig = plt.figure(figsize=(12,5))
    plot.show_segmentation(fig, img, mask, flow, channels=[0])
    plt.tight_layout()
    plt.show()



# Extract cells from images

# Exclude background from cells

# Convert shapes matching to expected ResNet50 input (224, 224, 3)

# normalize image for ResNet50
x = cell_img.astype(np.float32)
p1, p99 = np.percentile(x, (1, 99))
x = np.clip(x, p1, p99)
x = (x - p1) / (p99 - p1)

# Inference of ResNet50 (Embeddings + Classifications)
# inp = Input(shape=(224, 224, 3))

#backbone = ResNet50(
#    weights="imagenet",
#    include_top=True   # ImageNet-Klassifikator bleibt drin
#)

# letzter Global-Average-Pooling-Layer
#embedding = backbone.layers[-2].output   # shape (None, 2048)
#logits = backbone.output                 # shape (None, 1000)

#model = Model(inputs=backbone.input, outputs=[embedding, logits])


#emb, probs = model(cell_img[None])