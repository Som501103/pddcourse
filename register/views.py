from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import MT_User, Course_D, List_Dept, List_Emp
from .forms import SaveForm
from django.shortcuts import redirect
import requests, xmltodict
import string
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q, F

def login(request):
    try:
        mgs = {
                    'massage' : ' '
                }
        if request.method == 'POST':
            Emp_id = request.POST.get('StaffID')
            Emp_pass = request.POST.get('StaffPS')
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
                request.session['Emp_id'] = Emp_id
                request.session['Fullname'] = Fullname
                request.session['Position'] = Position
                request.session['LevelCode'] = LevelCode
                request.session['Department'] = Dept
                request.session['Dept_code'] = Dept_code
                request.session['RegionCode'] = RegionCode 

                return redirect('home')
            else:
                mgs = {
                    'massage' : 'รหัสพนักงานหรือรหัสผ่านไม่ถูกต้อง....'
                }
                # return redirect('login',{'mgs':mgs})
            
    except Course_D.DoesNotExist:
        raise Http404

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
    Emp_id = request.session['Emp_id'] 
    Fullname = request.session['Fullname']
    Dept = request.session['Department']
    check_km = List_Emp.objects.filter(E_ID = Emp_id,ref_course__PK_Course_D__range=(3,6)).exclude(ref_course='8').count()
    print(check_km)
    if check_km == 0:
        courses = Course_D.objects.all().filter(status = 0).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('PK_Course_D')
    
    elif Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599':
        courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('PK_Course_D')

    else : 
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('PK_Course_D')
    
    return render(request, 'home.html', {'courses': courses})


def course_title(request, PK_Course_D):
    try:
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
        else:
            course = Course_D.objects.get(PK_Course_D=PK_Course_D, status = 1)
            student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')
        massage = ''
        if request.method == 'POST':
            Emp_email = request.POST.get('Emp_email')
            Emp_tel = request.POST.get('Emp_tel')
            # print(Emp_id)
            # print(Emp_email)
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id,ref_course__PK_Course_D__range=(3,6)).exclude(ref_course='8').count()
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
            if qs_check_user == 1:
                check_user_regist = List_Emp.objects.filter(E_ID = Emp_id,ref_course__PK_Course_D__range=(9,12)).exclude(ref_course='8').count()
                if check_user_regist == 0:
                    print('online')
                    print(PK_Course_D)
                    nameget = idm(Emp_id)
                    fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                    employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = Emp_email, Tel = Emp_tel)
                    employee.save()
                    count = len(List_Emp.objects.filter(ref_course=PK_Course_D, status = 1))
                    print (count)
                    update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                    print(update_num_student)
                    massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว"
                else :
                    massage = "ท่านได้ลงทะเบียนแล้ว"
            else:
                massage = "หลักสูตรเปิดสำหรับผู้ที่เคยลงทะเบียน KM in action ช่วงเดือน เมษายน 2563"

    except Course_D.DoesNotExist:
        raise Http404

    return render(request, 'course_register.html', {'course': course,'student':student,'massage':massage,'profile':profile})

def course_detial(request, PK_Course_D):
    try:
        course = Course_D.objects.get(PK_Course_D=PK_Course_D)
        student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1)
    except Course_D.DoesNotExist:
        raise Http404

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
    print(employeedata['FirstName'])
    return employeedata

def checkStudent(Emp_id):
    student = len(List_Emp.objects.get(E_ID= Emp_id,status= 1))
    if student == 0:
        rerult = 1
    else :
        rerult = 0
    return rerult


class UsersListJson(BaseDatatableView):
        # The model we're going to show
        model = List_Emp
        columns = ['Fullname', 'Dep', 'Regist_Date']
        order_columns = ['Regist_Date','Dep','Fullname']

        def filter_queryset(self, qs):
            sSearch = self.request.GET.get('sSearch', None)
            if sSearch:
                qs = qs.filter(Q(Fullname__istartswith=sSearch) | Q(Dep__istartswith=sSearch))
            return qs




    
# Create your views here.
