from flask import Flask, render_template, request, redirect,url_for, session

from db_config import get_database_connection

# create flask application
app = Flask(__name__)

app.secret_key ="secret123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method =='POST':
        
        username = request.form['username']
        password = request.form['password']
        
        connection = get_database_connection()
        
        cursor = connection.cursor(dictionary=True)

        
        query = """
            SELECT *
            FROM users
            WHERE username = %s
            AND password = %s
            
        """
        
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            session['user_id'] = user['user_id']
            session['full_name'] = user['full_name']

            return redirect('/')
        
        else:

            return render_template(
                'login.html',
                error='Invalid Username or Password'
            )

    return render_template(
        'login.html',
        error=None
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

@app.route('/')
def home():
    
    if 'user_id' not in session:
        return redirect('/login')
    
    connection = get_database_connection()
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM student")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
        
    
    cursor.close()
    connection.close()
    
    return render_template(
        'index.html',
        total_students=total_students,
        total_attendance=total_attendance,
        total_tasks=total_tasks
    )

# View all students page
@app.route('/students')
def view_students():
   
    connection = get_database_connection()
    
    cursor = connection.cursor(dictionary=True)
   
    cursor.execute("SELECT * FROM student")
    
    students = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('students.html', students=students)


# add student page
@app.route('/add_student/', methods=['GET', 'POST'])
def add_student():
    
    if request.method == 'POST':
       
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        mobile_number = request.form.get('mobile_number')
        email = request.form.get('email')
        course_name = request.form.get('course_name')

        connection = get_database_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO student (
            first_name, last_name, gender, mobile_number, email, course_name, admission_date
        ) VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
       
        """
       
        cursor.execute(query, (first_name, last_name, gender, mobile_number, email, course_name))
        
        connection.commit()
       
        cursor.close()
        connection.close()

        return "student added successfully!!"

    return render_template('add_student.html')

    #edit student page
@app.route('/edit_student/<int:student_id>', methods=['GET','POST'])
def edit_student(student_id):

    #Create database connection
    connection = get_database_connection()

    #Create cursor object
    cursor = connection.cursor(dictionary=True)

    #Check form submission
    if request.method == 'POST':

        #Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        course_name = request.form['course_name']

        #SQL Update Query
        query = """
            UPDATE student
            SET
                first_name = %s,
                last_name = %s,
                gender = %s,
                mobile_number = %s,
                email = %s,
                course_name = %s
            WHERE  student_id = %s
        """

        #Excecute query 
        cursor.execute(
            query,
            (
                first_name,
                last_name,
                gender,
                mobile_number,
                email,
                course_name,
                student_id
            )
        )

        #save changes 
        connection.commit()

        #close connection
        cursor.close

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):

    connection = get_database_connection()
    
    cursor = connection.cursor()

    query = "DELETE FROM student WHERE student_id = %s"

    cursor.execute(query, (student_id))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/student')

@app.route('/attendance')
def attendance():
    
    connection = get_database_connection()
    
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM students")
    
    students = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template(
        'attendance.html',
        students=students
    )
    
@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    
    student_id = request.form['student_id']
    
    
    attendance_status = request.form['attendance_status']
    
    connection = get_database_connection()
    
    cursor = connection.cursor()
    
    query = """
        INSERT INTO attendance
        (
            student_id,
            attendance_date,
            attendance_status
            
        )
        VALUES
        (%s, CURDATE(), %s)
     """
        
    cursor.execute(
        query,
        (
            student_id,
            attendance_status
         )
    )
        
    connection.commit()
        
    cursor.close()
    connection.close()
        
    return redirect('/attendance_report')

@app.route('/attendance_report')
def attendance_report():
    
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    
   
    query = """
        SELECT
            a.attendance_id,
            a.attendance_date,
            a.attendance_status,
            s.first_name,
            s.last_name,
            s.course_name
        FROM attendance a
        INNER JOIN students s 
            ON a.student_id = s.student_id
        ORDER BY a.attendance_id DESC
        """
        
    cursor.execute(query)
    attendance_list = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template(
        'attendance_report.html',
        attendance_records=attendance_list
    )
    
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    
    if request.method == 'POST':
        
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        maximum_marks = request.form['maximum_marks']
        
        connection = get_database_connection()
        
        cursor = connection.cursor()
        
        query = """
            INSERT INTO tasks
            (
                task_name,
                task_description,
                maximum_marks
                
            )
            VALUES
            (%s, %s, %s)
    """
        cursor.execute(
            query,
            (
                task_name,
                task_description,
                maximum_marks
            )
        )  
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return redirect('/tasks') 
    
    return render_template('add_task.html')

@app.route('/tasks')
def tasks():

    connection = get_database_connection()
    
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT *
        FROM tasks
        ORDER BY task_id DESC
    """
    
    cursor.execute(query)
    
    
    task_list = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template(
        'tasks.html',
        tasks=task_list
    )
    
@app.route('/assign_task', methods=['GET', 'POST'])
def assign_task():
    
    connection = get_database_connection()
    
    cursor = connection.cursor(dictionary=True)
    
    if request.method =='POST':
        
        student_id = request.form['student_id']
        task_id = request.form.get('task_id')
        
        obtained_marks = 0
        
        query = """
            INSERT INTO student_tasks
            (
                student_id,
                task_id,
                obtained_marks,
                submission_date
            )
            VALUES
            (%s, %s, %s, CURDATE())
            """
            
        cursor.execute(
                query,
            (
                student_id,
                task_id,
                obtained_marks
            )
        )
            
        connection.commit()
            
        cursor.close()
        connection.close()
        
        return redirect('/student_tasks')
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template(
        'assign_task.html',
        students=students,
        tasks=tasks
    )
        
@app.route('/student_tasks') 
def student_tasks():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT 
            st.student_task_id AS student_task_id, 
            s.first_name, 
            s.last_name, 
            t.task_name, 
            st.obtained_marks, 
            st.submission_date
        FROM student_tasks st
        LEFT JOIN students s ON st.student_id = s.student_id
        LEFT JOIN tasks t ON st.task_id = t.task_id
        ORDER BY st.student_task_id DESC
    """
    
    cursor.execute(query)
    task_list = cursor.fetchall()
    
    print("--- DATABASE RECORDS ---")
    print(task_list)
    
    cursor.close()
    connection.close()
    
    return render_template(
        'student_tasks.html',   
        task_records=task_list
    )
    
    # Student performance report
@app.route('/performance_report')
def performance_report():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query with GROUP BY and aggregate functions
    query = """
        SELECT

            students.student_id,
            students.first_name,
            students.last_name,
            students.course_name,

            COUNT(student_tasks.student_task_id)
                AS total_tasks,

            SUM(student_tasks.obtained_marks)
                AS total_marks,

            AVG(student_tasks.obtained_marks)
                AS average_marks,

            SUM(
                CASE
                    WHEN student_tasks.submission_status = 'Submitted'
                    THEN 1
                    ELSE 0
                END
            ) AS submitted_tasks

        FROM students

        LEFT JOIN student_tasks
            ON students.student_id = student_tasks.student_id

        GROUP BY
            students.student_id,
            students.first_name,
            students.last_name,
            students.course_name

        ORDER BY total_marks DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch report data
    performance_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load report page
    return render_template(
        'performance_report.html',
        performance_records=performance_records
    )

# Attendance summary report
@app.route('/attendance_summary')
def attendance_summary():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL summary query
    query = """
        SELECT

            attendance_date,

            COUNT(attendance_id)
                AS total_records,

            SUM(
                CASE
                    WHEN attendance_status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS total_present,

            SUM(
                CASE
                    WHEN attendance_status = 'Absent'
                    THEN 1
                    ELSE 0
                END
            ) AS total_absent,

            SUM(
                CASE
                    WHEN attendance_status = 'Leave'
                    THEN 1
                    ELSE 0
                END
            ) AS total_leave

        FROM attendance

        GROUP BY attendance_date

        ORDER BY attendance_date DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch records
    attendance_summary_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'attendance_summary.html',
        attendance_summary_records=attendance_summary_records
    )
   
if __name__ == '__main__' :

    app.run(debug=True)
    