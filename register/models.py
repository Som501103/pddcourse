from django.db import models
from django.contrib.auth.models import User

class MT_User(models.Model):
    PK_User = models.AutoField(primary_key=True)
    User_ID = models.CharField(max_length=10,null=True)
    Division_ID = models.CharField(max_length=5,null=True)
    Permit_Group = models.CharField(max_length=5,null=True)
    Key_Date =  models.DateTimeField(auto_now_add=True)
    
       
class Course_D(models.Model):
    PK_Course_D = models.AutoField(primary_key=True)
    Course_ID = models.CharField(max_length=15, unique=True)
    Course_Name = models.CharField(max_length=300,null=True)
    CourseType_ID = models.CharField(max_length=2,null=True)
    Batch_Type = models.CharField(max_length=1,null=True)
    Batch = models.CharField(max_length=300,null=True)
    Start_Date = models.DateField(null=True)
    End_Date = models.DateField(null=True)
    Duration = models.IntegerField(null=True)
    Location = models.CharField(max_length=300,null=True)
    Area_ID = models.CharField(max_length=3,null=True)
    Number_App = models.IntegerField(null=True)
    Number_People = models.IntegerField(null=True)
    BudgetApp_1 = models.DecimalField(max_digits=13, decimal_places=2,null=True)
    BudgetApp_2 = models.DecimalField(max_digits=13, decimal_places=2,null=True)
    BudgetPay_1 = models.DecimalField(max_digits=13, decimal_places=2,null=True)
    BudgetPay_2 = models.DecimalField(max_digits=13, decimal_places=2,null=True)
    Key_By = models.CharField(max_length=10,null=True)
    Key_Date = models.DateField(auto_now_add=True)
    RegisterStatus = models.BooleanField(null=True)
    RegisterType = models.CharField(max_length=15,null=True)
    Start_Time = models.DateTimeField(null=True)
    End_Time = models.DateTimeField(null=True)
    status = models.IntegerField(null=True, default=1)
    def __str__(self):
        return self.Course_ID, self.Course_Name


class List_Dept(models.Model):
    PK_List = models.AutoField(primary_key=True)
    ref_course = models.ForeignKey(Course_D, related_name='List_Dept_Course_D',on_delete = models.CASCADE,null= True)
    ref_group = models.CharField(max_length=5,null=True)
    dept = models.CharField(max_length=30,null=True)  
    number_dept = models.IntegerField(null=True)
    number_stamp = models.IntegerField(null=True)
    status = models.IntegerField(default=1, null=True)
    # status 1= on, 0 = offf


class List_Emp(models.Model):
    PK_List_Emp = models.AutoField(primary_key=True)
    ref_course = models.ForeignKey(Course_D, related_name='List_Emp_Course_D',on_delete = models.CASCADE,null= True,default='0')
    E_ID = models.CharField(max_length=10,null=True,blank=True)
    Fullname = models.CharField(max_length=70,null=True,blank=True)
    Position = models.CharField(max_length=20,null=True,default='หผ.')
    Level = models.CharField(max_length=2,null=True,default='08')
    Dep = models.CharField(max_length=100,null=True,blank=True)
    Regist_Date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1, null=True)
    # status 1= on, 0 = offf

    def __str__(self):
        return self.E_ID, self.ref_course


























# Create your models here.
