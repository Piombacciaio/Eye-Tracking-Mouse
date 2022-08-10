#Try to import required libraries, if unable install libraries and restart the program
try:

    import cv2, keyboard as kb, mediapipe as mp, pyautogui as pag

except:

    import os, sys, pip

    pip.main(['install', 'opencv-python'])
    pip.main(['install', 'mediapipe'])
    pip.main(['install', 'pyautogui'])
    os.system("cls")

    self = os.path.basename(sys.argv[0])
    os.system("python " + self)



CAMERA = cv2.VideoCapture(0)
FACE_MESH = mp.solutions.mediapipe.python.solutions.face_mesh.FaceMesh(refine_landmarks=True)
SCREENW, SCREENH = pag.size()

loop = 0
reference_position = None
screenx = 0
screeny = 0

while True:

    if kb.is_pressed('esc'):

        exit(1)

    _, frame = CAMERA.read()
    frame = cv2.flip(frame, 1) #Filp the frame so it's the same as looking in a mirror
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    meshed_frame = FACE_MESH.process(gray_frame)
    frameh, framew, _ = frame.shape

    landmark_coords = meshed_frame.multi_face_landmarks
    
    if reference_position != None:

        cv2.circle(frame, (reference_position[0],reference_position[1]), 2, (255, 0, 0)) #If there is a reference position, draw a blue circle at the location

    if landmark_coords:

        landmarks = landmark_coords[0].landmark 
        for index, landmark in enumerate(landmarks[474:478]): #Locate 4 points around the iris

            x = int(landmark.x * framew)
            y = int(landmark.y * frameh)
            cv2.circle(frame, (x,y), 2, (0, 255, 0)) #Draw a green circle at landmark location

            if index == 1:

                if loop == 0: #At the first run of the loop set the current eye position will be set as the reference position

                    reference_position = [x, y]
                    screenx = int(SCREENW / framew * x) #Convert the position offset from the dimension of the cv2 screen to the actual screen size
                    screeny = int(SCREENH / frameh * y)
                    pag.moveTo(screenx, screeny)
                    loop += 1
                
                elif kb.is_pressed("ctrl+space"): #If this combination is pressed the current eye position will be set as the reference position

                    reference_position = [x, y]

                else:

                    if int(x) - int(reference_position[0]) > 1: #If x value of the eye position is bigger than the x value of the reference position move the cursor 5 pixels up

                        screenx = screenx + 5
                        pag.moveTo(screenx, screeny)
                    
                    if int(x) - int(reference_position[0]) < -1:#If x value of the eye position is smaller than the x value of the reference position move the cursor 5 pixels down

                        screenx = screenx - 5
                        pag.moveTo(screenx, screeny)

                    if int(y) - int(reference_position[1]) > 1: #If y value of the eye position is bigger than the y value of the reference position move the cursor 5 pixels right

                        screeny = screeny + 5
                        pag.moveTo(screenx, screeny)

                    if int(y) - int(reference_position[1]) < -1: #If y value of the eye position is smaller than the y value of the reference position move the cursor 5 pixels left

                        screeny = screeny - 5
                        pag.moveTo(screenx, screeny)

        #Eyelids location
        left_eye = [landmarks[145], landmarks[159]] #Landmark points for top and bottom eyelids of the left eye eye
        for landmark in left_eye:

            x = int(landmark.x * framew)
            y = int(landmark.y * frameh)
            cv2.circle(frame, (x,y), 2, (0, 0, 255)) #Draw a red circle at landmark location

        right_eye = [landmarks[374], landmarks[386]] #Landmark points for top and bottom eyelids of the right eye
        for landmark in right_eye:

            x = int(landmark.x * framew)
            y = int(landmark.y * frameh)
            cv2.circle(frame, (x,y), 2, (0, 0, 255))

        #Blink detection
        #If distance between top and botto eyelid is less than 0.01 (float) trigger the command: 
        # - left click if using left eye (keep close to hold)
        # - right click if using right eye 
        # - middle click if using both eyes
        if left_eye[0].y - left_eye[1].y <= 0.01 and right_eye[0].y - right_eye[1].y > 0.01:

            pag.mouseDown(button="left")

        if left_eye[0].y - left_eye[1].y > 0.01 and right_eye[0].y - right_eye[1].y > 0.01:

            pag.mouseUp(button="left")

        if left_eye[0].y - left_eye[1].y > 0.01 and right_eye[0].y - right_eye[1].y <= 0.01:

            pag.rightClick()

        if left_eye[0].y - left_eye[1].y <= 0.01 and right_eye[0].y - right_eye[1].y <= 0.01:

            pag.middleClick()

    cv2.imshow('eye tracking mouse', frame)
    cv2.waitKey(1)
