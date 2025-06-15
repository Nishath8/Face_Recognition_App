import streamlit as st
import cv2
import os
import numpy as np
import face_recognition
import datetime
import csv
import hashlib

# --- CONFIGURATION ---
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# --- SESSION STATE INIT ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- FUNCTIONS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

def save_uploaded_face(file, name):
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    os.makedirs(person_dir, exist_ok=True)
    file_path = os.path.join(person_dir, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    st.success(f"Saved face for {name}!")

def load_known_faces():
    known_encodings = []
    known_names = []
    for person_name in os.listdir(KNOWN_FACES_DIR):
        person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)
    return known_encodings, known_names

def mark_attendance(name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(ATTENDANCE_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, timestamp])

def show_camera_preview(known_encodings, known_names):
    st.subheader("🎥 Live Camera Feed")
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
    capture = st.checkbox("Start Camera")

    attendance_marked = set()

    while capture:
        ret, frame = camera.read()
        if not ret:
            st.error("Failed to access camera")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                if name not in attendance_marked:
                    mark_attendance(name)
                    attendance_marked.add(name)
                    st.success(f"✅ Marked attendance for {name}")
                top, right, bottom, left = face_location
                cv2.rectangle(rgb_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(rgb_frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        FRAME_WINDOW.image(rgb_frame)

    camera.release()

# --- UI ---
st.title("🧑🏻‍💻 Face Recognition Attendance System")

menu = st.sidebar.radio("Navigation", ["Login", "Mark Attendance", "Upload New Faces", "View Attendance"])

if menu == "Login":
    st.subheader("🔒 Admin Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")

if menu == "Upload New Faces":
    if not st.session_state.authenticated:
        st.warning("Please login as admin to upload faces.")
    else:
        st.subheader("📤 Upload New Known Faces")
        name = st.text_input("Person's Name")
        uploaded_files = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
        if st.button("Upload"):
            if name and uploaded_files:
                for file in uploaded_files:
                    save_uploaded_face(file, name)
            else:
                st.warning("Provide a name and at least one image.")

if menu == "Mark Attendance":
    st.subheader("📸 Mark Attendance Using Face Recognition")
    known_encodings, known_names = load_known_faces()
    if known_encodings:
        show_camera_preview(known_encodings, known_names)
    else:
        st.warning("No known faces found. Please upload some first.")

if menu == "View Attendance":
    st.subheader("📋 Attendance Records")
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, newline="") as f:
            reader = csv.reader(f)
            data = list(reader)
            st.write("### Total Entries:", len(data))
            st.dataframe(data, use_container_width=True)
    else:
        st.info("No attendance records yet.")
