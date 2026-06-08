 create database student_task_manager;
use student_task_manager;
create table student(
student_id int primary key auto_increment,
first_name varchar(100),
last_name varchar(100),
gender varchar(20),
mobile_number varchar(20),
email varchar(100),
course_name varchar(100),
admission_date date
);

insert into students (
first_name,
last_name,
gender,
mobile_number,
email,
course_name,
admission_date
)
value (
'Chaitany',
'Patil',
'male',
'9876654788',
'chaituu@10.com',
'c++',
curdate()
);

select * from student;

update student
set
gender = 'Male',
mobile_number = '9970245621',
email = 'harish12@gmail.com',
course_name = 'BCA',
admission_date = curdate()
where student_id = 3;


select * from student;
update student
set
email = 'chaitya12@gmail.com',
course_name = 'BCA',
admission_date = curdate()
where student_id = 5;
select * from student;

delete student
set
email = 'chaitya12@gmail.com',
course_name = 'BCA',
admission_date = curdate()
where student_id = 5;
select * from student;

CREATE TABLE attendance
(
	attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    attendance_date DATE,
    attendance_status VARCHAR(50),
    FOREIGN KEY (student_id)
    REFERENCES student(student_id)
    );
    SHOW TABLES;
    
    DESCRIBE attendance;
    
    SELECT
  *
FROM
  `student`;

CREATE TABLE
  `tasks` (
    `task_id` INT PRIMARY KEY AUTO_INCREMENT,
    `task_name` VARCHAR(200),
    `task_description` TEXT,
    `maximum_marks` INT
  );
        
	INSERT INTO tasks
    (
		task_name,
        task_description,
        maximum_marks
        )
	VALUES
    (
		'Python Assignment',
        'Basic Python Practice',
        100
	);
    
        
CREATE TABLE student_tasks
(
	student_task_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    task_id INT,
    obtained_marks INT,
    submission_date DATE,
    FOREIGN KEY (student_id)
    REFERENCES students(student_id),
    FOREIGN KEY (task_id)
    REFERENCES tasks(task_id)
);

show tables;

SELECT * FROM tasks;

ALTER TABLE student_tasks
ADD COLUMN submission_status VARCHAR(50);

ALTER TABLE student_tasks
ADD COLUMN remark TEXT;

SELECT * FROM student_tasks;
DESCRIBE student;
SELECT * FROM report;
SELECT * FROM student_tasks;
	INSERT INTO tasks
    (
		task_name,
        task_description,
        maximum_marks
        )
	VALUES
    (
		'Java',
        'java basic',
        100
	);
    	INSERT INTO tasks
    (
		task_name,
        task_description,
        maximum_marks
        )
	VALUES
    (
		'HTML',
        'Basic HTML Practice',
        100
	);
    
    USE student_task_manager;

CREATE TABLE users
(
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR (100),
    full_name VARCHAR(200)
    );
    
    INSERT INTO users
    (
		username,
        password,
        full_name
	)
    VALUES
    (
		'harish',
        'hari1203',
        'Code Wonders'
	);