import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def kmeans(k=3):
    """Get centers of RGB array, and put labels."""
    cluster = KMeans(n_clusters=k, random_state=0).fit(x)
    centers = cluster.cluster_centers_
    labels = cluster.predict(x)
    return centers, labels


def create(centers, labels, new_file_path="k_new.png"):
    """Replace original picture's pixel with a center value which is nearest to itself.
        So get the new picture."""
    n = np.zeros((H, W, 4))
    idx = 0
    for i in range(H):
        for j in range(W):
            n[i][j] = centers[labels[idx]]
            idx += 1
    img = Image.fromarray(n.astype('uint8')).convert('RGB')
    img.save(new_file_path)


def get_rgb(file_path):
    """Get original picture's RGB array and size."""
    image = Image.open(file_path).convert("RGBA")
    np_image = np.array(image, dtype=np.uint8)
    height, width, _ = np_image.shape
    '''
    width, height = image.size
    rgb_list = []
    for h in range(height):
        for w in range(width):
            r, g, b, _ = image.getpixel((w, h))
            rgb_list.append([r, g, b])
    np_rgb = np.array(rgb_list)
    print(np_rgb.shape)
    '''
    np_rgb = np.reshape(np_image, (width * height, -1))
    return np_rgb, width, height


if __name__ == "__main__":
    x, W, H = get_rgb("./jj.jpg")
    pixel_centers, pixel_labels = kmeans()
    create(pixel_centers, pixel_labels)
