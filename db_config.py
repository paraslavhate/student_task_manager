import mysql.connector

def get_database_connection():
    connection = mysql.connector.connect(
        host = 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        user = '3N37LnrfCK8iyhY.root',
        password = 'srPOP9eZVUyj6qJ7',
        database = 'student_task_manager',
        port = 4000
    )

    return connection 