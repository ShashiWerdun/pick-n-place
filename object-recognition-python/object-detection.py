import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# define paths and constants
WORKSPACE_IMG_PATH = r'../workspace-images/sample-3.jpeg'

# function to show image in a new window using cv2
def show_image(image, image_name=''):
    cv.imshow(image_name, image)
    cv.waitKey(0)
    cv.destroyAllWindows()

# function to detect and extract individual object images and centroid
def get_object_data(path=WORKSPACE_IMG_PATH):
    # store image of workspace at each phase in a dictionary
    workspace_imgs = {}

    # load grayscale image
    grayscale_img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    workspace_imgs['grayscale image'] = grayscale_img

    # convert image to binary
    threshold, binary_image = cv.threshold(grayscale_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    workspace_imgs['binary image'] = binary_image
    
    # detect edges in binary image
    edge_image = cv.Canny(binary_image, 100, 70)
    workspace_imgs['edge detected image'] = edge_image

    # create a 5x5 kernel and perform image dilation
    kernel = np.ones((5, 5), np.uint8)
    dilated_image = cv.dilate(edge_image, kernel, iterations=1)
    workspace_imgs['dilated image'] = dilated_image

    # create contours for individual objects
    contours, hierarchy = cv.findContours(dilated_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour_image = grayscale_img.copy()
    contours = [contour for contour in contours if cv.contourArea(contour)>1000]
    cv.drawContours(contour_image, list(contours), -1, color=(0, 0, 255), thickness=5)
    workspace_imgs['contour image'] = contour_image

    # find bounding boxes for cropping individual object
    bboxes = [cv.boundingRect(contour) for contour in contours]
    bbox_image = grayscale_img.copy()
    for bbox in bboxes:
        cv.rectangle(bbox_image, bbox, (0, 0, 256), 4)
    workspace_imgs['bounding box image'] = bbox_image

    # individual object images
    object_images = [grayscale_img[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]].copy() for bbox in bboxes]

    # find centroid of each object using it's contour
    centroids = []
    for contour in contours:
        M = cv.moments(contour)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        centroids.append((cx, cy))

    # combine all image data into a dictionary
    objects_data = {'image':object_images, 'bbox':bboxes, 'centroid':centroids}

    # create a dataframe from the object data
    objects_df = pd.DataFrame(data=objects_data)

    # draw centroids
    centroid_image = grayscale_img.copy()
    for point in objects_df['centroid']:
        cv.circle(centroid_image, (int(point[0]), int(point[1])), 1, (0, 0, 256), 5)
    workspace_imgs['image with centroids of objects'] = centroid_image

    # return workspace images and object dataframe
    return workspace_imgs, objects_df

# show workspace images at every phase
def display_workspace_phases(images):
    # create a figure
    fig = plt.figure()
    cols = 3
    rows = int(len(images) / 3 + 1)

    # add all images as subplots
    for i, (phase, image) in enumerate(images.items()):
        fig.add_subplot(rows, cols, i+1)
        plt.imshow(image, cmap='gray')
        plt.title(phase)
        plt.axis('off')