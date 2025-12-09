import cv2
import numpy as np

# Path to your image
image_path = "slant2.png" 

# Load the image
img = cv2.imread(image_path)
print(img.shape)


fx_factor = 1 #0.25 # Scale by 50% horizontally
fy_factor = 1 #0.25 # Scale by 50% vertically

resized_image = cv2.resize(img, None, fx=fx_factor, fy=fy_factor)

print(resized_image.shape)

if img is None:
    print("Failed to load image:", image_path)
    exit()

# Initialize the QRCode detector
detector = cv2.QRCodeDetector()

# Detect and decode
data, bbox, s_img = detector.detectAndDecode(resized_image)

if bbox is not None:
    # Convert bbox to integer numpy array for safety
    bbox = np.array(bbox, dtype=int).reshape(-1, 2)

    # Compute width and height
    x_coords = bbox[:,0]
    y_coords = bbox[:,1]
    width = max(x_coords) - min(x_coords)
    height = max(y_coords) - min(y_coords)

    if width >= 60 and height >= 60:
        # Draw bounding box
        for i in range(len(bbox)):
            pt1 = tuple(bbox[i])
            pt2 = tuple(bbox[(i+1) % len(bbox)])
            cv2.line(resized_image, pt1, pt2, (255,0,0), 2)

        # Show decoded text
        if data:
            pt = tuple(bbox[0])
            cv2.putText(resized_image, data, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            print("QR Code detected:", data)
    else:
        print(f"QR code too small: {width}x{height}")
else:
    print("No QR code found in the image.")

print("Bounding box: ", bbox)

# Display the image with bounding box
cv2.imshow("QR Code Reader", resized_image)
cv2.imshow("QR Corrected", s_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

