import qrcode
import cv2
import csv
import sqlite3

# Create a database connection
conn = sqlite3.connect('attendance.db')

# Create a table to store the student data
cur = conn.cursor()
cur.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    qr_code TEXT
)
''')

# Read the student data from the CSV file
with open('student_data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    # Iterate over the rows in the CSV file
    for row in reader:
        # Create a student object
        student = {}
        student['id'] = row[0]
        student['name'] = row[1]
        student['qr_code'] = qrcode.make(row[1]).png_url()

        # Insert the student data into the database
        cur.execute('''
INSERT INTO students (id, name, qr_code)
VALUES (?, ?, ?)
''', (student['id'], student['name'], student['qr_code']))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

# Create a video capture object
cap = cv2.VideoCapture(0)

# Initialize the attendance data
attendance = []

# Loop until the user presses `Ctrl`+`C`
while True:
    # Capture a frame from the video
    ret, frame = cap.read()

    # Find all QR codes in the frame
    qr_codes = cv2.qrcode.detectMulti(frame)

    # Iterate over the QR codes
    for qr_code in qr_codes:
        # Get the data from the QR code
        data = qr_code.data.decode('utf-8')

        # Check if the data is a student ID
        if data.isdigit():
            # Find the student with the corresponding ID
            student = cur.execute('SELECT * FROM students WHERE id = ?', (data,)).fetchone()

            # If the student is found, mark their attendance
            if student is not None:
                attendance.append((student['id'], student['name']))

    # Display the frame
    cv2.imshow('Attendance System', frame)

    # Check if the user pressed `Esc`
    if cv2.waitKey(1) == 27:
        break

# Close the video capture object
cap.release()

# Close the window
cv2.destroyAllWindows()

# Generate an attendance report
with open('attendance_report.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID', 'Name'])
    for student in attendance:
        writer.writerow(student)


