% load image and close all previous images
close all
rgb = imread('./inputs/sample-2.jpeg');
figure
imshow(rgb);

% convert to grayscale
grayscale = rgb2gray(rgb);
figure
imshow(grayscale);

% convert to binary
level = graythresh(grayscale);
disp(level);
binary = imbinarize(grayscale, level);
figure
imshow(binary);

% edge detection using Canny Method
edges = edge(binary, 'canny');
figure
imshow(edges);

% image dilation
se = strel('line',11,90);
dilated = imdilate(edges, se);
figure
imshow(dilated);

% image filling
filled = imfill(dilated, "holes");
figure
imshow(filled);


% BLOB analysis

% Define thresholds
channel1Min = 1;
channel1Max = 1;

% Create mask
sliderBW = (filled(:,:,1) >= channel1Min ) & (filled(:,:,1) <= channel1Max);
BW = sliderBW;

figure
imshow(BW)

noise = strel('disk' , 3);

open = imopen(BW, noise);
figure
imshow(open);

blob = vision.BlobAnalysis('MinimumBlobArea', 200, 'MaximumBlobArea', 1000000);
[objectArea, objCentroid, bboxout] = step(blob, open);
rectangle = insertShape(rgb, 'rectangle', bboxout, 'Linewidth', 4, 'Color', [155 164 155]);
figure
imshow(rectangle)

% extract objects from the original image by cropping
for n = 1:size(bboxout, 1)
    object_image = imcrop(rgb, bboxout(n, :));
    object_name = append('./outputs/object-', string(n), '.jpeg');
    imwrite(object_image, object_name);
end