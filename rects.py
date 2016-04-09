import cv2

def outlineRect(image, rect, color):
	if rect is None:
		return
	x, y, w, h = rect
	cv2.rectangle(image, (x, y), (x + w, y + h), color)
