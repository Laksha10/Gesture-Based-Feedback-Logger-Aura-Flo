import cv2
import numpy as np
import mediapipe as mp
import time
from stage2_audio_whisper import record_and_transcribe  # 🔗 Voice integration
from feedback_logger import init_db, save_feedback
init_db()

# Mediapipe Pose setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

TRIGGER_THRESHOLD = 0.13
DEBOUNCE_SECONDS = 2
EMA_ALPHA = 0.2  # Smoothing factor

last_trigger_time = 0
cooldown_active = False
last_frame_time = time.time()
smoothed_dist = None
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Failed to open camera")
    exit()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    print("📷 Camera stream started. Press 'q' to quit.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("❌ Empty frame received. Exiting.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            def get_coords(idx):
                lm = landmarks[idx]
                return np.array([lm.x, lm.y]) if lm.visibility > 0.5 else None

            lw = get_coords(mp_pose.PoseLandmark.LEFT_WRIST.value)
            rw = get_coords(mp_pose.PoseLandmark.RIGHT_WRIST.value)
            ls = get_coords(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
            rs = get_coords(mp_pose.PoseLandmark.RIGHT_SHOULDER.value)

            if all(val is not None for val in [lw, rw, ls, rs]):
                lw_dist = np.linalg.norm(lw - ls)
                rw_dist = np.linalg.norm(rw - rs)
                avg_dist = (lw_dist + rw_dist) / 2

                # Apply exponential moving average smoothing
                if smoothed_dist is None:
                    smoothed_dist = avg_dist
                else:
                    smoothed_dist = EMA_ALPHA * avg_dist + (1 - EMA_ALPHA) * smoothed_dist

                now = time.time()

                if not cooldown_active and smoothed_dist < TRIGGER_THRESHOLD:
                    print(f"✅ GESTURE TRIGGERED — Avg dist: {smoothed_dist:.3f}")
                    last_trigger_time = now
                    cooldown_active = True
                    cv2.putText(frame, "✅ Triggered", (10, 80), font, 1, (0, 255, 0), 2)

                    # 🔊 Voice input starts here
                    user_feedback = record_and_transcribe()
                    print("📥 Final Transcription:", user_feedback)
                    save_feedback(user_feedback, smoothed_dist)
                else:
                    print(f"❌ No trigger — dist too high: {smoothed_dist:.3f}")
                    cv2.putText(frame, f"❌ Not triggered: {smoothed_dist:.3f}", (10, 80), font, 0.8, (0, 0, 255), 2)
                
                if cooldown_active and (now - last_trigger_time > DEBOUNCE_SECONDS):
                    cooldown_active = False
                    print("🔄 Cooldown ended. Ready for next gesture.")
            else:
                print("⚠️ Some landmarks missing, skipping frame")
                cv2.putText(frame, "⚠️ Incomplete landmarks", (10, 80), font, 0.8, (0, 165, 255), 2)

            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
            )
        else:
            print("❌ No pose landmarks detected.")
            cv2.putText(frame, "❌ No landmarks", (10, 80), font, 0.8, (0, 0, 255), 2)

        fps = 1 / (time.time() - last_frame_time)
        last_frame_time = time.time()
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 40), font, 0.8, (255, 255, 255), 2)

        cv2.imshow("Gesture Trigger Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 Exiting...")
            break

cap.release()
cv2.destroyAllWindows()
