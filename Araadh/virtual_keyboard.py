import cv2
import mediapipe as mp
import math
rows = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M"],
    ["SPACE","BACKSPACE", "CLEAR"],
]
red = (0,0,255)
dark = (20,14,11)
white = (255,255,255)
font = cv2.FONT_HERSHEY_COMPLEX

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence =0.7)
camera = cv2.VideoCapture(0)
camera.set(3,1280)
camera.set(4,720)

keys = []
text = ""
was_pinching = False

def build_keys(width,height):
    size = width//13 #how big onekey is
    gap = size // 8 # gap bw two keys
    top = height//4 #how far down the first row will start the would be 720/4 = 180 
    for row_number, row in enumerate(rows):
        if len(row) ==3:
            key_width = size*3+gap*2

        else:
            key_width=size

        row_width = len(row)* key_width + (len(row)-1)* gap
        x = (width-row_width)//2
        y = top+row_number * (size+gap)

        for label in row:
            keys.append((label,x,y,key_width,size))
            x= x+ key_width+gap

def to_pixels(point,width,height):
    return int(point.x*width), int(point.y*height)

def find_keys(px,py):
    for label,x,y,w,h in keys:
        if x<=px <=x +w and y <= py <= y+h:
            return label
    return None

def distance(a,b):
    return math.hypot(a[0]-b[0],a[1]-b[1])
def press(label):
    global text
    if label == "SPACE":
        text = text + " "
    elif label == "BACKSPACE":
        text = text[:-1]

    elif label == "CLEAR":
        text= ""

    else:
        text = text+label
while True:
    success, frame = camera.read()

    if not success:
        print("Cam not working get good (#easter eggs)")
        break

    frame = cv2.flip(frame,1)
    height, width = frame.shape[:2]
    if len(keys) == 0:
        build_keys(width,height)

    rgb  = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    tip = None
    hovered = None
    pinching = False
    if result.multi_hand_landmarks:
        points = result.multi_hand_landmarks[0].landmark
        tip = to_pixels(points[8],width,height)
        hovered = find_keys(tip[0],tip[1])
        thumb = to_pixels(points[4],width,height)
        wrist = to_pixels(points[0],width,height)
        knuckle = to_pixels(points[9],width,height)
        palm = distance(wrist,knuckle)
        if palm>0 and distance(tip,thumb)/palm<0.3:
            pinching=True


    if pinching and not was_pinching and hovered is not None:
        press(hovered)
        print(text)
    was_pinching = pinching
    overlay = frame.copy()
    size = keys[0][4]
    bar_x = keys[0][1]
    bar_y = height//12
    bar_width = width - 2 * bar_x

    cv2.rectangle(overlay,(bar_x,bar_y),(bar_x+bar_width,bar_y+size),dark,-1)

    for label,x,y,w,h in keys:
        colour = dark
        if label == hovered:
            colour = red
            if pinching:
                colour = white
        cv2.rectangle(overlay,(x,y),(x+w,y+h),colour,-1)

    frame = cv2.addWeighted(overlay,0.6,frame,0.4,0)

    cv2.rectangle(frame,(bar_x,bar_y),(bar_x+bar_width,bar_y+size),white,2)
    cv2.putText(frame,text[-28:],(bar_x+20,bar_y+size*2//3),font,size/70,white,2)

    for label,x,y,w,h in keys:
        cv2.rectangle(frame,(x,y),(x+w,y+h),white,2)
        scale = h/80
        text_size = cv2.getTextSize(label,font,scale,2)[0]
        text_x = x+(w-text_size[0])//2
        text_y = y+(h+text_size[1])//2
        letter_colour = white
        if label == hovered and pinching:
            letter_colour = dark
        cv2.putText(frame,label,(text_x,text_y),font,scale,letter_colour,2)

    if tip is not None:
        cv2.circle(frame,tip,12,red,-1)
        if pinching:
            cv2.circle(frame,tip,20,white,3)

    cv2.imshow("Cthru Keyboard",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

