from django.db import models


# Create your models here.

# ************ head models ***************

class City_master(models.Model):
    city = models.CharField(max_length=60 , blank=True , null=True)
    status = models.CharField(max_length=10 , blank=True , null=True)

    def __str__(self):
        return self.city
    
class Location_Master(models.Model):
    city = models.ForeignKey(City_master, on_delete = models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length = 100, blank=True, null=True)
    status = models.CharField(max_length = 10, blank=True, null=True)

    def __str__(self):
        return self.location

class Category_Master(models.Model):
    category = models.CharField(max_length=50,blank=True,null=True)
    status = models.CharField(max_length = 10, blank=True, null=True)

    def __str__(self):
        return self.category
    
class SubCategory_Master(models.Model):
    category = models.ForeignKey(Category_Master, on_delete=models.CASCADE , blank=True , null=True)
    sub_category = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length = 10, blank=True, null=True)
    
    def __str__(self):
        return self.sub_category
    
class University_Master(models.Model):
    university = models.CharField(max_length=100 , blank=True , null=True)
    status = models.CharField(max_length = 10, blank=True, null=True)

    def __str__(self):
        return self.university 
    
class Collage_Master(models.Model):
    university = models.ForeignKey(University_Master,on_delete=models.CASCADE, blank=True , null=True)
    collage = models.CharField(max_length = 100 , blank=True , null=True)
    status = models.CharField(max_length = 10, blank=True, null=True)

    def __str__(self):
        return self.collage
    
class Course_Master(models.Model):
    course = models.CharField(max_length=100 , blank=True , null=True)
    category = models.ForeignKey(Category_Master, on_delete=models.CASCADE, blank=True , null=True)
    sub_category = models.ForeignKey(SubCategory_Master , on_delete=models.CASCADE , blank=True , null=True)
    duration = models.CharField(max_length=70 , blank=True , null=True)
    fees = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length = 10, blank=True, null=True)

    def __str__(self):
        return self.course
    

# ************** Master Models ***************
    
class Stu_Inquiry(models.Model):
    name = models.CharField(max_length = 100 , blank=True , null=True)
    university = models.ForeignKey(University_Master , on_delete=models.CASCADE , blank=True , null=True)
    collage = models.ForeignKey(Collage_Master , on_delete=models.CASCADE , blank=True , null=True)
    course = models.ForeignKey(Course_Master, on_delete=models.CASCADE , blank=True , null=True)
    email = models.EmailField(max_length=150 , blank=True , null=True)
    mobile_no = models.CharField(max_length=10 , blank=True , null=True)
    home_mobile_no = models.CharField(max_length=10 , blank=True , null=True)
    status = models.CharField(max_length=10 , blank=True , null=True)

    def __str__(self):
        return self.name
    
class Stu_Admit(models.Model):
    stu_name = models.ForeignKey(Stu_Inquiry , on_delete = models.CASCADE , blank=True , null=True)
    aadhar_no = models.CharField(max_length=13 , blank=True , null=True)
    location = models.ForeignKey(Location_Master , on_delete=models.CASCADE , blank=True , null=True)
    course = models.ForeignKey(Course_Master,on_delete=models.CASCADE,blank=True,null=True)
    duration = models.CharField(max_length = 50,blank=True,null=True)
    date = models.DateField(null=True)
    total_fees = models.IntegerField(null=True, blank=True, default=0)
    paid_now = models.IntegerField(null=True, blank=True, default=0)
    balance_fees = models.IntegerField(null=True, blank=True, default=0)
    next_followup_date = models.DateField(null=True)
    system = models.CharField(max_length=30 , blank=True , null = True)
    fee_close = models.CharField(max_length=10 , blank=True , null=True)

    def __str__(self):
        return self.name
    
class Fee_followup(models.Model):
    today_date = models.DateField(null=True)
    student_name = models.ForeignKey(Stu_Admit,on_delete=models.CASCADE , blank=True , null=True)
    course = models.CharField(max_length=50,blank=True,null=True)
    fees_paid = models.IntegerField(null=True, blank=True, default=0)
    balance_till = models.IntegerField(null=True, blank=True, default=0)
    now_paid = models.IntegerField(null=True, blank=True, default=0)
    total_balance_pending = models.IntegerField(null=True, blank=True, default=0)
    next_follow_up_date = models.DateField(null=True)
    
    def __str__(self):
        return self.today_date , self.student_name
    
    def save(self, *args, **kwargs):
        # Call the parent class's save() method
        super(Fee_followup, self).save(*args, **kwargs)
        
        # Update Stu_Admit fields based on Fee_followup data
        student = self.student_name
        student.paid_now = self.fees_paid
        student.balance_fees = self.total_balance_pending
        student.next_followup_date = self.next_follow_up_date
        student.fee_close = "Yes" if self.total_balance_pending == 0 else "No"
        student.save()
    
    # def save(self, *args, **kwargs):
    #     # Update Stu_Admit instance when saving Fee_followup instance
    #     if self.student_name:
    #         self.student_name.paid_now += self.now_paid
    #         self.student_name.balance_fees += self.balance_till - self.now_paid
    #         self.student_name.next_followup_date = self.next_follow_up_date
    #         if self.student_name.balance_fees == 0:
    #             self.student_name.fee_close = 'Yes'
    #         else:
    #             self.student_name.fee_close = 'No'
    #         self.student_name.save()
    #     super(Fee_followup, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    # # Update Stu_Admit instance when saving Fee_followup instance
    #     if self.student_name:
    #         updated_paid_now = self.student_name.paid_now + int(self.now_paid)
    #         updated_balance_fees = self.student_name.balance_fees + int(self.balance_till) - int(self.now_paid)

    #         self.student_name.paid_now = updated_paid_now
    #         self.student_name.balance_fees = updated_balance_fees
    #         self.student_name.next_followup_date = self.next_follow_up_date

    #         if updated_balance_fees == 0:
    #             self.student_name.fee_close = 'Yes'
    #         else:
    #             self.student_name.fee_close = 'No'

    #         # Save Fee_followup instance first
    #         super(Fee_followup, self).save(*args, **kwargs)

    #         # Save Stu_Admit instance after updating its fields
    #         self.student_name.save()
    #     else:
    #         super(Fee_followup, self).save(*args, **kwargs)
            
    # def save(self, *args, **kwargs):
    #     # Update Stu_Admit instance when saving Fee_followup instance
    #     if self.student_name:
    #         updated_paid_now = self.student_name.paid_now + int(self.now_paid)
    #         updated_balance_fees = self.student_name.balance_fees + int(self.balance_till) - int(self.now_paid)

    #         self.student_name.paid_now = updated_paid_now
    #         self.student_name.balance_fees = updated_balance_fees
    #         self.student_name.next_followup_date = self.next_follow_up_date

    #         if updated_balance_fees == 0:
    #             self.student_name.fee_close = 'Yes'
    #         else:
    #             self.student_name.fee_close = 'No'

    #         # Save Stu_Admit instance after updating its fields
    #         self.student_name.save()
        
    #     # Save Fee_followup instance after updating Stu_Admit fields
    #     super(Fee_followup, self).save(*args, **kwargs)