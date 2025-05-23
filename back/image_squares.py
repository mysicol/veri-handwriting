import cv2
import easyocr
import numpy as np
import sys

def get_cropped_image(x, y, w, h, image=None):
    return image[y:y+h, x:x+w]

def display_cropped_image(x, y, w, h, title="dontcare", image=None):
    cv2.imshow(title, image[y:y+h, x:x+w])
    cv2.waitKey(0)

def rotate_contour(contour, image):
    rect = cv2.minAreaRect(contour)
    angle = rect[2]
    if angle < -45:
        angle += 90
    else:
        angle = -angle

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)

    rotated_contour = np.zeros_like(image)
    cv2.drawContours(rotated_contour, [contour], -1, 255, cv2.FILLED)
    rotated_contour = cv2.warpAffine(rotated_contour, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # rotated_contour = cv2.cvtColor(rotated_contour, cv2.COLOR_GRAY2BGR)

    return rotated_contour

def has_markings(rect):
    """Checks if a given rectangle area contains markings."""
    gray_roi_full = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)

    gray_roi = get_cropped_image(20, 20, gray_roi_full.shape[1] - 40, gray_roi_full.shape[0] - 40, gray_roi_full)

    # Compute mean pixel intensity
    mean_intensity = cv2.mean(gray_roi)[0]  

    # Apply edge detection
    edges = cv2.Canny(gray_roi, 50, 150)
    edge_count = np.count_nonzero(edges)  # Count nonzero edge pixels

    print(f"Mean intensity: {mean_intensity}, Edge count: {edge_count}")
    # cv2.imshow("gray", gray_roi)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    # Thresholds to determine if it's a marked rectangle
    return edge_count > 100

def rotate_image(image, angle):
    """Rotates an image by the given angle while keeping the full image in view."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Compute the new bounding dimensions
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to account for translation
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Perform the rotation
    rotated = cv2.warpAffine(image, M, (new_w, new_h))
    
    return rotated

def sort_key(square, thresh):
        x, y, w, h = cv2.boundingRect(square)
        return (y // thresh, x)

def get_image_squares(image):

    ################################# RAW IMAGE STRAIGTENING PROC #################################

    # image = cv2.imread("image4.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # Define size limits
    min_area = 1000       # Smallest marker we accept
    max_area = 100000     # Largest marker (adjust based on your image)

    # Dictionary to store potential markers (outer square -> inner square count)
    markers = []

    # print(len(contours))

    totalAngle = 0
    totalCount = 0

    # Identify potential marker candidates
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(approx)

        # Check if it's a quadrilateral and within size limits
        if len(approx) == 4 and min_area < area < max_area:
            markers.append(approx)
            x, y, w, h = cv2.boundingRect(approx)
            rect_angle = cv2.minAreaRect(approx)[2]
            if (rect_angle > 45):
                rect_angle -= 90
            totalAngle += rect_angle
            totalCount += 1

            # print(f"w: {w}, h: {h}, a: {rect_angle}")
            # display_cropped_image(x, y, w, h, "Contour", image)
        elif len(approx) == 4:
            print(f"Rejected contour area: {area}")

    print(f"Average angle: {totalAngle / totalCount}")

    rotated = rotate_image(image, (totalAngle / totalCount))

    ################################################################################################

    ############################## STRAIGHTENED IMAGE PROC ########################################
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

    # # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # Define size limits
    min_area = 200000       # Smallest marker we accept
    max_area = 1000000000     # Largest marker (adjust based on your image)

    # Dictionary to store potential markers (outer square -> inner square count)
    markers = []
    main_contour = []

    # Identify potential marker candidates
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(approx)

        # Check if it's a quadrilateral and within size limits
        if len(approx) == 4 and min_area < area < max_area:
            main_contour.append(approx)
            x, y, w, h = cv2.boundingRect(approx)
            y = y - 10
            h = h + 20
            x = x - 10
            w = w + 20
            rect_angle = cv2.minAreaRect(approx)[2]
            cropped_full = get_cropped_image(x, y, w, h, rotated)
            # cv2.imshow("test", cropped_full)
            # cv2.waitKey(0)
        # elif len(approx) == 4:
        #     print(f"Rejected contour area: {area}")


    ################################################################################################



    gray = cv2.cvtColor(cropped_full, cv2.COLOR_BGR2GRAY)

    # # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY_INV, 11, 2)


    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # Define size limits
    min_area = 10000       # Smallest marker we accept
    max_area = 100000     # Largest marker (adjust based on your image)

    marked_squares = []

    totalAngle = 0
    totalCount = 0

    # Identify potential marker candidates
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(approx)

        # Check if it's a quadrilateral and within size limits
        if len(approx) == 4 and min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(approx)

            cropped = get_cropped_image(x, y, w, h, cropped_full)
            # cv2.imshow("a", cropped)
            # cv2.waitKey(0)
            marked = has_markings(cropped)
            # print(marked)

            if marked:
                marked_squares.append(approx)
                # cv2.imshow("test", cropped)
                # cv2.waitKey(0)
            
            # cv2.imshow("test", cropped)
            # cv2.waitKey(0)

        elif len(approx) == 4:
            print(f"Rejected contour area: {area}")

    print(f"Total detected contours: {len(contours)}")
    print(f"Filtered contours: {len(marked_squares)}")

    # Sort the marked_squares list by their top-left corner (x, y) coordinates


    total_width = sum(cv2.boundingRect(square)[2] for square in marked_squares)
    max_height = max(cv2.boundingRect(square)[3] for square in marked_squares)
    min_height = min(cv2.boundingRect(square)[3] for square in marked_squares)

    sorting_key = lambda square: sort_key(square, min_height - 50)

    marked_squares = sorted(marked_squares, key=sorting_key)

    print(min_height)

    canvas = np.zeros((max_height, total_width, 3), dtype=np.uint8)

    current_x = 0

    cropped_images = []

    for square in marked_squares:
        x, y, w, h = cv2.boundingRect(square)
        cropped = get_cropped_image(x, y, w, h, cropped_full)
        cropped_images.append(cropped)

        canvas[0:h, current_x:current_x + w] = cropped
        current_x += w

    # cv2.imshow("Marked Squares", canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return cropped_images

def characters_from_np(img):
    return get_characters(cv2.imdecode(img, cv2.IMREAD_COLOR))

def get_characters(image):
    squares = get_image_squares(image)

    reader = easyocr.Reader(["en"])
    
    characters = []
    for i in range(len(squares)):
        square = squares[i]
        results = reader.readtext(squares[i], allowlist='abcdefghijklmnopqrstuvwxyz')

        character = " "
        if len(results) > 0:
            character = results[0][1]
            if len(character) > 1:
                character = character[0]
        print(character)
        characters.append((cv2.resize(square, (40, 40)), character))

    return characters

if __name__ == "__main__":
    if len(sys.argv) < 2:
        image_path = "image.jpg"
    else:
        image_path = sys.argv[1]

        image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        sys.exit(1)

    print(get_characters(image))