from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import MT_User, Course_D, List_Dept, List_Emp, Course_Director, Check_Loginerror, Check_Staff_End, Subject
from .forms import SaveForm
from django.shortcuts import redirect
import requests, xmltodict
import string
from django.db.models import Q, F
from datetime import datetime
def login(request):
    mgs = {
                'massage' : ' '
            }
    if request.method == 'POST':
        Emp_id = request.POST.get('StaffID')
        Emp_pass = request.POST.get('StaffPS')
        check_error = len(Check_Loginerror.objects.filter(E_ID=Emp_id))
        check_error = 1 #bypass
        if check_error > 0 :
        # Emp_id == '303270' or Emp_id == '501249' or Emp_id == '489343' or Emp_id == '235859' or Emp_id == '444717' or Emp_id == '444660':
            reposeMge = 'true'   
        else : 
            check_ID = idm_login(Emp_id,Emp_pass)
            # print(check_ID)
            reposeMge = check_ID

        if reposeMge == 'true':
            nameget = idm(Emp_id)
            # print(nameget)
            Fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
            Position = nameget['PositionDescShort']
            LevelCode = nameget['LevelCode']
            Dept = nameget['DepartmentShort']
            Dept_code = nameget['NewOrganizationalCode']
            RegionCode = nameget['RegionCode']
            Email = nameget['Email']
            request.session['Emp_id'] = Emp_id
            request.session['Fullname'] = Fullname
            request.session['Position'] = Position
            request.session['LevelCode'] = LevelCode
            request.session['Department'] = Dept
            request.session['Dept_code'] = Dept_code
            request.session['RegionCode'] = RegionCode
            request.session['Email'] = Email
            return redirect('home')
        else:
            mgs = {
                'massage' : 'รหัสพนักงานหรือรหัสผ่านไม่ถูกต้อง....'
            }
            # return redirect('login',{'mgs':mgs})

    return render(request, 'login.html', {'mgs':mgs})

def idm_login(Emp_id, Emp_pass):
    print('--------------------')
    
    url="https://idm.pea.co.th/webservices/idmservices.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    xmltext ='''<?xml version="1.0" encoding="utf-8"?>
                 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <IsValidUsernameAndPassword_SI xmlns="http://idm.pea.co.th/">
                        <WSAuthenKey>{0}</WSAuthenKey>
                        <Username>{1}</Username>
                        <Password>{2}</Password>
                        </IsValidUsernameAndPassword_SI>
                    </soap:Body>
                </soap:Envelope>'''
    wskey = '07d75910-3365-42c9-9365-9433b51177c6'
    body = xmltext.format(wskey,Emp_id,Emp_pass)
    response = requests.post(url,data=body,headers=headers)
    print(response.status_code)
    o = xmltodict.parse(response.text)
    jsonconvert=dict(o)
    # print(o)
    authen_response = jsonconvert["soap:Envelope"]["soap:Body"]["IsValidUsernameAndPassword_SIResponse"]["IsValidUsernameAndPassword_SIResult"]["ResultObject"]
    return authen_response

def home(request):
    courses= {
            'courses' : ''
        }
    subjects= {
            'subjests' : ''
    }
    Emp_id = request.session['Emp_id']
    Fullname = request.session['Fullname']
    Dept = request.session['Department']
    Dept_code = request.session['Dept_code']
    Position = request.session['Position']
    LevelCode = request.session['LevelCode']
    Cut_Dept_code = Dept_code[:4]
    Cut_Dept_code2 = Dept[:3]
    get_dept = Dept[5:8]
    print(Dept_code)
    print(LevelCode)
    print(Fullname)
    print(Dept)
    print(get_dept)
    print(Cut_Dept_code2)
    check_SD = len(Course_Director.objects.filter(E_ID = Emp_id))
    check_km = List_Emp.objects.filter(E_ID = Emp_id,ref_course__PK_Course_D__range=(3,6)).exclude(ref_course='8').count()
    print(check_km)
    now = datetime.now()
    current_time = now.strftime("%H")
    mini = now.strftime("%M")
    print("Current Time =", current_time)
    if current_time == "09" and int(mini) <= 30 :
        open1 = Course_D.objects.get(PK_Course_D = 109)
        open1.status = 1
        open1.save()
    elif current_time == "09" and int(mini) <= 59 and int(mini) >= 30 :
        open2 = Course_D.objects.get(PK_Course_D = 110)
        open2.status = 1
        open2.save()
    elif current_time == "10" and int(mini) <= 59 and int(mini) >= 30 :
        open3 = Course_D.objects.get(PK_Course_D = 111)
        open3.status = 1
        open3.save()
    elif current_time == "11" and int(mini) <= 30 : 
        open4 = Course_D.objects.get(PK_Course_D = 112)
        open4.status = 1
        open4.save()
    elif current_time == "11" and int(mini) <= 59 and int(mini) >= 30 :
        open5 = Course_D.objects.get(PK_Course_D = 113)
        open5.status = 1
        open5.save()

    if Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' :
            courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    elif Cut_Dept_code2 ==  "ฝพบ" :
        courses = Course_D.objects.all().exclude( PK_Course_D = 110 ).exclude(PK_Course_D = 111).exclude( PK_Course_D = 112).exclude( PK_Course_D = 113).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    elif get_dept == "กพค" or Cut_Dept_code2 ==  "กพค":
        courses = Course_D.objects.all().exclude( PK_Course_D = 109).exclude(PK_Course_D = 111).exclude( PK_Course_D = 112).exclude( PK_Course_D = 113).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    elif get_dept == "ศฝฟ" or Cut_Dept_code2 == "ศฝฟ":
        courses = Course_D.objects.all().exclude(PK_Course_D = 109).exclude( PK_Course_D = 110).exclude( PK_Course_D = 112).exclude( PK_Course_D = 113).filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    elif get_dept == "กฝช" or Cut_Dept_code2 ==  "กฝช": 
        courses = Course_D.objects.all().exclude(PK_Course_D = 109).exclude( PK_Course_D = 110).exclude( PK_Course_D = 111).exclude( PK_Course_D = 113).filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    elif get_dept == "รรช" or Cut_Dept_code2 ==  "รรช":
        courses = Course_D.objects.all().exclude(PK_Course_D = 109).exclude( PK_Course_D = 110).exclude( PK_Course_D = 111).exclude( PK_Course_D = 112).filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    else:  
        if Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' :
            courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        elif LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2': # เช็คระดับของนักศึกษา ระดับ7-8
            courses = Course_D.objects.all().exclude( PK_Course_D = 109 ).exclude( PK_Course_D = 110 ).exclude(PK_Course_D = 111).exclude( PK_Course_D = 112).exclude( PK_Course_D = 113).filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        else : 
            courses = Course_D.objects.all().exclude( PK_Course_D = 109 ).exclude( PK_Course_D = 110 ).exclude(PK_Course_D = 111).exclude( PK_Course_D = 112).exclude( PK_Course_D = 113).filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
    competency_data = Course_D.objects.all().filter(Access_level=2,status=1)
    #print(Subject.objects.all().filter(Url_location='https://virtual.yournextu.com/Catalog'))
    #subject = Relation_comp.objects.select_related('Course_ID').filter(Course_ID__Course_ID='PDD01CO08')
    subjects = Subject.objects.all()
    open_course = len(Course_D.objects.filter(PK_Course_D =75,status = 1))
    print("open_course",open_course)
    return render(request, 'home.html', {'courses': courses,'Cut_Dept_code':Cut_Dept_code,'subjests':subjects,'Fullname':Fullname,'open_course':open_course})


def course_title(request, PK_Course_D):
    Emp_id = request.session['Emp_id'] 
    Fullname = request.session['Fullname']
    Dept = request.session['Department']
    profile = {
            'Emp_id' : Emp_id,
            'Fullname' : Fullname,
            'Dept' : Dept
    }
    
    if PK_Course_D == 14:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')

    elif PK_Course_D == 49:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')

    elif PK_Course_D == 50:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')

    elif PK_Course_D == 51:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')

    elif PK_Course_D == 52:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')
    
    elif PK_Course_D == 52:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')

    else:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')
    massage = ''
    if request.method == 'POST':
            # Emp_email = request.POST.get('Emp_email')
            Emp_tel = request.POST.get('Emp_tel')
            # print(Emp_id)
            # print(Emp_email)
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
            print(qs_check_user)
            # print(PK_Course_D)
            # if PK_Course_D == 8:
            #     qs_check_user_online = len(List_Emp.objects.filter(E_ID = Emp_id, status= 1, ref_course = 8))
            #     if qs_check_user_online == 0:
            #         print('online')
            #         print(PK_Course_D)
            #         nameget = idm(Emp_id)
            #         fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
            #         employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = Emp_email, Tel = Emp_tel)
            #         employee.save()
            #         count = len(List_Emp.objects.filter(ref_course=PK_Course_D, status = 1))
            #         print (count)
            #         update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
            #         print(update_num_student)
            #         massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว"
            #     else:
            #         massage = "ท่านได้ลงทะเบียนแล้ว"

            
            # elif qs_check_user == 0:
            #     nameget = idm(Emp_id)
            #     if nameget['BaCode'] == 'Z000':
            #         print('km')
            #         print(nameget['TitleFullName'], nameget['FirstName'],nameget['LastName'],nameget['DepartmentShort'])
            #         fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
            #         employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'])
            #         employee.save()
            #         count = len(List_Emp.objects.filter(ref_course=PK_Course_D, status = 1))
            #         print (count)
            #         update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
            #         print(update_num_student)
            #         massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว"
            #     else :
            #         massage = "หลักสูตรนี้เฉพาะหนักงานที่สังกัดใน สำนักงานใหญ่"
            # else:

            #     massage = "ท่านได้ลงทะเบียนแล้ว"
            if qs_check_user == 0:
                # check_user_regist = List_Emp.objects.filter(E_ID = Emp_id,ref_course__PK_Course_D__range=(9,14)).exclude(ref_course='8').count()
                
                print('online')
                print(PK_Course_D)
                nameget = idm(Emp_id)
                fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'],Dept_code = nameget['DepartmentSap'], Tel = Emp_tel, Email = nameget['Email'])
                employee.save()
                count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                print (count)
                update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                print(update_num_student)
                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว"
            else :
                massage = "ท่านได้ลงทะเบียนแล้ว"
    

    return render(request, 'course_register.html', {'course': course,'student':student,'massage':massage,'profile':profile})

def course_detial(request, PK_Course_D):

    course = Course_D.objects.get(PK_Course_D=PK_Course_D)
    student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1)
  

    return render(request, 'course_register.html', {'course': course,'student':student})

def idm(Emp_id):
    url="https://idm.pea.co.th/webservices/EmployeeServices.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    xmltext ='''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <GetEmployeeInfoByEmployeeId_SI xmlns="http://idm.pea.co.th/">
                        <WSAuthenKey>{0}</WSAuthenKey>
                        <EmployeeId>{1}</EmployeeId>
                        </GetEmployeeInfoByEmployeeId_SI>
                </soap:Body>
                </soap:Envelope>'''
    wsauth = 'e7040c1f-cace-430b-9bc0-f477c44016c3'
    body = xmltext.format(wsauth,Emp_id)
    response = requests.post(url,data=body,headers=headers)
    o = xmltodict.parse(response.text)
    # print(o)
    jsonconvert=o["soap:Envelope"]['soap:Body']['GetEmployeeInfoByEmployeeId_SIResponse']['GetEmployeeInfoByEmployeeId_SIResult']['ResultObject']
    employeedata = dict(jsonconvert)
    # print(employeedata['FirstName'])
    # print(employeedata['NewOrganizationalCode'])
    return employeedata

def checkStudent(Emp_id):
    student = len(List_Emp.objects.get(E_ID= Emp_id,status= 1))
    if student == 0:
        rerult = 1
    else :
        rerult = 0
    return rerult


# Create your views here.

def update_eng(request):
    mgs = {
                    'massage' : ' '
                }
    update_staff = Check_Staff_End.objects.all()
    for x in update_staff:
        nameget = idm(x.E_ID)
        fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
        position = nameget['PositionDescShort']
        level = nameget['LevelCode']
        Dept_code = nameget['NewOrganizationalCode']
        DepartmentShort = nameget['DepartmentShort']
        
        update_staff = Check_Staff_End.objects.get(E_ID = x.E_ID)
        update_staff.Name = fullname
        update_staff.Position = position
        update_staff.Level = level
        update_staff.Dept_code = Dept_code
        update_staff.Dept_Short = DepartmentShort
        update_staff.save()
        print('done')

        # print(level)
        mgs = {
                    'massage' : 'done'
                }

    return render(request, 'update_eng.html', {'mgs':mgs})

def course_base(request, PK_Course_D):
    massage=''
    subjects= {
        'subjests' : ''
    }
    course = Course_D.objects.get(PK_Course_D=PK_Course_D)
    Emp_id = request.session['Emp_id'] 
    Fullname = request.session['Fullname']
    Dept = request.session['Department']
    LevelCode = request.session['LevelCode']
    subjects = Subject.objects.all().filter(Sub_level=1)
    student = List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D))
    # print(subjects)
    profile = {
            'Emp_id' : Emp_id,
            'Fullname' : Fullname,
            'Dept' : Dept,
            'LevelCode' : LevelCode
    }
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Emp_tel = request.POST.get('Emp_tel')
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
            if qs_check_user == 0:
                nameget = idm(Emp_id)
                fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                if nameget['LevelCode'] == '07' or nameget['LevelCode'] == '08' or nameget['LevelCode'] == 'M1' or nameget['LevelCode'] == 'M2':
                    employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                    # employee.save()
                    count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                
                    # update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                    
                    massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว"
                else :
                    massage = "ท่านไม่ได้อยู่ในกลุ่มระดับ 7-8 ที่หลักสูตรกำหนด"
            else :
                massage = "ท่านได้ลงทะเบียนแล้ว"
    

    return render(request,'course_base.html',{'course': course,'profile':profile,'subjects':subjects,'student':student})


def course_base2(request, PK_Course_D):
    massage=''
    subjects= {
        'subjests' : ''
    }
    course = Course_D.objects.get(PK_Course_D=PK_Course_D)
    Emp_id = request.session['Emp_id'] 
    Fullname = request.session['Fullname']
    Dept = request.session['Department']
    LevelCode = request.session['LevelCode']
    Email = request.session['Email']
    subjects = Subject.objects.all().filter(Sub_level=1)
    student = List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D))
    qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
    if qs_check_register > 0:
        massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
    # print(subjects)
    profile = {
            'Emp_id' : Emp_id,
            'Fullname' : Fullname,
            'Dept' : Dept,
            'LevelCode' : LevelCode,
            'Email' : Email
    }
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Emp_tel = request.POST.get('Emp_tel')
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
            
            if qs_check_user == 0:
                nameget = idm(Emp_id)
                fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                if nameget['LevelCode'] == '07' or nameget['LevelCode'] == '08' or nameget['LevelCode'] == 'M1' or nameget['LevelCode'] == 'M2':
                    employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                    if course.status == '1' or course.status == 1:
                        employee.save()
                        count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                        update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                        qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                        massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                    else :
                        massage = "ยังไม่เปิดให้ลงทะเบียน"
                else :
                    massage = "ท่านไม่ได้อยู่ในกลุ่มระดับ 7-8 ที่หลักสูตรกำหนด"
            else :
                massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
        else:
            massage = "มีผู้ลงทะเบียนครบแล้ว"

    return render(request,'course_base2.html',{'course': course,'profile':profile,'subjects':subjects,'student':student,'massage':massage,'qs_check_register':qs_check_register})

def course_base3(request, PK_Course_D):
    massage=''
    subjects= {
        'subjests' : ''
    }
    course = Course_D.objects.get(PK_Course_D=PK_Course_D)
    Emp_id = request.session['Emp_id'] 
    Fullname = request.session['Fullname']
    Dept = request.session['Department']
    LevelCode = request.session['LevelCode']
    Email = request.session['Email']
    print(PK_Course_D)
    student = List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D))
    qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
    if qs_check_register > 0:
        massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
    # print(subjects)
    profile = {
            'Emp_id' : Emp_id,
            'Fullname' : Fullname,
            'Dept' : Dept,
            'LevelCode' : LevelCode,
            'Email' : Email
    }
    if course.PK_Course_D == 109 or course.PK_Course_D == 110 or course.PK_Course_D == 111 or course.PK_Course_D == 112 or course.PK_Course_D == 113 :

        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().exclude(Subject_name = 'Managing and Coaching Teams').filter(Sub_level=3)
        if LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2':
            subjects = Subject.objects.all().filter(Sub_level=3)
    elif LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2': # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=1)
    elif LevelCode == '09' or LevelCode == '10'  or LevelCode == '11' or LevelCode == 'M3' or LevelCode == 'M4' or LevelCode == 'M5' or LevelCode == 'M6': # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=2)
    
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Emp_tel = request.POST.get('Emp_tel')
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
            
            if qs_check_user == 0:
                nameget = idm(Emp_id)
                fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                if nameget['LevelCode'] == '07' or nameget['LevelCode'] == '08' or nameget['LevelCode'] == 'M1' or nameget['LevelCode'] == 'M2' or course.PK_Course_D == 109 or course.PK_Course_D == 110 or course.PK_Course_D == 111 or course.PK_Course_D == 112 or course.PK_Course_D == 113:
                    employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                    if course.status == '1' or course.status == 1:
                        employee.save()
                        count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                        update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                        qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                        massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                    else :
                        massage = "ยังไม่เปิดให้ลงทะเบียน"
                else :
                    massage = "ท่านไม่ได้อยู่ในกลุ่มระดับ 7-8 ที่หลักสูตรกำหนด"
            else :
                massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
        else:
            massage = "มีผู้ลงทะเบียนครบแล้ว"

    return render(request,'course_base3.html',{'course': course,'profile':profile,'subjects':subjects,'student':student,'massage':massage,'qs_check_register':qs_check_register})