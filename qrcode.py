import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    data, bbox, _ = detector.detectAndDecode(frame)

    if bbox is not None:
        for i in range(len(bbox)):
            pt1 = tuple(map(int, bbox[i][0]))
            pt2 = tuple(map(int, bbox[(i+1) % len(bbox)][0]))
            cv2.line(frame, pt1, pt2, (255,0,0), 2)

        if data:
            pt = tuple(map(int, bbox[0][0]))
            cv2.putText(frame, data, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            print("QR Code detected:", data)

    cv2.imshow("QR Code Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

