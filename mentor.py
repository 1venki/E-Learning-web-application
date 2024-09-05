import socket
import smtplib
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import mimetypes
import json

# Establish PostgreSQL connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Applemsit_2002",
    host="localhost"
)

def store_registration_data(Data):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reg (first_name, last_name, email, dob, qualification, experience, reason, course) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
                       (Data['firstName'], Data['lastName'], Data['email'], Data['dob'], Data['qualification'], Data['experience'], Data['reason'],Data['course']))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error storing data: {e}")
        return False

def server_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return f'HTTP/1.1 404 NOT FOUND ERROR\n\nFile is not found'.encode()

def parse_post_data(body):
    data = {}
    for pair in body.split("&"):
        key, value = pair.split("=")
        if key == 'email':
            value = value.replace("%40", "@")
            value = value.replace("+", " ")
        data[key] = value
    return data

smtp_host = 'smtp.gmail.com'
smtp_port = 587
smtp_email = 'jpaddalak9999@gmail.com'
smtp_pass = 'xbry vwcw dpdg ratq'

def generate_reference_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_email1(recipient_email, applicant_name, status):
    try:
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_email = 'jpaddalak9999@gmail.com'  # Update with your Gmail address
        smtp_pass = 'xbry vwcw dpdg ratq'  # Update with your Gmail password
        message = MIMEMultipart()
        message['From'] = smtp_email
        message['To'] = recipient_email
        if status == "accept":
            message['Subject'] = 'Course Registration Confirmation'
            body = f"Dear {applicant_name},\n\nCongratulations! Your application has been accepted. We look forward to seeing you soon!\n\nBest regards,\nThe Learning App Team"
        elif status == "reject":
            message['Subject'] = 'Course Registration Rejection'
            body = f"Dear {applicant_name},\n\nWe regret to inform you that your application has been rejected. Thank you for your interest.\n\nBest regards,\nThe Learning App Team"
        message.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(smtp_email, smtp_pass)
        server.sendmail(smtp_email, recipient_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
def send_email(recipient_email, applicant_name):
    try:
        message = MIMEMultipart()
        message['From'] = smtp_email
        message['To'] = recipient_email
        message['Subject'] = 'Course Registration Confirmation'
        reference_id = generate_reference_id()
        body = f"Dear {applicant_name},\n\nThank you for registering for our course. Here is your reference Id: {reference_id}. We look forward to seeing you soon!\n\nBest regards,\nThe Patashala Team"
        message.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_pass)
        text = message.as_string()
        server.sendmail(smtp_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
 
def handle_request(request):
    headers, body = request.split("\r\n\r\n", 1)
    headers = headers.split("\n")
    first_line = headers[0].split()
    method = first_line[0]
    path = first_line[1]

    if 'favicon.ico' in request or len(request) == 0:
        return b''
    # Extract course name from the Referer header if available
    # referer = next((header.split(': ')[1] for header in headers if header.startswith('Referer')), None)
    # if referer and '.html' in referer:
    #     # course_name = parse_course_from_referer(referer)
    # else: 
    #     # Extract course name directly from the path component of the URI
    #     course_name = path.split('/')[-1].replace('.html', '')

    if method =='GET':
        if path=='/':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/homepage.html")
            return header
        elif path=='/mentor-signup':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("signup pages/counselors_signup.html")
            return header
        elif path=='/Student-signup':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("signup pages/Student_signup.html")
            return header
        elif path=='/counselors_signup':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("signup pages/counselors_signup.html")
            return header
        elif path=='/back-home':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/homepage.html")
            return header
        # if path=='/':
        #     header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("mentor's.html")
        #     return header
        elif path == '/student_login':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file('student_login.html')
            return header
        elif path == '/mentor_login':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("mentor's.html")
            return header
        elif path == '/login':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("counselor_loginpage.html")
            return header
        elif path == '/mentor-login':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("mentor's.html")
            return header
        # elif path == '/cspp':
        #     header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("cspp.html")
        #     return header
        elif path.endswith('.js'):
            response = f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n'.encode() + server_file(f'{path[1:].strip()}')
            return response
        elif path.endswith('.jpg'):
            response = f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n'.encode() + server_file(f'home-page{path.strip()}')
            return response
        elif path.endswith('.png'):
            response = f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n'.encode() + server_file(f'home-page{path.strip()}')
            return response
        elif path == '/wad':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("wad.html")
            return header
        elif path == "/join":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("join.html")
                return header
        elif path == "/ics.html":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("ics.html")
            return header
        elif path == "/ads.html":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("ads.html")
            return header
        elif path == "/cspp":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/cspp.html")
            return header
        elif path =="/view_course":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/view_course.html")
            return header
        elif path =="/mentor's.html":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("mentor's.html")
            return header
        elif path =="/mentor_open_page":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/mentor_open_page.html")
            return header
        elif path =="/mentor's":
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("mentor's.html")
            return header
        elif path =="/counselor_loginpage":
                    header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("ars.html")
                    return header
        elif path =="/student/home":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("view_course.html")
                return header
        elif path == "/cspp-c":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/cspp_mentor.html")
                return header
        if path == "/mentor_table":
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT first_name, last_name, course, email FROM mentor")
                mentors = cursor.fetchall()
                cursor.close()
            # Construct HTML response with mentor table data
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("ars.html")
            # Replace placeholders in HTML template with mentor data
                header = header.replace(b'{% for mentor in mentors %}', b'')
                for mentor in mentors:
                    row_html = f"<tr><td>{mentor[0]}</td><td>{mentor[1]}</td><td>{mentor[2]}</td><td>{mentor[3]}</td></tr>"
                    header += row_html.encode()
                header += b'{% endfor %}'
                return header
            except Exception as e:
                print(f"Error fetching mentor data: {e}")
            # If an error occurs, return a 500 response
                return b'HTTP/1.1 500 INTERNAL SERVER ERROR\nContent-Type: text/html\n\nFailed to fetch mentor data'
        elif path == '/api/requests':
            conn = None  # Initialize conn outside the try block
            try:
                conn = psycopg2.connect(
                    dbname="postgres",
                    user="postgres",
                    password="Applemsit_2002",
                    host="localhost"
                )
                # Connect to PostgreSQL database
                cursor = conn.cursor()
                # Execute SQL query to fetch requests
                cursor.execute("SELECT * FROM mentor;")
                requests = cursor.fetchall()
                # Convert requests to JSON format
                requests_list = []
                for request in requests:
                    requests_list.append({
                        'first_name': request[1],
                        'last_name': request[2],
                        'course': request[3],
                        'email': request[4],
                    })
                # Send JSON response
                response = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n'.encode() + json.dumps(requests_list).encode()
            except psycopg2.Error as e:
                print("Error fetching requests:", e)
                error_response = {'error': 'Failed to fetch requests'}
                response = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n'.encode() + json.dumps(error_response).encode()
            finally:
                if conn:
                    cursor.close()
                    conn.close()
            return response
        elif path == '/email':
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("output-accept.html")
            return header
        else:
            # If no valid path is matched, return a 404 response
            response = 'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n'.encode() + b'Page Not Found'
            return response
    elif method == 'POST':
            # if path == "/main-homepage":
            #     header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("homepage.html")
            #     return header
            if path=='/mentor-signup':
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/homepage.html")
                return header
            elif path=='/back-home':
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/homepage.html")
                return header
            elif path == "/tutor-login":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/mentor_open_page.html")
                return header
            elif path == '/student/home':
                header ='HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode()+ server_file("home-page/mentor_open_page.html")
                return header
            elif path == '/tutor/home':
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("output-accept.html")
                return header
            elif path =="/view_course":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/view_course.html")
                return header
            elif path =="/counselor_loginpage":
                    header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("ars.html")
                    return header
            elif path =="/mentor's":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("mentor's.html")
                return header
            elif path =="/student-home":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("view_course.html")
                return header
            elif path =="/student_home":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("student_home.html")
                return header
            elif path == "/cspp":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("home-page/cspp.html")
                return header
            elif path == "/cspp-c":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("cspp_mentor.html")
                return header
            elif path == "/cspp_back":
                header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + server_file("view_course.html")
                return header
            elif path == '/sendemail':
                formData = request.split('\r\n\r\n')[1]
                data = json.loads(formData)
                email = data.get('email')
                name = data.get('first_name')
                course = data.get('course')
                action = data.get('action')
                send_email1(email, name, action)
                #to delete rows
                conn = psycopg2.connect(
                    dbname="postgres",
                    user="postgres",
                    password="Applemsit_2002",
                    host="localhost"
                )
                cur = conn.cursor()
                cur.execute(f"DELETE FROM requests WHERE email = '{email}' AND program = '{formData.get('course')}'")
                conn.commit()            
                cur.close()
                conn.close()
                response = f"HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n".encode()
                return response
            elif path == "/join":
                Data = parse_post_data(body)
                applicant_name = Data.get("firstName") + " " + Data.get("lastName")
                if store_registration_data(Data):
                    email = Data.get("email")
                    send_email(email, applicant_name)
                    try:
                        cursor = conn.cursor()
                        # cursor.execute("INSERT INTO mentor (first_name, last_name, email) VALUES (%s,%s, %s, %s)",
                        #    (Data['firstName'], Data['lastName'],course_name, Data['email']))
                        cursor.execute("INSERT INTO mentor (first_name, last_name, course, email) VALUES (%s, %s, %s, %s)",
                               (Data['firstName'], Data['lastName'],Data['course'], Data['email']))
                        conn.commit()
                        cursor.close()
                    except Exception as e:
                     print(f"Error inserting data into mentor table: {e}")
                    header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode()+ server_file("output.html")
                    return header
                else:
                    # If storing data fails, return a 500 response
                    return b'HTTP/1.1 500 INTERNAL SERVER ERROR\nContent-Type: text/html\n\nFailed to store data'
    else:
        response = 'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n'.encode() + b'Page Not Found'
        return response
    # If no valid method is matched, return a 405 response
    response = 'HTTP/1.1 405 METHOD NOT ALLOWED\nContent-Type: text/html\n\n'.encode() + b'Method Not Allowed'
    return response

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_var = 5432
        server_socket.bind(('localhost', new_var))
        server_socket.listen(1)
        print("Listening on port 5432...")
        while True:
            client_connection, client_address = server_socket.accept()
            request = client_connection.recv(1024).decode()
            response = handle_request(request)
            client_connection.sendall(response)
            client_connection.close()
            print(request)
    except Exception as e:
        print(f"error starting server :{e}" )

if __name__ == '__main__':
    start_server()
