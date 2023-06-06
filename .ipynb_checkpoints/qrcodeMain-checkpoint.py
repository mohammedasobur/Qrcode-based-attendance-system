import cv2
import pyzbar
import pandas as pd
import qrcode

student_data = pd.read_csv("student_data.csv")

attendance_data = {"Student ID": [], "Attendance": []}

for student_id in student_data["Student ID"]:
    qr_code = qrcode.make(student_id)
    qr_code.save(f"{student_id}.png")
    
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    decoded_objs = pyzbar.decode(frame)
    
for obj in decoded_objs:
    data = obj.data.decode("utf-8")
    qr_type = obj.type
    
    if qr_type == "QRCODE":
        if data in student_data["Student ID"].values:
            if data in attendance_data["Student ID"]:
                print(f"Student with ID {data} is already marked present.")
            else: 
                attendance_data["Student ID"].append(data)
                attendance_data["Attendance"].append("Present")
                print(f"Student with ID {data} is marked present.")
        else:
            print(f"Student with ID {data} is not in the student data.")
            
    cv2.imshow("Attendance System", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

attendance_df = pd.DataFrame(attendance_data)

merged_data = pd.merge(student_data, attendance_df, on="Student ID", how="left")

merged_data ["Attendance"].fillna("Absent", inplace=True)

merged_data.to_csv("attendance_report.csv", index=False)
    
    