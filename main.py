import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

# Hand detector
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1,
                        detectionCon=0.7, minTrackCon=0.5)

gemini_answer = "Waiting for input..."
prev_pos = None
canvas = None

def getHandInfo(img):
    hands, img = detector.findHands(img, draw=False, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    else:
        return None

def draw(info, prev_pos, canvas, img):
    fingers, lmlist = info
    current_pos = None

    if fingers == [0, 1, 0, 0, 0]:  # Index finger up
        current_pos = lmlist[8][0:2]
        if prev_pos is None:
            prev_pos = current_pos
        cv2.line(canvas, prev_pos, current_pos, color=(0, 0, 255), thickness=12)
        prev_pos = current_pos
    elif fingers == [1, 0, 0, 0, 0]:  # Thumb up clears canvas
        canvas = np.zeros_like(img)
    return current_pos, canvas

def sendToAI(model, canvas, fingers):
    global gemini_answer
    if fingers == [0, 1, 1, 1, 0]:  # Index, middle, ring up
        try:
            pil_image = Image.fromarray(canvas)
            response = model.generate_content([
                "Solve the math equation in this image.",
                pil_image
            ])
            gemini_answer = response.text or "No response received."
        except Exception as e:
            gemini_answer = f"Error: {str(e)}"

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    img = cv2.flip(img, 1)

    if canvas is None:
        canvas = np.zeros_like(img)

    info = getHandInfo(img)
    if info:
        fingers, lmlist = info

        # Display finger status
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        status = ['Up' if val else 'Down' for val in fingers]
        for i, (name, stat) in enumerate(zip(finger_names, status)):
            cv2.putText(img, f"{name}: {stat}", (10, 50 + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        prev_pos, canvas = draw(info, prev_pos, canvas, img)
        sendToAI(model, canvas, fingers)
    else:
        prev_pos = None

    # Combine canvas with camera feed
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img_combined = cv2.bitwise_and(img, img_inv)
    img_combined = cv2.bitwise_or(img_combined, canvas)

    # Right panel for Gemini output
    right_panel = np.ones((720, 400, 3), dtype=np.uint8) * 255
    y0 = 50
    for i, line in enumerate(gemini_answer.split('\n')):
        y = y0 + i * 30
        cv2.putText(right_panel, line[:50], (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Resize left and join panels
    left_panel = cv2.resize(img_combined, (880, 720))
    final_ui = np.hstack((left_panel, right_panel))

    cv2.imshow("Smart Canvas + Gemini Assistant", final_ui)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
