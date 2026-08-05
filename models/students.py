'''
    Database SQL models for Students route.
    This models file includes the following funcion:
        – VIEWS
        – ADD STUDENT
        – EDIT STUDENT
        – DELETE STUDENT
        – SEARCH
'''
from src.database import db_connection
import pymysql.cursors


class student_M:

    # Display all students
    def display_Students():
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''
                    SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    '''
        cursor.execute(SqlQuery)
        students = cursor.fetchall()
        db.close()
        cursor.close()
        return students

    #idNumber Checking
    def check_idNumber_Dict(idNumber):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT students.idNumber FROM students WHERE idNumber = %s'''
        cursor.execute(SqlQuery, idNumber)
        idNumber_unique = cursor.fetchone()
        db.close()
        cursor.close()
        return idNumber_unique

    # Display all courses
    def display_Courses():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT * FROM course_table'''
        cursor.execute(SqlQuery)
        courses = cursor.fetchall()
        db.close()
        cursor.close()
        return courses

    # Display courses alongside colleges
    def display_course_college():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT course_table.courseCode, college_table.collegeName
        FROM course_table RIGHT JOIN college_table ON college_table.collegeCode = course_table.collegeCode'''
        cursor.execute(SqlQuery)
        courses_colleges = cursor.fetchall()
        db.close()
        cursor.close()
        return courses_colleges

    # Add student into the database
    def add_Students(idNumber, firstName, lastName, courseCode, yearLevel, gender):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''INSERT INTO students(idNumber, firstName,
            lastName, courseCode, yearLevel, gender)  VALUES (%s, %s, %s, %s, %s, %s)'''
        SqlValues = (idNumber, firstName, lastName,
                                courseCode, yearLevel, gender)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Add student with a photo into the database
    def add_Students_p(idNumber, firstName, lastName, courseCode, yearLevel, gender, image):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''INSERT INTO students(idNumber, firstName,
            lastName, courseCode, yearLevel, gender, image_id)  VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        SqlValues = (idNumber, firstName, lastName,
                                courseCode, yearLevel, gender, image)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Delete a student from the database
    def delete_Student(students_id):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = "DELETE FROM students WHERE students_id = %s"
        SqlValues = (students_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Edit a student information from the datbase
    def edit_Student(firstNameEdit, lastNameEdit,
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''UPDATE students SET firstName=%s, lastName=%s,
                        courseCode=%s, yearLevel=%s, gender=%s WHERE students_id=%s'''
        SqlValues = (firstNameEdit, lastNameEdit,
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Edit a student information with a photo from the database
    def edit_Student_p(firstNameEdit, lastNameEdit,
                            courseCodeEdit, yearLevelEdit, genderEdit, image, student_id):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''UPDATE students SET firstName=%s, lastName=%s,
                        courseCode=%s, yearLevel=%s, gender=%s, image_id=%s WHERE students_id=%s'''
        SqlValues = (firstNameEdit, lastNameEdit,
                            courseCodeEdit, yearLevelEdit, genderEdit, image, student_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()

    @staticmethod
    def filter_search(course_key_Code=None,
                      student_key_Gender=None,
                      student_key_Level=None):

        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        sql = """
            SELECT
                students.students_id,
                students.idNumber,
                students.firstName,
                students.lastName,
                students.courseCode,
                students.course_id,
                students.yearLevel,
                students.gender,
                students.image_id,
                COALESCE(college_table.collegeName,'N/A') AS collegeName
            FROM students
            LEFT JOIN course_table
                ON students.courseCode = course_table.courseCode
            LEFT JOIN college_table
                ON course_table.collegeCode = college_table.collegeCode
            WHERE 1=1
        """

        values = []

        if course_key_Code:
            sql += " AND students.courseCode = %s"
            values.append(course_key_Code)

        if student_key_Gender:
            sql += " AND students.gender = %s"
            values.append(student_key_Gender)

        if student_key_Level:
            sql += " AND students.yearLevel = %s"
            values.append(student_key_Level)

        cursor.execute(sql, tuple(values))
        data = cursor.fetchall()

        cursor.close()
        db.close()

        return data


    @staticmethod
    def search_combine(course_key_Code=None,
                       student_key_Level=None,
                       student_key_Gender=None):

        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        sql = """
            SELECT
                students.students_id,
                students.idNumber,
                students.firstName,
                students.lastName,
                students.courseCode,
                students.course_id,
                students.yearLevel,
                students.gender,
                students.image_id,
                COALESCE(college_table.collegeName,'N/A') AS collegeName
            FROM students
            LEFT JOIN course_table
                ON students.courseCode = course_table.courseCode
            LEFT JOIN college_table
                ON course_table.collegeCode = college_table.collegeCode
            WHERE 1=1
        """

        values = []

        if course_key_Code:
            sql += " AND students.courseCode = %s"
            values.append(course_key_Code)

        if student_key_Level:
            sql += " AND students.yearLevel = %s"
            values.append(student_key_Level)

        if student_key_Gender:
            sql += " AND students.gender = %s"
            values.append(student_key_Gender)

        cursor.execute(sql, tuple(values))
        data = cursor.fetchall()

        cursor.close()
        db.close()

        return data


    @staticmethod
    def search_Student(student_key,
                       course_key_Code=None,
                       student_key_Level=None,
                       student_key_Gender=None):

        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        sql = """
            SELECT
                students.students_id,
                students.idNumber,
                students.firstName,
                students.lastName,
                students.courseCode,
                students.course_id,
                students.yearLevel,
                students.gender,
                students.image_id,
                COALESCE(college_table.collegeName,'N/A') AS collegeName
            FROM students
            LEFT JOIN course_table
                ON students.courseCode = course_table.courseCode
            LEFT JOIN college_table
                ON course_table.collegeCode = college_table.collegeCode
            WHERE
            (
                students.idNumber LIKE %s OR
                students.firstName LIKE %s OR
                students.lastName LIKE %s
            )
        """

        values = [
            f"%{student_key}%",
            f"%{student_key}%",
            f"%{student_key}%"
        ]

        if course_key_Code:
            sql += " AND students.courseCode = %s"
            values.append(course_key_Code)

        if student_key_Level:
            sql += " AND students.yearLevel = %s"
            values.append(student_key_Level)

        if student_key_Gender:
            sql += " AND students.gender = %s"
            values.append(student_key_Gender)

        cursor.execute(sql, tuple(values))
        data = cursor.fetchall()

        cursor.close()
        db.close()

        return data