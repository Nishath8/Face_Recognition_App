# 🎯 Face Recognition Attendance System

A real-time face recognition-based attendance system using **Streamlit**, **OpenCV**, and the **face_recognition** library. The application enables automatic attendance marking using a live webcam feed. It also provides a secure admin interface to upload new known faces and export attendance data.

---

## 📌 Features

- 🔐 **Admin Login** for secure access
- 📸 **Live webcam face recognition**
- ✅ **Automatic attendance marking** with date and time
- ⬆️ **Upload new known faces** through the UI
- 🧠 Uses `face_recognition` for high-accuracy facial matching
- 📁 **Exports attendance** data to `attendance.csv`
- 🖼️ Real-time camera preview in Streamlit

---

## 🧰 Tech Stack

- **Python 3.10**
- **Streamlit**
- **OpenCV**
- **face_recognition**
- **Dlib**
- **Pillow (PIL)**

---

## 🛠️ Installation


### Clone the repository
```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```
### Create a virtual environment (recommended)
```
python -m venv faceenv
```
### Activate the environment
#### Windows
```
faceenv\Scripts\activate
```
#### macOS/Linux
```
source faceenv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```
# 🚀 Usage
```
streamlit run app.py
```
Once the app launches:

1. Log in as admin to begin recognition

2. Allow access to the webcam when prompted

3. Recognized users will be automatically marked in attendance.csv

# 📂 Project Structure
```
Face_recognition_system/
│
├── app.py                      # Main Streamlit app
├── attendance.csv              # Attendance log file
├── known_faces/                # Directory of user-uploaded images
└── requirements.txt            # Required packages
```
# 👤 Admin Login

- Username: admin
- Password: admin123

# 🔄 How It Works
1. The app loads face encodings from the .pkl model file.

2. Live webcam feed is accessed and frames are scanned for faces.

3. If a match is found, name and timestamp are logged.

4. Admin can upload new face images via the UI.

5. Attendance is saved to attendance.csv.

# 🔐 Privacy Considerations
1. Only face encodings are stored (no raw images).

2. All processing happens locally on your machine.

3. Admin authentication restricts unauthorized changes.

# ✅ Future Improvements
1. Add user roles and permissions

2. Store records in a database (SQLite/MySQL)

3. Add face re-training feature without manual restart

4. Build cross-platform desktop executable

# 🙌 Acknowledgements
Thanks to the developers of face_recognition, dlib, and Streamlit for making real-time facial recognition approachable for developers and researchers alike.
