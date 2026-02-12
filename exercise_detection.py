import cv2
import mediapipe as mp
import numpy as np

# ================= SETTINGS =================
INPUT_VIDEO = "i7.mp4"
OUTPUT_VIDEO = "o7.mp4"
# ============================================

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(INPUT_VIDEO)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

pushup_counter = 0
squat_counter = 0
pushup_stage = None
squat_stage = None

frame_count = 0
angle_buffer = []
knee_buffer = []

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    progress = int((frame_count / total_frames) * 100)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # ===== Choose more visible side =====
        left_sh = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_sh = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        side_prefix = "LEFT" if left_sh.visibility > right_sh.visibility else "RIGHT"

        def L(name):
            return landmarks[getattr(mp_pose.PoseLandmark, f"{side_prefix}_{name}").value]

        shoulder = L("SHOULDER")
        elbow = L("ELBOW")
        wrist = L("WRIST")
        hip = L("HIP")
        knee = L("KNEE")
        ankle = L("ANKLE")

        shoulder_pt = [shoulder.x, shoulder.y]
        elbow_pt = [elbow.x, elbow.y]
        wrist_pt = [wrist.x, wrist.y]
        hip_pt = [hip.x, hip.y]
        knee_pt = [knee.x, knee.y]
        ankle_pt = [ankle.x, ankle.y]

        # ================= PUSHUP =================
        elbow_angle = calculate_angle(shoulder_pt, elbow_pt, wrist_pt)
        body_angle = calculate_angle(shoulder_pt, hip_pt, ankle_pt)

        angle_buffer.append(elbow_angle)
        if len(angle_buffer) > 5:
            angle_buffer.pop(0)

        smoothed_elbow = sum(angle_buffer) / len(angle_buffer)

        if body_angle > 150:
            if smoothed_elbow < 130:
                pushup_stage = "down"

            if smoothed_elbow > 165 and pushup_stage == "down":
                pushup_stage = "up"
                pushup_counter += 1

        # ================= IMPROVED SQUAT =================
        knee_angle = calculate_angle(hip_pt, knee_pt, ankle_pt)

        knee_buffer.append(knee_angle)
        if len(knee_buffer) > 5:
            knee_buffer.pop(0)

        smoothed_knee = sum(knee_buffer) / len(knee_buffer)

        # Standing position
        if smoothed_knee > 165:
            squat_stage = "up"

        # Down position
        if smoothed_knee < 115 and squat_stage == "up":
            squat_stage = "down"
            squat_counter += 1

        # Draw skeleton
        mp_draw.draw_landmarks(frame,
                               results.pose_landmarks,
                               mp_pose.POSE_CONNECTIONS)

        # ===== PRINT ANGLES =====
        cv2.putText(frame, f'Elbow: {int(smoothed_elbow)}',
                    (400, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 0), 2)

        cv2.putText(frame, f'Body: {int(body_angle)}',
                    (400, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 0), 2)

        cv2.putText(frame, f'Knee: {int(smoothed_knee)}',
                    (400, 120), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 2)

    # ================= DISPLAY =================
    cv2.putText(frame, f'Pushups: {pushup_counter}',
                (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0, 255, 0), 2)

    cv2.putText(frame, f'Squats: {squat_counter}',
                (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (255, 0, 0), 2)

    cv2.putText(frame, f'Progress: {progress}%',
                (30, 120), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 255), 2)

    bar_width = int((progress / 100) * width)
    cv2.rectangle(frame,
                  (0, height - 20),
                  (bar_width, height),
                  (0, 255, 0),
                  -1)

    out.write(frame)
    cv2.imshow("Exercise Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("===================================")
print("Processing Completed")
print(f"Total Pushups: {pushup_counter}")
print(f"Total Squats: {squat_counter}")
print("Output saved as:", OUTPUT_VIDEO)
print("===================================")