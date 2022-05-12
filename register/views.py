from os import access
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import MT_User, Course_D, List_Dept, List_Emp, Course_Director, Check_Loginerror, Check_Staff_End, Subject , Course_out
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
    
    if request.method == 'POST':
        Emp_id = request.POST.get('StaffID')
        #Emp_pass = request.POST.get('StaffPS')
        check_error = len(Check_Loginerror.objects.filter(E_ID=Emp_id))
        #check_error = 1 #bypass
        if check_error > 0 :
        # Emp_id == '303270' or Emp_id == '501249' or Emp_id == '489343' or Emp_id == '235859' or Emp_id == '444717' or Emp_id == '444660':
            reposeMge = 'true'   
        else : 
            #check_ID = idm_login(Emp_id,Emp_pass)
            # print(check_ID)
            reposeMge = 'true'
        #reposeMge = 'true'
        if reposeMge == 'true':
            '''nameget = idm(Emp_id)
            # print(nameget)
            Fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
            Position = nameget['PositionDescShort']
            LevelCode = nameget['LevelCode']
            Dept = nameget['DepartmentShort']
            Dept_code = nameget['NewOrganizationalCode']
            RegionCode = nameget['RegionCode']
            Email = nameget['Email']
            request.session['Fullname'] = Fullname
            request.session['Position'] = Position
            request.session['LevelCode'] = LevelCode
            request.session['Department'] = Dept
            request.session['Dept_code'] = Dept_code
            request.session['RegionCode'] = RegionCode
            request.session['Email'] = Email'''
            request.session['Emp_id'] = Emp_id
            print('fubukai')
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
        '''Fullname = request.session['Fullname']
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
        now = datetime.now()
        current_time = now.strftime("%H")
        mini = now.strftime("%M")
        print("Current Time =", current_time)'''
        massage = ""
        listcheck = ['480705','301812','258182','464393','477891','473041','491031','490718','474762','459518','482896','464482','305696','422919','401989','448444','472817','477493','492477','425917','307999','481280','482692','470158','316914','315405','486361','279447','418643','311443','461727','476594','441785','444092','427595','322478','445593','284858','471837','408892','419453','497295','415140','497757','433643','498643','485438','497040','489555','464987','319077','422935','317407','470297','488290','481638','314768','496821','499781','492786','498001','477061','482553','495318','485496','488313','497989','491382','496560','498959','472134','500935','485894','485747','296350','496942','497542','497683','498430','501413','502283','498271','499157','498646','501022','500311','498437','496796','497651','498144','498436','497642','497737','498227','498179','498118','497882','498962','499960','501417','498663','485844','498143','501235','497378','500706','499926','511481','511431','510978','488062','481719','485315','459453','466191','428402','495081','488119','497428','442121','497933','498631','487414','496849','497716','296538','495447','490239','495290','495101','500030','497841','498513','445420','497032','501546','501997','504532','498992','498729','502981','501282','501670','499585','502900','505327','502258','502336','505938','501608','502957','498523','498071','497911','478669','497901','504789','503951','497553','497541','498042','498237','500175','499777','499992','499100','490035','497339','500958','498815','499412','498351','499771','496027','499857','499738','493546','505087','505151','505957','505958','501104','504435','500765','506213','504832','500139','504516','504907','504753','504749','502822','501215','504478','502834','504474','497568','502874','503972','501754','501626','505107','505811','505095','502840','503952','497951','505092','505373','508204','506479','506647','496253','495227','501136','505540','508537','508763','508242','505960','506401','506402','495251','507790','508479','502160','508425','508252','503388','505320','496693','502055','506062','498582','502420','504465','503877','504843','506665','505812','506477','505980','506320','503047','507607','506893','508436','505719','504910','508214','501362','500189','507644','507649','508231','508770','505362','506160','505257','508314','510944','510587','500903','501501','510910','505581','501220','510487','510573','509439','509437','509441','510565','510518','510444','509820','510118','503928','509378','509752','509740','506511','507199','505260','504666','506096','505377','504711','506598','505034','508437','506892','502168','508616','506341','505824','505162','507808','508087','505987','505815','505984','509937','510818','509361','508337','510433','509359','510542','510255','510218','511199','508959','510650','510585','510554','509308','505433','503210','510436','509938','509021','510641','510536','510543','510970','509092','509161','510352','510400','509693','510549','510083','509119','510263','510355','510296','509103','506800','507743','510869','510266','510461','509737','509559','509216','509317','510590','510589','509011']
        if Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' or Emp_id == '510951' or Emp_id == '510187':
            openorclose = Course_D.objects.get(PK_Course_D = 10)
            courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') 
            print(courses)
        else: 
            openorclose = Course_D.objects.get(PK_Course_D = 10)
            print(Emp_id,Emp_id in listcheck)
            if Emp_id in listcheck:
                courses = Course_D.objects.filter(Course_ID = 'PDD01CO21').annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
            elif Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' or Emp_id == '510951':
                courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                print(courses)
            #elif LevelCode == '09' or LevelCode == 'M3' or LevelCode == '10' or LevelCode == 'M4':
            #    courses = Course_D.objects.all().filter(Access_level = 3).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
            #    print(courses)
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
                courses = Course_D.objects.all().filter(Access_level = 1,status = 1).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        competency_data = Course_D.objects.all().filter(Access_level=2,status=1)
        #print(Subject.objects.all().filter(Url_location='https://virtual.yournextu.com/Catalog'))
        #subject = Relation_comp.objects.select_related('Course_ID').filter(Course_ID__Course_ID='PDD01CO08')
        #print(openorclose.Number_App , openorclose.Number_People)
        subjects = Subject.objects.all()
        open_course = len(Course_D.objects.filter(PK_Course_D = 9,status = 1))
        print("open_course",open_course)
        return render(request, 'home.html', {'openorclose': openorclose,'courses': courses,'subjests':subjects,'open_course':open_course,'massage':massage})
    except:
        return redirect('login')

def course_title(request, PK_Course_D):
    Emp_id = request.session['Emp_id'] 
    profile = {
            'Emp_id' : Emp_id,
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
    #Fullname = request.session['Fullname']
    #Dept = request.session['Department']
    #LevelCode = request.session['LevelCode']
    #Email = request.session['Email']
    #print(PK_Course_D)
    student = List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D))
    qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
    if qs_check_register > 0:
        massage = "ท่านได้ลงทะเบียนแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"
    # print(subjects)
    profile = {
            'Emp_id' : Emp_id,
    }
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Email = request.POST.get('Emp_email')
            Emp_tel = request.POST.get('Emp_tel')
            Emp_pre = request.POST.get('Emp_pre')
            Emp_name = request.POST.get('Emp_name')
            Emp_surename = request.POST.get('Emp_surename')
            Emp_position = request.POST.get('Emp_position')
            Emp_dep = request.POST.get('Emp_dep')
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
            check_same_user = List_Emp.objects.filter(E_ID = Emp_id).count()
            list = ['408892','477150','498623','470530','492087','497337','497542','497882','498893','499157','499346','499634','499934','499959','500304','500866','501925','502294','501977','509161','460365','503062','509308','505107','486688','498053','487202','503047','508959','404018','510542','500765','422595','315405','409694','505815','505984','490239','509559','510266','510589','510590','508616','502420','509011','504979','507733','499146','502055','499777','510263','507199','498237','289298','456031','460323','464555','479631','235956','308296','279447','416138','331760','467723','485315','509437','509439','509441','510487','510565','510573','510587','496253','502160','503388','508252','509752','478669','498523','505310','500903','499320','501021','408363','415140','445593','467927','471837','477948','480056','481337','488127','492053','492736','492786','495045','495087','495156','497227','497274','497295','498312','499307','499311','499723','499905','500326','500706','500860','490190','306731','469173','258182']
            print(qs_check_user,check_same_user)
            if qs_check_user == 0 or check_same_user == 0 :
                Num_Emp = int(Emp_id)
                if Num_Emp not in list:
                    print('fubukai')
                    fullname = Emp_pre+Emp_name+' '+Emp_surename
                    employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = Emp_position,Level = '00' ,Dep = Emp_dep, Email = Email, Dept_code='00' , Tel = Emp_tel , Gender='-')
                    if course.status == '1' or course.status == 1:
                        employee.save()
                        print('check 2')
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
            listcheck = ['507666','229078','240113','241266','251334','255493','255948','256596','258182','270980','275273','279146','280919','284947','293629','295100','297403','297940','298051','298085','298116','299308','299358','303050','304153','304975','305272','305298','308652','308678','310154','311736','311760','311841','311883','311922','322606','322622','322729','322745','322787','326854','327575','327761','330764','331095','331794','331817','331833','331964','333283','409424','409539','413025','413669','413936','415182','415386','416049','416057','417605','418473','420226','425357','427943','428062','428135','439974','442553','444050','447870','451201','454746','458716','460307','464490','464628','464953','467024','467171','467456','467757','468892','478619','480747']
            listcheck2 = ['437516','333631','498411','497435','500704','497988','495696','492011','501416','506523','505108','504626','507656','507657','481442','488876','497043','497022','499274','500142','498082','505274','505094','510935','511199','503927','510933','491120','498623','489597','490116','497474','492126','495050','495310','498481','498880','501603','502895','505126','502247','505327','505793','499585','505827','507584','497200','481523','464555','502267','472516','491780','492477','497472','440585','510934','444694','481086','467723','477891','497476','499311','506676','501543','505297','505331','509030','499146','206240','456031']
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()           
            if qs_check_user == 0:
                if PK_Course_D == '8' or PK_Course_D == 8 :
                    check_user_version2 = List_Emp.objects.filter(E_ID = Emp_id,ref_course = Course_D.objects.get(Course_ID='PDD01CO14')).count()
                    if check_user_version2 == 0:
                        nameget = idm(Emp_id)
                        fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                        if Emp_id in listcheck:
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
                    if Emp_id in listcheck:
                        employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                        if course.status == '1' or course.status == 1:
                            employee.save()
                            count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                            update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                            qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                            massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                        else :
                            massage = "ยังไม่เปิดให้ลงทะเบียน"
                    elif Emp_id in listcheck2:
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

@csrf_exempt
def course_base_firebase(request, PK_Course_D):
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
   
    if request.method == 'POST':
        if course.Number_App > course.Number_People:
            Emp_tel = request.POST.get('Emp_tel')
            listcheck = ['507666','229078','240113','241266','251334','255493','255948','256596','258182','270980','275273','279146','280919','284947','293629','295100','297403','297940','298051','298085','298116','299308','299358','303050','304153','304975','305272','305298','308652','308678','310154','311736','311760','311841','311883','311922','322606','322622','322729','322745','322787','326854','327575','327761','330764','331095','331794','331817','331833','331964','333283','409424','409539','413025','413669','413936','415182','415386','416049','416057','417605','418473','420226','425357','427943','428062','428135','439974','442553','444050','447870','451201','454746','458716','460307','464490','464628','464953','467024','467171','467456','467757','468892','478619','480747']
            listcheck2 = ['437516','333631','498411','497435','500704','497988','495696','492011','501416','506523','505108','504626','507656','507657','481442','488876','497043','497022','499274','500142','498082','505274','505094','510935','511199','503927','510933','491120','498623','489597','490116','497474','492126','495050','495310','498481','498880','501603','502895','505126','502247','505327','505793','499585','505827','507584','497200','481523','464555','502267','472516','491780','492477','497472','440585','510934','444694','481086','467723','477891','497476','499311','506676','501543','505297','505331','509030','499146','206240','456031']
            qs_check_user = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()           
            if qs_check_user == 0:
                if PK_Course_D == '8' or PK_Course_D == 8 :
                    check_user_version2 = List_Emp.objects.filter(E_ID = Emp_id,ref_course = Course_D.objects.get(Course_ID='PDD01CO14')).count()
                    if check_user_version2 == 0:
                        nameget = idm(Emp_id)
                        fullname = nameget['TitleFullName']+nameget['FirstName']+' '+nameget['LastName']
                        if Emp_id in listcheck:
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
                    if Emp_id in listcheck:
                        employee = List_Emp(ref_course=course, E_ID = Emp_id, Fullname= fullname, Position = nameget['PositionDescShort'],Level = nameget['LevelCode'] ,Dep = nameget['DepartmentShort'], Email = nameget['Email'], Dept_code=nameget['NewOrganizationalCode'] , Tel = Emp_tel , Gender=nameget['GenderCode'])
                        if course.status == '1' or course.status == 1:
                            employee.save()
                            count = len(List_Emp.objects.filter(ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D), status = 1))
                            update_num_student = Course_D.objects.filter(PK_Course_D = PK_Course_D).update(Number_People = count)
                            qs_check_register = List_Emp.objects.filter(E_ID = Emp_id, ref_course = Course_D.objects.get(PK_Course_D=PK_Course_D)).count()
                            massage = "ท่านได้ลงทะเบียนสำเร็จแล้ว กรุณาตรวจสอบ e-mail ของท่าน ถ้าไม่ถูกต้องกรุณาติดต่อที่เบอร์ 5858 หรือ แจ้งใน HRD Connext"

                        else :
                            massage = "ยังไม่เปิดให้ลงทะเบียน"
                    elif Emp_id in listcheck2:
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

    return render(request,'course_base_firebase.html',{'course': course,'profile':profile,'subjects':subjects,'sub_subjects':sub_subjects,'student':student,'massage':massage,'qs_check_register':qs_check_register})

def outhome(request):
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
        
        massage = ""
        courses = Course_out.objects.all()
        return render(request, 'home.html', {'courses': courses})
    except:
        return redirect('login')