from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
import pymysql.cursors
from config import SECRET_KEY
from src.database import db_connection
from models.courses import course_M
#from models.students import student_M



courses_bp = Blueprint("Cbp", __name__,  template_folder='/templates')


#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COURSES STARTS IN HERE.#
#<-------------------------------------------------->#

@courses_bp.route('/courses')
def courses():

    course_data = list(course_M.display_Courses())
    course_data.reverse()

    college_data = course_M.display_Colleges()

    # KEEP ALL COURSES FOR FILTERS
    filter_courses = course_data

    total_courses = len(course_data)

    page = request.args.get('page', 1, type=int)
    per_Page = 10

    start_Page = (page - 1) * per_Page
    end_Page = start_Page + per_Page

    # ONLY FOR TABLE
    courses_on_Page = course_data[start_Page:end_Page]


    total_Pages = (total_courses + per_Page - 1) // per_Page
    page_Number = list(range(1, total_Pages + 1))


    return render_template(
        '/courses/courses.html',
        Courses=courses_on_Page,
        FilterCourses=filter_courses,
        Colleges=college_data,
        page=page,
        number_of_Pages=page_Number,
        total_Pages=total_Pages
    )

#For editing/updating the course information
@courses_bp.route('/edit_course', methods = ["POST"])
def edit_course():
    if request.method == "POST":
        print('successfully edited the select item')
        course_id = request.form['course_id']
        courseCodeEdit = request.form['courseCodeEdit']
        courseNameEdit = request.form['courseNameEdit']
        collegeCodeEdit =  request.form['collegeCodeEdit']

        unique_courseCode = course_M.check_courseCode(courseCodeEdit)
        unique_courseName = course_M.check_courseName(courseNameEdit)
        unique_collegeCode = course_M.check_collegeCode(collegeCodeEdit)

        if len(courseCodeEdit) < 1:
            flash("You need to input valid course code!", category='error')

        elif len(courseNameEdit) < 1:
            flash("You need to input valid course name!", category='error')

        elif unique_courseName and unique_courseCode and unique_collegeCode:
            flash("Course already exists!", category='error')

        elif not unique_courseName and unique_courseCode and not unique_collegeCode:
            flash("Course already exists!", category='error')

        else:
            # Implement add function for proper string formatting.
            capt_courseCodeEdit = courseCodeEdit.upper()
            capt_courseNameEdit = courseNameEdit.title().replace('Of', 'of').replace("In", "in")
            course_M.edit_Course(capt_courseCodeEdit, capt_courseNameEdit, collegeCodeEdit, course_id)
            flash("you have successfully edited the course information!", category='success')
    return redirect(url_for('Cbp.courses'))

#For adding a new course information
@courses_bp.route('/add_course', methods=["GET","POST"])
def add_course():
    if request.method == "POST":
        courseCode = request.form['courseCode']
        courseName = request.form['courseName']
        collegeCode = request.form['collegeCode']

        unique_courseCode = course_M.check_courseCode(courseCode)

        # Implement add function for proper string formatting.
        capt_courseCode = courseCode.upper()
        capt_courseName = courseName.title().replace('Of', 'of').replace("In", "in")

        if len(courseCode) < 1:
            flash("You need to input valid course code!", category='error')
        elif len(courseName) < 1:
            flash("You need to input valid course name!", category='error')
        elif unique_courseCode:
            flash("Course already exists!", category='error')
        else:
            course_M.add_Course(capt_courseCode, capt_courseName, collegeCode)
            flash("Successfully added the course information!", category="success")
    return redirect(url_for('Cbp.courses'))

#For deleting courses
@courses_bp.route('/delete_course/<string:courseCode>', methods=["GET"])
def delete_course(courseCode):
    print('The course has been successfully deleted!')
    course_M.delete_Course(courseCode)
    flash("You have deleted course information. It will take effect on the students enrolled on the deleted course. ", category='secondary')
    return redirect(url_for('Cbp.courses'))

@courses_bp.route('/course_search', methods=['GET'])
def course_search():
    course_selection = course_M.display_Courses()
    college_selection = course_M.display_Colleges()

    course_key = request.args.get('course_key', '')
    course_key_Code = request.args.get('course_key_Code', '')
    course_key_Name = request.args.get('course_key_Name', '')
    college_key_Code = request.args.get('college_key_Code', '')
    page = request.args.get('page', 1, type=int)

    if course_key_Code == 'By Course Code':
        course_key_Code = None

    if course_key_Name == 'By Course Name':
        course_key_Name = None

    if college_key_Code == 'By College Code':
        college_key_Code = None

    try:
        # Default value
        search_data = []

        # Search by Course Code
        if course_key_Code and not course_key_Name and not college_key_Code:
            search_data = course_M.search_filter(course_key_Code, None, None)

        # Search by Course Name
        elif course_key_Name and not course_key_Code and not college_key_Code:
            search_data = course_M.search_filter(None, course_key_Name, None)

        # Search by College Code
        elif college_key_Code and not course_key_Code and not course_key_Name:
            search_data = course_M.search_filter(None, None, college_key_Code)

        # General Search
        elif course_key:
            search_data = course_M.search_Course(
                course_key,
                course_key_Name,
                course_key_Code,
                college_key_Code
            )

        # Total number of results
        total_courses = len(search_data)

        per_Page = 10
        start_Page = (page - 1) * per_Page
        end_Page = start_Page + per_Page

        courses_on_Page = search_data[start_Page:end_Page]

        total_Pages = (total_courses + per_Page - 1) // per_Page

        if total_Pages == 0:
            total_Pages = 1

        page_Number = list(range(1, total_Pages + 1))

        next_url = url_for(
            'Cbp.course_search',
            course_key=course_key,
            course_key_Code=course_key_Code,
            course_key_Name=course_key_Name,
            college_key_Code=college_key_Code,
            page=page + 1
        ) if page < total_Pages else None

        prev_url = url_for(
            'Cbp.course_search',
            course_key=course_key,
            course_key_Code=course_key_Code,
            course_key_Name=course_key_Name,
            college_key_Code=college_key_Code,
            page=page - 1
        ) if page > 1 else None

        return render_template(
            '/courses/course_results.html',
            Courses=courses_on_Page,
            course_select=course_selection,
            college_select=college_selection,
            page=page,
            number_of_Pages=page_Number,
            total_Pages=total_Pages,
            next_page=next_url,
            prev_page=prev_url
        )

    except Exception as e:
        flash(f"Error occurred! {e}", category='error')
        return redirect(url_for('Cbp.courses'))


#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COURSES ENDS IN HERE.#
#<-------------------------------------------------->#
