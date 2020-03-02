from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import MT_User, Course_D, List_Dept, List_Emp
from .forms import SaveForm
import requests, xmltodict
import string
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q


def home(request):
    courses = Course_D.objects.all().filter(status = 1)
    # count = Course_D['']


    return render(request, 'home.html', {'courses': courses})

def course_title(request, PK_Course_D):
    try:
        course = Course_D.objects.get(PK_Course_D=PK_Course_D, status = 1)
        student = List_Emp.objects.filter(ref_course=PK_Course_D, status= 1).order_by('-PK_List_Emp')
        massage = ''
        if request.method == 'POST':
            Emp_id = request.POST.get('Emp_id')
            print(Emp_id)
            qs_check_user = len(List_Emp.objects.filter(E_ID = Emp_id, status= 1))
            if qs_check_user == 0:
                nameget = idm(Emp_id)
                print(nameget['TitleFullName'], nameget['FirstName'],nameget['LastName'],nameget['DepartmentShort'])
                fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'])
                employee.save()
                count = len(List_Emp.objects.get(ref_course=course, status = 1))
                update_num_student = Course_D.objects.filter(PK_Course_D=course).update(Number_People=count)
                employee.Fullname
                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว"
                
            else:
                massage = "ท่านได้ลงทะเบียน หรือ เคยผ่านกการฝึกอบรมหลักสูตร KM Tools/KM Action/KM Facilitator แล้ว"

    except Course_D.DoesNotExist:
        raise Http404

    return render(request, 'course_register.html', {'course': course,'student':student,'massage':massage})

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

    print(o)
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
