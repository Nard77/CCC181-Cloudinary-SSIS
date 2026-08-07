from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
from networkx import reverse
import pymysql.cursors
import filetype
import magic
from pathlib import Path

from torch import sort
from config import SECRET_KEY
from src.database import db_connection
from models.students import student_M


import re
import cloudinary
from cloudinary import CloudinaryImage
from cloudinary.uploader import upload


students_bp = Blueprint("Sbp", __name__,  template_folder='/templates')

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING STUDENTS STARTS IN HERE.#
#<-------------------------------------------------->#

    #This is for accessing students table and its actions:
@students_bp.route('/students')
def students():
    course = request.args.get("course_key_Code")
    year = request.args.get("student_key_Level")
    gender = request.args.get("student_key_Gender")
    keyword = request.args.get("student_key")

    #displays all of the students
    students = list(student_M.display_Students())

    sort = request.args.get("sort", "")
    order = request.args.get("order", "asc")

    if sort:
        if sort == "yearLevel":
            year_map = {
                "1st-Year": 1,
                "2nd-Year": 2,
                "3rd-Year": 3,
                "4th-Year": 4
            }

            students.sort(
                key=lambda x: year_map.get(x["yearLevel"], 99),
                reverse=(order=="desc")
            )
        else:
            students.sort(
                key=lambda x: x[sort].lower(),
                reverse=(order=="desc")
            )

    # course_college = student_M.display_course_college()

    #if students['courseCode'] == 'N/A':
    #   pass

    number = len(students)
    total_students = number

    page = request.args.get('page', 1, type=int)
    print(page)
    per_Page = 10
    start_Page = (page - 1) * per_Page
    end_Page = start_Page + per_Page

    students_on_Page = students[start_Page:end_Page]

    #students_dict = dict(students_on_Page)

    total_Pages = (total_students + per_Page - 1) // per_Page
    print(f"The amout of total pages are: {total_Pages}")

    page_Number = list(range(1, total_Pages + 1))
    print(page_Number)

    image = request.files.get('image_upd')

    #displays all of the courses
    courses = student_M.display_Courses()

    return render_template(
        "/students/students.html",
        Students=students_on_Page,
        Courses=courses,
        page=page,
        number_of_Pages=page_Number,
        total_Pages=total_Pages,
        image=image,
        sort=sort,
        order=order
    )

@students_bp.route('/student_search', methods=["GET"])
def student_search():

    courses = student_M.display_Courses()

    student_key = request.args.get('student_key', '').strip()
    course_key_Code = request.args.get('course_key_Code', '')
    student_key_Level = request.args.get('student_key_Level', '')
    student_key_Gender = request.args.get('student_key_Gender', '')
    page = request.args.get('page', 1, type=int)
    sort = request.args.get("sort", "idNumber")
    order = request.args.get("order", "asc")

    # Remove placeholder values
    if course_key_Code == "By Course Code":
        course_key_Code = None

    if student_key_Level == "By Year Level":
        student_key_Level = None

    if student_key_Gender == "By Gender":
        student_key_Gender = None

    # No search/filter at all
    if not student_key and not course_key_Code and not student_key_Level and not student_key_Gender:
        return redirect(url_for("Sbp.students"))

    try:

        # ONE function handles everything
        search_data = student_M.search_Student(
            student_key,
            course_key_Code,
            student_key_Level,
            student_key_Gender
        )
        reverse = order == "desc"

        if sort == "firstName":
            search_data.sort(key=lambda x: x["firstName"].lower(), reverse=reverse)

        elif sort == "lastName":
            search_data.sort(key=lambda x: x["lastName"].lower(), reverse=reverse)

        elif sort == "yearLevel":
            search_data.sort(key=lambda x: x["yearLevel"], reverse=reverse) 

        total_students = len(search_data)

        per_Page = 10
        start = (page - 1) * per_Page
        end = start + per_Page

        students_on_Page = search_data[start:end]

        total_Pages = max(1, (total_students + per_Page - 1) // per_Page)
        page_Number = list(range(1, total_Pages + 1))

        next_url = None
        prev_url = None

        if page < total_Pages:
            next_url = url_for(
                'Sbp.student_search',
                student_key=student_key,
                course_key_Code=course_key_Code,
                student_key_Level=student_key_Level,
                student_key_Gender=student_key_Gender,
                sort=sort,
                order=order,
                page=page+1
            )
            

        if page > 1:
            prev_url = url_for(
                'Sbp.student_search',
                student_key=student_key,
                course_key_Code=course_key_Code,
                student_key_Level=student_key_Level,
                student_key_Gender=student_key_Gender,
                sort=sort,
                order=order,
                page=page-1
            )

    except Exception as e:
        print(e)
        flash(f"Error occurred: {e}", "error")
        return redirect(url_for("Sbp.students"))

    return render_template(
        "/students/student_results.html",
        search_results=students_on_Page,
        Courses=courses,
        page=page,
        number_of_Pages=page_Number,
        total_Pages=total_Pages,
        next_page=next_url,
        prev_page=prev_url,
        student_key=student_key,
        course_key_Code=course_key_Code,
        student_key_Level=student_key_Level,
        student_key_Gender=student_key_Gender,
        selected_course=course_key_Code,
        selected_yearLevel=student_key_Level,
        selected_gender=student_key_Gender,
        sort=sort,
        order=order
    )

#For editing/updating the student information
@students_bp.route('/edit_student', methods=["POST"])
def edit_students():
    if request.method == "POST":
        try:
            print('successfully edited the select item')
            student_id = request.form['student_id']
            firstNameEdit = request.form['firstNameEdit']
            lastNameEdit =  request.form['lastNameEdit']
            courseCodeEdit = request.form['courseCodeEdit']
            yearLevelEdit = request.form['yearLevelEdit']
            genderEdit = request.form['genderEdit']

            #taking in the uplaoded image from the front-end.
            image = request.files['imageEdit']
            file_size = len(image.read())
            image.seek(0)

            if len(firstNameEdit) < 2:
                flash("You need to input valid first name!", category='error')
            elif len(lastNameEdit) < 2:
                flash("You need to input valid last name!", category='error')
            elif file_size > 10 * 1024 * 1024:
                flash("The image uploaded exceeds the maximum file size!", category='error')

            elif not image:
                print("image has not been changed")
                student_M.edit_Student(firstNameEdit.title(), lastNameEdit.title(),
                                courseCodeEdit, yearLevelEdit, genderEdit, student_id)
                flash("you have successfully edited the student information!", category='success')

            elif image.content_type not in ["image/jpg", "image/jpeg", "image/png"]:
                flash("Image must be uploaded in correct format!", category='error')

            else:

                uploaded_file = upload(image)
                image_id = CloudinaryImage(uploaded_file['public_id']).build_url(width = 50, height = 50, crop = "fill")
                print(image_id)
                student_M.edit_Student_p(firstNameEdit.title(), lastNameEdit.title(),
                                courseCodeEdit, yearLevelEdit, genderEdit, image_id, student_id)
                flash("you have successfully edited the student information!", category='success')
            return redirect(url_for('Sbp.students'))

        except Exception as e:
            flash(f"Error occured! {e}", category="secondary")

    return redirect(url_for('Sbp.students'))



# For adding a new student information
@students_bp.route('/add_students', methods=["POST"])
def add_student():
    if request.method == "POST":
        try:
            idNumber = request.form['idNumber']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            courseCode = request.form['courseCode']
            yearLevel = request.form['yearLevel']
            gender = request.form['gender']

            student_idNumber = student_M.check_idNumber_Dict(idNumber)

            # Get uploaded image (optional)
            image = request.files.get('image_upd')

            capt_firstName = firstName.title()
            capt_lastName = lastName.title()

            pattern = r"^\d{4}-\d{4}$"

            if len(idNumber) < 1:
                flash("You need to input valid ID Number!", category='error')

            elif len(firstName) < 1:
                flash("You need to input valid first name!", category='error')

            elif len(lastName) < 1:
                flash("You need to input valid last name!", category='error')

            elif courseCode == 'Select a Course':
                flash("Please enter a valid course.", category='error')

            elif student_idNumber:
                flash("ID Number Already Exists!", category='error')

            elif not re.findall(pattern, idNumber):
                flash(f"{idNumber} is not a valid ID Number.", category="error")

            # No picture uploaded
            elif image is None or image.filename == "":
                image_id = ""
                student_M.add_Students_p(
                    idNumber,
                    capt_firstName,
                    capt_lastName,
                    courseCode,
                    yearLevel,
                    gender,
                    image_id
                )

                flash("Successfully added the student information!", category='success')

            else:

                # Check file size (10 MB)
                image.seek(0, 2)
                file_size = image.tell()
                image.seek(0)

                if file_size > 10 * 1024 * 1024:
                    flash("The image exceeds the maximum size of 10 MB!", category='error')

                elif image.content_type not in ["image/jpg", "image/jpeg", "image/png"]:
                    flash("Image must be JPG, JPEG, or PNG!", category='error')

                else:
                    uploaded_file = upload(image)

                    image_id = CloudinaryImage(
                        uploaded_file['public_id']
                    ).build_url(
                        width=50,
                        height=50,
                        crop="fill"
                    )

                    student_M.add_Students_p(
                        idNumber,
                        capt_firstName,
                        capt_lastName,
                        courseCode,
                        yearLevel,
                        gender,
                        image_id
                    )

                    flash("Successfully added the student information!", category='success')

            return redirect(url_for('Sbp.students'))

        except Exception as e:
            flash(f"Error occurred: {e}", category="secondary")

    return redirect(url_for('Sbp.students'))


#For deleting a selected student
@students_bp.route('/delete_student/<string:students_id>', methods=["GET"])
def delete_student(students_id):
    try:
        print('The student has been successfully deleted!')
        flash("you have deleted a student information", category='secondary')
        student_M.delete_Student(students_id)
        return redirect(url_for('Sbp.students'))

    except Exception as e:
        flash(f"Error occured {e}", category="secondary")

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING STUDENTS ENDS IN HERE.#
#<-------------------------------------------------->#
