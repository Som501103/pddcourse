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
    #try:
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
        listcheck = ['510954','504789','509752','509740','500379','504516','508271','500380','505356','508354','510116','505292','439136','501416','505283','497248','466947','511634','508437','511669','497989','505092','504585','502840','491120','497752','501022','459453','502891','500311','499100','504773','505124','479673','492443','509020','506903','505334','506683','499926','507652','511655','504753','505093','499733','501211','497009','508254','492451','509633','503623','502887','303319','497976','505151','510296','498497','508467','503063','497441','502460','488062','497074','508380','506937','323791','289298','488630','503501','490792','499959','498108','503951','495080','493758','505414','510352','502822','505824','504532','495020','501754','500935','504910','508524','499663','510436','454445','508107','502874','423981','501261','502981','505978','498101','507949','501282','486361','487804','427595','511735','496693','510255','485844','504750','499894','505980','495290','500139','497052','472914','507812','504568','510542','506664','469979','511431','497651','503965','510514','485886','510329','503415','510946','511748','504971','510355','500167','495377','505945','505874','507201','435881','508049','498045','491382','510262','482529','481298','511605','487422','496854','505726','510433','409686','475328','511519','510197','497683','509322','405739','500015','290192','497739']
        listcheck2 = ['464628','303270','322282','413033','444204','454479','469173','470019','281606','409490','430946','466662','466997','470263','478782','489335','491104','235710','235914','464131','466311','490158','307541','409466','414592','426670','430792','463389','466484','468224','485284','489343','489733','492786','492980','497376','497378','497784','499781','501103','501235','202416','266868','318990','330798','430263','471722','489880','490750','493449','494267','497337','497349','497369','501105','501224','501234','501422','501436','501582','501959','502284','489610','497074','499117','499725','501181','501249','502074','502813','503710','504768','504947','505096','506541','506542','495041','500663','501512','501514','502104','502238','503288','503309','503328','503355','503389','504636','507599','507666','508364','508527','509019','509941','505017','505021','505055','505056','506717','506787','506794','508494','509888','510187','510490','510642','510917','510941','510951','511179','511655','511745','512424','504979','507733','507757','508976','512367','506884','507676','507677','507678','507679','507680','508964','508965','508966','508967','508968','510138','510139','510144','510174','510180','511114','511115','511116','511117','511118','511167','511173','512165','512236','512237','512238','512239','512240','512241','512242','512243','512244','512245','512246','512247','512248','512249','512250','512251','512252','512253','512254','512255','512256','512257','512258','512259','512260','512261','512262','512263','512264','512265','512266','512267','512268','512269','512270','512271','512272','512273','512274','512275','512276','512277','512278','512279','512280','512281','512282','512283','512284','512285','512286','512287','512288','512289','512290','512291','512292','512293','512294','512295','512296','512297','512298','512299','512300','512301','512302','512303','512304','512305','512306','512307','512308','512309','512310','512311','512312','512313','512314','512315','512316','512317','512318','512319','512320','512321','512322','512323','512324','512325','512326']
        listcheck3 = ['504947','501105','430792','511179','497074','492613','510642','478782','466311','508527','505055','510917','501422','485284','489880','489733','466484','466662','413033','494267','497784','470019','489335','502104','492980','303270','503288','501582','409466','281606','507757','469814','503389','490158','506542','502074','505021','501512','499725','468224','503309','505056','495248','509019','469173','497337','510951','507733','504979','470530','492786','493449','489343','499781','510187','497378','501959','501235']
        listcheck4 = ['497996','499891','509903','481523','500076','511181','505308','503046','508387','511744','485674','506661','430661','503942','482723','501521','508423','501949','456031','505159','505416','501011','497456','449709','489199','511627','472605','482105','500067','500771','508526','313843','493449','492883','502915','456099','508431','505158','505323','500877','512413','498169','485519','498618','504763','508265','507654','470124','508640','504583','508242','504915','473465','498641','507915','502155','506567','493669','497439','500884','437906','299081','512337','471976','501224','424319','452671','500959','471934','501604','498521','502888','491154','502935','478669','497366','508166','512329','512330','511628','507622','459843','508446','508241','489084','498122','512422','505130','497314','508953','498430','505327','499770','498450','498411','508294','474770','428038','508266','498103','510961','503972','509415','508302','506080','509199','501362','511734','508741','496002','500189','510869','498629','508719','498959','510590','500143','496036','511610','495340','508537','498283','498562','304103','510257','498244','510565','506538','501899','500656','503361','507403','505754','505719','497859','496893','499915','508931','501774','506605','505843','489961','495786','509361','492778','503366','495374','497572','503171','500760','507251','493350','268404','507808','511617','508958','274057','498564','512193','510892','503020','478473','510273','506902','497004','509067','512376','499934','507415','509896','500287','498090','503317','505540','501164','495239','510867','502937','495524','496512','307999','507164','502211','499657','402888','443664','451706','511059','507946','510550','510562','501303','499857','506092','506995','508330','507405','305696','506326','511762','481808','500204','503412','505073','501729','510316','505498','501559','512120','510538','329789','511618','511702','510566','499387','507038','422757','507594','511665','504708','507130','507795','498800','483389','442391','480315','511907','496439','470085','504840','505358','509256','511501','498906','500181','501345','509950','500382','498218','506082','496604','417671','454089','510553','504605','496351','506087','511767','503355','511173','503328','511167','505017','409490','512424','497349','490158','507757','469173','499781','501582','492786','466311','489335','503288','466662']
        if Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' or Emp_id == '510951' or Emp_id == '510187':
            courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D') 
            print(courses)
        else:
            if Emp_id in listcheck4 or Emp_id in listcheck:
                print('isin')
                courses = Course_D.objects.filter(Duration = 4512).exclude(PK_Course_D = 24).exclude(PK_Course_D = 25).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
            elif Emp_id in listcheck:
                courses = Course_D.objects.filter(Duration = 4512).exclude(PK_Course_D = 18).exclude(PK_Course_D = 19).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
            elif Emp_id == '501103' or Emp_id == '503710' or Emp_id == '499781' or Emp_id == '507599' or Emp_id == '492613' or Emp_id == '497784' or Emp_id == '510951':
                courses = Course_D.objects.all().annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
                print(courses)
            else : 
                #massage = "ไม่มีวิชาที่ท่านสามารถลงทะเบียนได้"
                courses = Course_D.objects.all().filter(Duration = 4512).annotate(Gap_number =F('Number_App') - F('Number_People')).order_by('-PK_Course_D')
        competency_data = Course_D.objects.all().filter(Access_level=2,status=1)
        #print(Subject.objects.all().filter(Url_location='https://virtual.yournextu.com/Catalog'))
        #subject = Relation_comp.objects.select_related('Course_ID').filter(Course_ID__Course_ID='PDD01CO08')
        #print(openorclose.Number_App , openorclose.Number_People)
        subjects = Subject.objects.all()
        open_course = len(Course_D.objects.filter(PK_Course_D = 24,status = 1))
        print("open_course",open_course)
        openorclose = Course_D.objects.get(PK_Course_D = 24)
        return render(request, 'home.html', {'openorclose': openorclose,'courses': courses,'subjests':subjects,'open_course':open_course,'massage':massage})
    #except:
        #return redirect('login')

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
    if course.Number_App <= course.Number_People:
        massage = "มีผู้ลงทะเบียนครบแล้ว"
    print('this',massage)
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
            #list = ['408892','477150','498623','470530','492087','497337','497542','497882','498893','499157','499346','499634','499934','499959','500304','500866','501925','502294','501977','509161','460365','503062','509308','505107','486688','498053','487202','503047','508959','404018','510542','500765','422595','315405','409694','505815','505984','490239','509559','510266','510589','510590','508616','502420','509011','504979','507733','499146','502055','499777','510263','507199','498237','289298','456031','460323','464555','479631','235956','308296','279447','416138','331760','467723','485315','509437','509439','509441','510487','510565','510573','510587','496253','502160','503388','508252','509752','478669','498523','505310','500903','499320','501021','408363','415140','445593','467927','471837','477948','480056','481337','488127','492053','492736','492786','495045','495087','495156','497227','497274','497295','498312','499307','499311','499723','499905','500326','500706','500860','490190','306731','469173','258182']
            list = []
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