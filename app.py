import flask
from flask import Flask, request, jsonify, session, redirect
from flask_session import Session
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors
import cv2 as cv
import time
import geocoder
import os
import numpy as np
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import random
import geocoder
import json
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)  # Enable CORS for all routes

#code for connect
app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = ''#password
app.config['MYSQL_DB'] = 'pathhole-tracker'#database name

mysql = MySQL(app)
@app.route('/')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    regPhone       = data.get('regPhone')
    regPassword    = data.get('regPassword')
    regName        = data.get('regName')
    regMail        = data.get('regMail')
    
    con = mysql.connect
    con.autocommit(True)
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_details WHERE user_phone = %s', (regPhone,))
    result = cursor.fetchone()
    
    if result:
        msg = '0'
    else:
        #executing query to insert new data into MySQL
        cursor.execute('INSERT INTO user_details VALUES (NULL, % s, % s, % s, % s, %s, NULL)', (regName, regPhone, regMail, regPassword, '',))
        
        msg = '1'
    
    return jsonify({'message': msg})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    signPhone       = data.get('signPhone')
    signPassword    = data.get('signPassword')
    
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_details WHERE user_phone = %s AND user_password = %s', (signPhone, signPassword,))
    result = cursor.fetchone()
    
    if result:
        msg = "1"
        session["userid"]   = result["user_id"]
        session["username"] = result["user_name"]
        session["phone"]    = result["user_phone"]
        session["email"]    = result["user_mail"]
        
        homepage()
    else:
       msg = "0"
    return jsonify({'message': msg})

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return(flask.render_template('homepage.html'))

@app.route('/pathhole', methods=['GET', 'POST'])
def pathhole():
    return(flask.render_template('pathhole.html'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    return(flask.render_template('report.html'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect('http://localhost:3000')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return(flask.render_template('about.html'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return(flask.render_template('contact.html'))

@app.route('/pathholemap', methods=['GET', 'POST'])
def pathholemap():
    return(flask.render_template('pathholemap.html'))

@app.route('/otplogin', methods=['GET', 'POST'])
def otplogin():
    return(flask.render_template('otplogin.html'))

#Pathhole
@app.route('/addquery', methods=['GET', 'POST'])
def addquery():
    if flask.request.method == 'POST':
        userid = session.get("userid")
        query = request.form['query']
        con = mysql.connect
        con.autocommit(True)
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO queries(user_id, query) VALUES('+str(userid)+',"'+query+'")')
        mysql.connect.commit()
    return "1"


#Pathhole
@app.route('/getreports', methods=['GET', 'POST'])
def getreports():
    if flask.request.method == 'POST':
        result = {}
        userid = session.get("userid")
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pathhole_detail_image')
        result = cursor.fetchall();
    return jsonify(result)

#Pathhole
@app.route('/getotp', methods=['GET', 'POST'])
def getotp():
    if flask.request.method == 'POST':
        result = {}
        email = request.form['email']
        con = mysql.connect
        con.autocommit(True)
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE user_mail = "'+email+'"')
        result = cursor.fetchall();
        if result:
            otp = str(random.randint(1000,9999))
            qry2 = "UPDATE user_details SET otp = "+otp+" WHERE user_mail = '"+str(email)+"'"
            updotp = cursor.execute(qry2)
            mysql.connect.commit()
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("manasmishra2401@gmail.com", "tbka fhnh wkfl rkev")
            # Email details
            sender_email_id = "manasmishra2401@gmail.com"
            recipient_email = email
            subject = "OTP for the pathhole detection system!"
            name = result[0]["user_name"]
            
            # Message content
            body = f"Hi Mr./Mrs. {name},\n\nThank you for supporting with Pathhole reporting Service!.\n\nHere is your OTP for the Email Verification: {otp}\n\nRegards,\nTeam Pathhole reporting system"
            
            # Create a MIMEText object
            msg = MIMEMultipart()
            msg['From'] = sender_email_id
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Attach the message body
            msg.attach(MIMEText(body, 'plain'))
            
            # sending the mail
            s.sendmail(sender_email_id, recipient_email, msg.as_string())
            s.quit()
            return jsonify("1")
            
        else:
            return jsonify("2")

@app.route('/verifyotp', methods=['GET', 'POST'])
def verifyotp():
    if flask.request.method == 'POST':
        otp = request.form['otp']
        email = request.form['email']
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE user_mail="'+str(email)+'"AND otp="'+str(otp)+'"')
        result = cursor.fetchone()
        if result:
            session["userid"]   = result["user_id"]
            session["username"] = result["user_name"]
            session["phone"]    = result["user_phone"]
            session["email"]    = result["user_mail"]
            return jsonify("1")
        else:
            return jsonify("0")

#Pathhole
@app.route('/getuserdata', methods=['GET', 'POST'])
def getuserdata():
    if flask.request.method == 'POST':
        result = {}
        userid = session.get("userid")
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE user_id='+str(userid))
        result = cursor.fetchall();
    return jsonify(result) 

#Pathhole
@app.route('/downloadreport', methods=['GET', 'POST'])
def downloadreport():
    if flask.request.method == 'POST':
        result = {}
        lid = request.form['id']
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pathhole_detail_image WHERE pathhole_id='+str(lid))
        result = cursor.fetchall();
    return jsonify(result)

def getusername(passid):
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_details WHERE user_id='+str(passid))
    data = cursor.fetchall();
    result = data[0]
    name = result["user_name"]+" ("+result["user_phone"]+")"
    return name

@app.route('/sendreportmail', methods=['GET', 'POST'])
def sendreportmail():
    if flask.request.method == 'POST':
        result = {}
        lid = request.form['id']
        receiver = request.form['receiver']
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pathhole_detail_image WHERE pathhole_id='+str(lid))
        data = cursor.fetchall();
        result = data[0]
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("manasmishra2401@gmail.com", "tbka fhnh wkfl rkev")
        # Email details
        sender_email_id = "manasmishra2401@gmail.com"
        recipient_email = receiver
        subject = "Mail From Road Pathhole Reporting System"
        sendername = getusername(result["user_id"])
        
        # Message content
        body = f"Hello There,\n\nYou are receiving this mail from pathhole reporting system send by the user {sendername}.\nA pathhole found in the location : {result['location']} and it was reported on : {result['timestamp']}.\n\nThe user commented as : {result['message']}. Kindly takes this as a consideration and the image of the pathhole is attached with this mail.\n\nWith regards,\nTeam Highway Authority"
        
        # Create a MIMEText object
        msg = MIMEMultipart()
        msg['From'] = sender_email_id
        msg['To'] = recipient_email
        msg['Subject'] = subject
        imgpath = 'Static/output/'+result["imagename"]
        with open(imgpath, 'rb') as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        image = MIMEImage(base64.b64decode(image_base64), name='pathhole.jpg', _subtype='jpeg')
        msg.attach(image)
        
        # Attach the message body
        msg.attach(MIMEText(body, 'plain'))
        
        # sending the mail
        s.sendmail(sender_email_id, recipient_email, msg.as_string())
        s.quit()
        
    return jsonify(result)


@app.route('/getpathcoords', methods=['GET', 'POST'])
def getpathcoords():
    if flask.request.method == 'POST':
        result = {}
        lid = request.form['lid']
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pathhole_detail_video WHERE pathhole_id='+str(lid))
        result = cursor.fetchall();
    return jsonify(result)

@app.route('/getlivereports', methods=['GET', 'POST'])
def getlivereports():
    if flask.request.method == 'POST':
        result = {}
        userid = session.get("userid")
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pathhole_detail_video')
        result = cursor.fetchall();
    return jsonify(result)

@app.route('/addpathhole', methods=['GET', 'POST'])
def addpathhole():
    if flask.request.method == 'POST':
       imgname = request.form['imgname']
       location = request.form['location']
       subject = request.form['subject']
       message = request.form['message']
       status = request.form['status']
       userid = session.get("userid")
       
       image_path = 'Static/output/'+imgname
       with open(image_path, 'rb') as image_file:
           imgdata = base64.b64encode(image_file.read()).decode('utf-8')
       
       con = mysql.connect
       con.autocommit(True)
       cursor = con.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('INSERT INTO pathhole_detail_image VALUES (NULL, % s, % s, % s, % s, % s, % s, %s,  NULL)', (userid, location, status, imgname, subject, message, imgdata, ))
       mysql.connect.commit()
    return "1"
       
#Detect function to get the file from app and return to the function 
@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if flask.request.method == 'POST':
       filename = request.form['filename']
       types = request.form['type']
       input_path  = './static/input/'+filename
       output_path = './static/output/detected'+filename
       det = findPathHoles(input_path, output_path)

    toReturn = {"outputfile": filename, "prediction":det}
    return jsonify(toReturn)    

net1 = cv.dnn.readNet('Weights/yolov7_tiny.weights', 'Weights/yolov7_tiny.cfg')
net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
model1 = cv.dnn_DetectionModel(net1)
model1.setInputParams(size=(640, 480), scale=1/255, swapRB=True)


def get_gps_coordinates():
    try:
        # Use the 'geocoder' library to get the current location based on IP address
        location = geocoder.ip('me')
        
        # Extract latitude and longitude from the location
        if location.latlng:
            latitude, longitude = location.latlng
            lanlat = [latitude, longitude]
            return lanlat
        else:
            print("Latitude and longitude not available.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def getlocname(latitude, longitude):
    locname = 'Unknown'
    geolocator = Nominatim(user_agent="reverse_geocoding_example")
    location = geolocator.reverse((latitude, longitude), language='en')
    locname = location.address if location else 'Unknown'
    return locname

@app.route('/livedetect', methods=['GET', 'POST'])
def livedetect():
    sl = get_gps_coordinates() #starting point
    start_loc = getlocname(sl[0], sl[1])
    
    cap = cv.VideoCapture(0)
    pos_coords = []
    neg_coords = []
    last_gps_fetch_time = time.time()
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture a frame from the webcam.")
            break

        # Detect pathholes in the frame
        classes, scores, boxes = model1.detect(frame, confThreshold=0.5, nmsThreshold=0.4)

        # Draw detection boxes on the frame
        if isinstance(classes, tuple):
            ded = 0
            current_time = time.time()
            if current_time - last_gps_fetch_time >= 5:
                gps_coordinates = get_gps_coordinates()
                last_gps_fetch_time = current_time
                pos_coords.append(gps_coordinates)
        else:
            ded = 1
            gps_coordinates = get_gps_coordinates()
            neg_coords.append(gps_coordinates)
                
            for (classid, score, box) in zip(classes, scores, boxes):
                label = "pothole"
                x, y, w, h = box
                recarea = w * h
                area = frame.shape[0] * frame.shape[1]

                if len(scores) != 0 and scores[0] >= 0.7 and (recarea / area) <= 0.1 and box[1] < 600:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    cv.putText(frame, f"%{round(scores[0] * 100, 2)} {label}", (box[0], box[1] - 10),
                               cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

        # Display the frame
        cv.imshow('Live Pathhole Detection', frame)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()
    
    if len(pos_coords) > 0 or len(neg_coords) > 0:
        po_crd = json.dumps(pos_coords)
        ng_crd = json.dumps(neg_coords)
        userid = session.get("userid")
        el = get_gps_coordinates() #starting point
        end_loc = getlocname(sl[0], sl[1])
        con = mysql.connect
        con.autocommit(True)
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO pathhole_detail_video VALUES (NULL, % s, % s, % s, % s, % s,  NULL)', (userid, start_loc, end_loc, ng_crd, po_crd, ))
        mysql.connect.commit()       
    # Release the webcam and close all windows
     
    return jsonify("1")
    
def findPathHoles(input_path, output_path):
    #reading label name from obj.names file
    class_name = []
    #in our case the object that is needsto be detected is pathhole
    with open(os.path.join("Objects",'obj.names'), 'r') as f:
        #Read the name from object file
        class_name = [cname.strip() for cname in f.readlines()]

    #defining the video source (0 for camera or file name for video)
    cap = cv.VideoCapture(input_path) 
    #whenever the video or image file is given it take it as a frame to process
    #get the height and width of the frame
    width  = cap.get(3)
    height = cap.get(4)
    #Create a image or video writer to store detected data
    result = cv.VideoWriter(output_path, 
                             cv.VideoWriter_fourcc(*'MJPG'),
                             10,(int(width),int(height)))

    #defining parameters for result saving and get coordinates
    #defining initial values for some parameters in the script
    g = geocoder.ip('me')
    #Already trained pathholes coordinated
    result_path = "Coordinates"
    #Training constatnsts. Some of the values needs to be passed as paramter to the respoective functions
    starting_time = time.time()
    Conf_threshold = 0.5
    NMS_threshold = 0.4
    #Variab;e initialization
    frame_counter = 0
    i = 0
    b = 0

    #detection loop
    #Until the image/ video frames are read
    while True:
        #Variable initialization for store the frames 
        ret, frame = cap.read()
        #Read next frames 
        frame_counter += 1
        #If frame is not break the loop
        if ret == False:
            break
        #analysis the stream with detection model
        #This will retuen the array which contains the area of pixels where the pathhole detected
        classes, scores, boxes = model1.detect(frame, Conf_threshold, NMS_threshold)
        if type(classes) is tuple:
            ded = 0
        else:
            ded = 1
        print(type(classes))
        #print("Class ", classes)
        #print("scored ", scores)
        #print("boxes ", boxes)
        #Once the pathholedetected draw it over the image
        for (classid, score, box) in zip(classes, scores, boxes):
            label = "pothole"
            #The measure of four sides of rectangle
            x, y, w, h = box
            recarea = w*h
            #Area of ractangle to be draws
            area = width*height
            #drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
            if(len(scores)!=0 and scores[0]>=0.7):
                if((recarea/area)<=0.1 and box[1]<600):
                    cv.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 1)
                    #Writing the text label pathhole and fps into the image frame
                    cv.putText(frame, "%" + str(round(scores[0]*100,2)) + " " + label, (box[0], box[1]-10),cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                    if(i==0):
                        cv.imwrite(os.path.join(result_path,'pothole'+str(i)+'.jpg'), frame)
                        with open(os.path.join(result_path,'pothole'+str(i)+'.txt'), 'w') as f:
                            f.write(str(g.latlng))
                            i=i+1
                    if(i!=0):
                        if((time.time()-b)>=2):
                            cv.imwrite(os.path.join(result_path,'pothole'+str(i)+'.jpg'), frame)
                            with open(os.path.join(result_path,'pothole'+str(i)+'.txt'), 'w') as f:
                                f.write(str(g.latlng))
                                b = time.time()
                                i = i+1
        #writing fps on frame
        endingTime = time.time() - starting_time
        fps = frame_counter/endingTime
        cv.putText(frame, f'FPS: {fps}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)
        #showing and saving result
        cv.imshow('frame', frame)
        result.write(frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        
    #end
    cap.release()
    result.release()
    cv.destroyAllWindows()
    return ded

if __name__ == '__main__':
    app.run(debug=False, port=5000)