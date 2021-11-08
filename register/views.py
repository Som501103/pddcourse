from os import access
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import MT_User, Course_D, List_Dept, List_Emp, Course_Director, Check_Loginerror, Check_Staff_End, Subject
from .forms import SaveForm
from django.shortcuts import redirect
import requests, xmltodict
import string
from django.db.models import Q, F
from datetime import datetime, timedelta , timezone, date 
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    mgs = {
                'massage' : ' '
            }
    '''list = [180436,181149,191788,200587,223747,229133,233564,255914,261232,261274,267644,268022,269175,275281,280414,283276,284638,287254,289719,292615,292681,294413,297788,297916,298158,298849,301391,301812,303254,303270,304161,305507,305688,305777,308068,308115,308474,308490,308628,308733,309399,309894,310489,311728,311778,311833,313479,314166,314213,315950,151063,194752,198057,199590,200537,222555,233881,235972,237623,251253,252712,258174,258742,263535,268894,273718,275192,276504,277487,283828,284094,284565,284793,285016,285139,286957,289353,290003,290312,290833,293988,296512,297291,298394,300492,300646,302494,302957,303602,303733,304056,304268,305939,306731,307826,308050,308767,309585,311914,312041,312944,313843,314962,315895,316469,318152,321579,321600,322282,322614,324153,324179,327004,327753,330879,331956,400014,401670,403177,404034,404937,407969,410271,413033,413415,414495,414665,415019,415027,415085,415920,415938,415988,415996,416031,416065,417566,418025,419673,420860,423004,423088,424783,425373,426662,427244,427927,427935,428151,428193,428486,429149,429513,430572,430718,430734,430768,430899,430912,432469,432697,432702,433261,437401,437689,444204,444254,444466,444513,444547,444636,444652,444678,448575,448957,449733,449995,451675,451926,452663,454128,454306,454534,454550,454657,454885,456007,456829,456992,457613,458253,458295,458635,458685,458693,459445,459518,459924,459974,459990,460234,460315,460527,460844,461010,461125,461141,462503,462511,462757,463193,463648,463907,464042,464327,464385,464393,464474,464521,464636,465030,465195,465276,465640,466256,466646,466905,466939,466947,466971,467286,467472,467553,467587,467707,467765,468012,468630,468923,469076,469173,469822,469872,469995,470213,470255,470865,471609,471934,472029,472427,472493,472516,472532,472582,472621,472671,472689,472702,472906,473033,473041,474398,474746,474762,475085,476219,476374,476413,476528,476536,477477,477613,477891,477914,478279,478350,479429,479657,479673,479681,479699,481002,481272,481450,481507,481549,481840,483088,484513,484822,485307,486515,487846,488452,488876,489034,489199,489416,490718,490792,490912,491031,491861,495077]
    for i in list:
        gettest = idm(i)
        print(i,gettest['LevelCode'],gettest['PositionDescShort'])'''
    if request.method == 'POST':
        Emp_id = request.POST.get('StaffID')
        Emp_pass = request.POST.get('StaffPS')
        check_error = len(Check_Loginerror.objects.filter(E_ID=Emp_id))
        #check_error = 1 #bypass
        if check_error > 0 :
        # Emp_id == '303270' or Emp_id == '501249' or Emp_id == '489343' or Emp_id == '235859' or Emp_id == '444717' or Emp_id == '444660':
            reposeMge = 'true'   
        else : 
            check_ID = idm_login(Emp_id,Emp_pass)
            # print(check_ID)
            reposeMge = check_ID
        #reposeMge = 'true'
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
    openorclose = {
            'openorclose' : ''
    }
    try:
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
        print('s+',Cut_Dept_code2)
        '''now = datetime.now()
        current_time = now.strftime("%H")
        mini = now.strftime("%M")
        print("Current Time =", current_time)'''
        massage = ""
        listcheck = ['507666','229078','240113','241266','251334','255493','255948','256596','258182','270980','275273','279146','280919','284947','293629','295100','297403','297940','298051','298085','298116','299308','299358','303050','304153','304975','305272','305298','308652','308678','310154','311736','311760','311841','311883','311922','322606','322622','322729','322745','322787','326854','327575','327761','330764','331095','331794','331817','331833','331964','333283','409424','409539','413025','413669','413936','415182','415386','416049','416057','417605','418473','420226','425357','427943','428062','428135','439974','442553','444050','447870','451201','454746','458716','460307','464490','464628','464953','467024','467171','467456','467757','468892','478619','480747']
        if Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' or Emp_id == '510951' or Emp_id == '510187':
            openorclose = Course_D.objects.get(PK_Course_D = 9)
            courses = Course_D.objects.all().filter(Access_level = 3).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') 
            print(courses)
        else:  
            openorclose = Course_D.objects.get(PK_Course_D = 10)
            print(Emp_id,Emp_id in listcheck)
            if Emp_id in listcheck:
                courses = Course_D.objects.filter(Course_ID = 'PDD01CO15').annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                print('อยู่ในlist',courses)
            elif Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' or Emp_id == '510951':
                courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                print(courses)
            elif LevelCode == '09' or LevelCode == 'M3' or LevelCode == '10' or LevelCode == 'M4':
                courses = Course_D.objects.all().filter(Access_level = 3).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                print(courses)
                '''elif LevelCode == 'M5' or LevelCode == 'M6' or Emp_id == '510951' or Emp_id == '510187':
                print('fubukai')
                courses = Course_D.objects.all().filter(Access_level = 2).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')'''
                
                '''elif LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2': # เช็คระดับของนักศึกษา ระดับ7-8
                courses = Course_D.objects.all().filter(status = 1).filter(Access_level = 2).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 4).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 3).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 5).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                #selected_course = Course_D.objects.all().filter(status = 1).filter(Access_level = 4 ).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
            elif LevelCode == '09' or LevelCode == 'M3':
                courses = Course_D.objects.all().filter(status = 1).filter(Access_level = 2).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 4).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 3).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 5).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                #selected_course = Course_D.objects.all().filter(status = 1).filter(Access_level = 4 ).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
            elif LevelCode == '10'  or LevelCode == '11' or LevelCode == 'M4' or LevelCode == 'M5' or LevelCode == 'M6' or LevelCode == 'S1':
                courses = Course_D.objects.all().filter(status = 1).filter(Access_level = 2).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 4).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 3).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') | Course_D.objects.all().filter(PK_Course_D = 5).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                #selected_course = Course_D.objects.all().filter(status = 1).filter(Access_level = 5).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') '''
            
            else : 
                #massage = "ไม่มีวิชาที่ท่านสามารถลงทะเบียนได้"
                courses = Course_D.objects.all().filter(Access_level = 3,status = 0).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        competency_data = Course_D.objects.all().filter(Access_level=2,status=1)
        #print(Subject.objects.all().filter(Url_location='https://virtual.yournextu.com/Catalog'))
        #subject = Relation_comp.objects.select_related('Course_ID').filter(Course_ID__Course_ID='PDD01CO08')
        #print(openorclose.Number_App , openorclose.Number_People)
        subjects = Subject.objects.all()
        open_course = len(Course_D.objects.filter(PK_Course_D = 9,status = 1))
        print("open_course",open_course)
        return render(request, 'home.html', {'openorclose': openorclose,'courses': courses,'Cut_Dept_code':Cut_Dept_code,'subjests':subjects,'Fullname':Fullname,'open_course':open_course,'massage':massage})
    except:
        return redirect('login')

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

@csrf_exempt
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

@csrf_exempt
def course_base2(request, PK_Course_D):
    massage=''
    subjects= {
        'subjests' : ''
    }
    sub_subjects= {
        'sub_subjests' : ''
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
    if course.PK_Course_D == 109 or course.PK_Course_D == 110 or course.PK_Course_D == 111 or course.PK_Course_D == 112 or course.PK_Course_D == 113 or course.PK_Course_D == 114 :
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().exclude(Subject_name = 'Managing and Coaching Teams').filter(Sub_level=3)
        if LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2':
            subjects = Subject.objects.all().filter(Sub_level=3)
    elif LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2': # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=1)
        sub_subjects = Subject.objects.filter(Sub_level = 4)
    elif LevelCode == '09' or LevelCode == 'M3' : # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=2)
        sub_subjects = Subject.objects.filter(Sub_level = 4)
    elif LevelCode == '10'  or LevelCode == '11' or LevelCode == 'M4' or LevelCode == 'M5' or LevelCode == 'M6' or LevelCode == 'S1': # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=3)
        sub_subjects = Subject.objects.filter(Sub_level = 5)
    else :
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Subject_ID = 13) | Subject.objects.all().filter(Subject_ID = 10) | Subject.objects.all().filter(Subject_ID = 5) | Subject.objects.all().filter(Subject_ID = 18) | Subject.objects.all().filter(Subject_ID = 17)
        sub_subjects = Subject.objects.all().filter(Subject_ID = 8) | Subject.objects.all().filter(Subject_ID = 4) | Subject.objects.all().filter(Subject_ID = 19) | Subject.objects.all().filter(Subject_ID = 22) 
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Emp_tel = request.POST.get('Emp_tel')
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
            check_same_user = List_Emp.objects.filter(E_ID = Emp_id).count()
            list = [500773,492435,498748,499680,501344,498053,492582,498930,481824,501925,497937,499320,488127,499910,499934,499894,499905,500304,497999,500860,495903,477948,501021,495291,495329,480056,495057,487066,486808,409694,501024,501977,500866]
            if qs_check_user == 0 and check_same_user == 0 :
                Num_Emp = int(Emp_id)
                if Num_Emp not in list:
                    nameget = idm(Emp_id)
                    fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                    Email = request.POST.get('Emp_email')
                    employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = Email, Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                    if course.status == '1' or course.status == 1:
                        employee.save()
                        count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                        update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                        qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                        massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                    else :
                        massage = "ยังไม่เปิดให้ลงทะเบียน"
                else :
                    massage ="ท่านไม่สามารถลงทะเบียนได้เนื่องจากมีจำนวนการเรียนไม่ถึงตามเกณฑ์ที่กำหนด"
            else :
                massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
        else:
            massage = "มีผู้ลงทะเบียนครบแล้ว"

    return render(request,'course_base2.html',{'course': course,'profile':profile,'subjects':subjects,'sub_subjects':sub_subjects,'student':student,'massage':massage,'qs_check_register':qs_check_register})

@csrf_exempt
def course_base3(request, PK_Course_D):
    massage=''
    subjects= {
        'subjests' : ''
    }
    sub_subjects= {
        'sub_subjests' : ''
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
    subjects['subjests'] = 'get0'
    sub_subjects['sub_subjests'] ='get1'
    '''if course.PK_Course_D == 109 or course.PK_Course_D == 110 or course.PK_Course_D == 111 or course.PK_Course_D == 112 or course.PK_Course_D == 113 or course.PK_Course_D == 114 :

        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().exclude(Subject_name = 'Managing and Coaching Teams').filter(Sub_level=3)
        if LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2':
            subjects = Subject.objects.all().filter(Sub_level=3)
    elif LevelCode == '07' or LevelCode == '08' or LevelCode == 'M1' or LevelCode == 'M2': # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=1)
        sub_subjects = Subject.objects.filter(Sub_level = 4)
    elif LevelCode == '09' or LevelCode == 'M3' : # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=2)
        sub_subjects = Subject.objects.filter(Sub_level = 4)
    elif LevelCode == '10'  or LevelCode == '11' or LevelCode == 'M4' or LevelCode == 'M5' or LevelCode == 'M6' or LevelCode == 'S1': # เช็คระดับของนักศึกษา ระดับ7-8
        courses = Course_D.objects.all().filter(status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        subjects = Subject.objects.all().filter(Sub_level=3)
        sub_subjects = Subject.objects.filter(Sub_level = 5)'''
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Emp_tel = request.POST.get('Emp_tel')
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()           
            if qs_check_user == 0:
                if PK_Course_D == '8' or PK_Course_D == 8 :
                    check_user_version2 = List_Emp.objects.filter(E_ID = Emp_id,ref_course = Course_D.objects.get(Course_ID='PDD01CO14')).count()
                    if check_user_version2 == 0:
                        nameget = idm(Emp_id)
                        fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                        if nameget['LevelCode'] == '10' or nameget['LevelCode'] == '10' or nameget['LevelCode'] == 'M4':
                            employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                            if course.status == '1' or course.status == 1:
                                employee.save()
                                count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                                update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                                qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                            else :
                                massage = "ยังไม่เปิดให้ลงทะเบียน"

                        elif nameget['LevelCode'] == '09' or nameget['LevelCode'] == 'M3' :
                            employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                            if course.status == '1' or course.status == 1:
                                employee.save()
                                count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                                update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                                qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                            else :
                                massage = "ยังไม่เปิดให้ลงทะเบียน"
                    else:
                        massage = "ท่านได้ลงทะเบียนแล้วในรุ่นอื่น กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
                elif PK_Course_D == '9' or PK_Course_D == 9:
                    check_user_version1 = List_Emp.objects.filter(E_ID = Emp_id,ref_course = Course_D.objects.get(Course_ID='PDD01CO13')).count()
                    if check_user_version1 == 0:
                        nameget = idm(Emp_id)
                        fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                        if nameget['LevelCode'] == '10' or nameget['LevelCode'] == '10' or nameget['LevelCode'] == 'M4':
                            employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                            if course.status == '1' or course.status == 1:
                                employee.save()
                                count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                                update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                                qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                            else :
                                massage = "ยังไม่เปิดให้ลงทะเบียน"

                        elif nameget['LevelCode'] == '09' or nameget['LevelCode'] == 'M3' :
                            employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                            if course.status == '1' or course.status == 1:
                                employee.save()
                                count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                                update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                                qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                            else :
                                massage = "ยังไม่เปิดให้ลงทะเบียน"
                    else:
                        massage = "ท่านได้ลงทะเบียนแล้วในรุ่นอื่น กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
                else:
                    nameget = idm(Emp_id)
                    fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                    if nameget['LevelCode'] == '10' or nameget['LevelCode'] == '10' or nameget['LevelCode'] == 'M4':
                        employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                        if course.status == '1' or course.status == 1:
                            employee.save()
                            count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                            update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                            qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                            massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                        else :
                            massage = "ยังไม่เปิดให้ลงทะเบียน"

                    elif nameget['LevelCode'] == '09' or nameget['LevelCode'] == 'M3' :
                        employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                        if course.status == '1' or course.status == 1:
                            employee.save()
                            count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                            update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                            qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                            massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                        else :
                            massage = "ยังไม่เปิดให้ลงทะเบียน"

                        '''elif nameget['LevelCode'] == '07' or nameget['LevelCode'] == '08' or nameget['LevelCode'] == 'M1' or nameget['LevelCode'] == 'M2' :
                            employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                            if course.status == '1' or course.status == 1:
                                employee.save()
                                count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                                update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                                qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                                massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                            else :
                                massage = "ยังไม่เปิดให้ลงทะเบียน"'''
                    else :
                        massage = "ท่านไม่ได้อยู่ในกลุ่มระดับ ที่หลักสูตรกำหนด"
            else :
                massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
        else:
            massage = "มีผู้ลงทะเบียนครบแล้ว"

    return render(request,'course_base3.html',{'course': course,'profile':profile,'subjects':subjects,'sub_subjects':sub_subjects,'student':student,'massage':massage,'qs_check_register':qs_check_register})
