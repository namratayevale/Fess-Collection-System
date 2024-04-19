from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login as auth_login , logout
from django.contrib import messages
from django.urls import reverse
from .models import *
#import for paginator
from django.core.paginator import Paginator
#import for csv file
import csv
from django.http import HttpResponse,FileResponse
#import for pdf file
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#for search
from django.http import JsonResponse
#  paper rotation for pdf
from reportlab.lib.pagesizes import letter, landscape
# for retrive data 
from django.http import JsonResponse




# *************** Login View *****************
def login(request):
    return render(request,'login/page.html')

def image(request):
    return render(request,'login/loginimg.html')

def headlogin(request):
    return render(request,'login/headlogin.html')

def masterlogin(request):
    return render(request,'login/masterlogin.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('head_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if not username or not password:
        #     messages.error(request, 'Enter Username')
        #     return redirect(reverse('headlogin'))
        
        # if not password:
        #     messages.error(request, 'Enter Password')
        #     return redirect('headlogin')

        validateuser = authenticate(request , username=username , password=password)
        if validateuser is not None and validateuser.is_staff:
            auth_login(request,validateuser)
            return redirect('head_dashboard')
        else:
            error_massage = 'Invalid credentials or not an admin account'
            messages.error(request, error_massage)
            return render(request,'login/headlogin.html')
    else:
        return render(request,'login/headlogin.html', {})

def master_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        masteruser = authenticate(request, username=username, password=password)
        if masteruser is not None:
            auth_login(request, masteruser)
            return redirect('dashboard')  # Redirect to user dashboard
        else:
            # Authentication failed
            error_msg = ' Invalid credentials'
            messages.error(request,error_msg)
            return render(request, 'login/masterlogin.html')
    else:
        return render(request, 'login/masterlogin.html')

def admin_logout(request):
    logout(request)
    return redirect('login')
    

# <<<<<<<<<< Head View >>>>>>>>>>

# ************** City View ***************

def city(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        status = request.POST.get('status')
        cities = City_master.objects.create(city=city,status=status)
        cities.save()
        return redirect(reverse('citylist'))
    else:
        return render(request, 'head/headForm/city-master.html')

def citylist(request):
    
    # cities = City_master.objects.filter(status='Active')
    cities = City_master.objects.all()
    
    # code for paginatin
    paginator = Paginator(cities,5)  # for count data on each page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    totalpage = page_obj.paginator.num_pages     # for going direct last page
    # page_obj = paginator.get_page(page_number)
    # return render(request, 'head/headList/city_list.html', {'page_obj': page_obj})
    data = {
        'cities':page_obj,
        # 'lastpage':totalpage,
        "page_obj": page_obj,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }
    return render(request, 'head/headList/city_list.html',data)
    
# def citylist(request):
#     show_inactive = request.GET.get('show_inactive') == 'true'
#     #  show active and inactive city list onclick button
#     if show_inactive:
#         cities = City_master.objects.filter(status='Inactive')
#     else:
#         cities = City_master.objects.filter(status='Active')

#     paginator = Paginator(cities, 5)        # for count data on each page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     totalpage = page_obj.paginator.num_pages
#     data = {
#         'cities': page_obj,
#         'show_inactive': show_inactive,
#         'totalpagelist': [n+1 for n in range(totalpage)]
#     }
#     return render(request, 'head/headList/city_list.html', data)

def update_city(request, id):
    record = City_master.objects.get(id=id)
    if request.method == 'POST':
        city = request.POST.get('city')
        status = request.POST['status']
        record.city = city
        record.status = status
        record.save()
        return redirect(reverse('citylist'))
    else:
        return render(request, 'head/update/cityList_Update.html', context={"record":record})




def citylist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="city_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['cityname','status'])

    cities = City_master.objects.all()
    for city in cities:
        writer.writerow([city.city,city.status])
    return response

def citylist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['City Name', 'Status']]
    cities = City_master.objects.all()
    for city in cities:
        data.append([city.city, city.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="city_data.pdf"'
    response.write(pdf_data)
    return response

def delete_city(request,id):
    dcity = City_master.objects.get(id=id)
    dcity.delete()
    return redirect(reverse('citylist'))

def search(request):
    pass
#     letter = request.GET.get('letter')
#     cities = City_master.objects.filter(name__istartswith=letter)
#     city_names = [city.city for city in cities]
    # return JsonResponse({'cities': city_names})

#  *********** Location View ************  

def location(request):
    active_cities = City_master.objects.filter(status='Active')
    if request.method == 'POST':
        city = request.POST.get('city')
        location = request.POST.get('location')
        status = request.POST.get('status')
        cities = City_master.objects.get(id=city)
        locations = Location_Master.objects.create(city_id=city,location=location,status=status)
        locations.save()
        return redirect(reverse('locationlist'))

    else:
        cities = City_master.objects.all()
        return render(request, 'head/headForm/location-master.html',{'cities':active_cities})


def locationlist(request):
    locations = Location_Master.objects.all()

    paginator = Paginator(locations,5)  # for count data on each page
    page_number = request.GET.get('page')
    location1 = paginator.get_page(page_number)
    totalpage = location1.paginator.num_pages     # for going direct last page
    data = {
        'locations':location1,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }

    return render(request, 'head/headList/location_list.html',context= data)
 
def delete_location(request,id):
    dloca = Location_Master.objects.get(id=id)
    dloca.delete()
    return redirect(reverse('locationlist'))

def update_location(request,id):
    city_id = City_master.objects.filter(status='Active')
    record = Location_Master.objects.get(id=id)
    if request.method == 'POST':
        city_id = request.POST.get('city')
        location = request.POST.get('location')
        status = request.POST.get('status')
        record.city_id = city_id
        record.location = location
        record.status = status
        record.save()
        return redirect(reverse('locationlist'))
    else:
        return render(request, 'head/update/Location_Update.html', context={"record":record,'city_id':city_id})
    
def locationlist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="location_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['city', 'location' ,'status'])

    locations = Location_Master.objects.all()
    for loc in locations:
        writer.writerow([loc.city,loc.location,loc.status])
    return response

def locationlist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['City','Location', 'Status']]
    locations = Location_Master.objects.all()
    for loc in locations:
        data.append([loc.city,loc.location,loc.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="location_data.pdf"'
    response.write(pdf_data)
    return response

# ************ Category view ***************

def categorylist(request):
    categoryData = Category_Master.objects.all()
        # code for paginatin
    paginator = Paginator(categoryData,4)  # for count data on each page
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    totalpage = categories.paginator.num_pages     # for going direct last page
    data = {
        'categoryData':categories,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }

    return render(request, 'head/headList/category_list.html',context=data)

def category(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        status = request.POST.get('status')
        categories = Category_Master.objects.create(category=category,status=status)
        categories.save()
        return redirect(reverse('categorylist'))
    else:
        return render(request, 'head/headForm/category.html')
    
def update_category(request,id):
    record = Category_Master.objects.get(id=id)
    if request.method == 'POST':
        category = request.POST.get('category')
        status = request.POST['status']
        record.category = category
        record.status = status
        record.save()
        return redirect(reverse('categorylist'))
    else:
        return render(request, 'head/update/category_update.html',context={'record':record})

def delete_category(request,id):
    dcate = Category_Master.objects.get(id=id)
    dcate.delete()
    return redirect(reverse('categorylist'))

def categorylist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="category_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['category' ,'status'])

    categories = Category_Master.objects.all()
    for cat in categories:
        writer.writerow([cat.category,cat.status])
    return response

def categorylist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['Category', 'Status']]
    categories = Category_Master.objects.all()
    for cat in categories:
        data.append([cat.category,cat.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="category_data.pdf"'
    response.write(pdf_data)
    return response

# ************ Sub-Category view ****************

def subcategorylist(request):
    sub_category = SubCategory_Master.objects.all()
    # pagination code
    paginator = Paginator(sub_category,4)  # for count data on each page
    page_number = request.GET.get('page')
    subcategories = paginator.get_page(page_number)
    totalpage = subcategories.paginator.num_pages     # for going direct last page
    data = {
        'sub_category':subcategories,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }

    return render(request, 'head/headList/subCategory_list.html',context=data)

def sub_category(request):
    active_categories = Category_Master.objects.filter(status='Active')
    if request.method == 'POST':
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        status = request.POST.get('status')
        category = Category_Master.objects.get(id=category)
        sub_categories = SubCategory_Master.objects.create(category=category,sub_category=sub_category,status=status)
        sub_categories.save()
        return redirect(reverse('subcategorylist'))
    else:
        categories = Category_Master.objects.all()
        return render(request, 'head/headForm/sub-category.html',{'categories':active_categories})

def update_subcategory(request,id):
    category_id = Category_Master.objects.filter(status='Active')
    record = SubCategory_Master.objects.get(id=id)
    if request.method == 'POST':
        category_id = request.POST.get('category')
        subcategory = request.POST.get('sub_category')
        status = request.POST.get('status')
        record.category_id = category_id
        record.sub_category = subcategory
        record.status = status
        record.save()
        return redirect(reverse('subcategorylist'))
    else:
        return render(request, 'head/update/Subcategory_Update.html', context={"record":record,'category_id':category_id})
    
def delete_subcategory(request,id):
    dcate = SubCategory_Master.objects.get(id=id)
    dcate.delete()
    return redirect(reverse('subcategorylist'))

def subcategorylist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="subcategory_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['category', 'subcategory' ,'status'])

    subcategories = SubCategory_Master.objects.all()
    for sub in subcategories:
        writer.writerow([sub.category,sub.sub_category,sub.status])
    return response

def subcategorylist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['Category','Subcategory', 'Status']]
    subcategories = SubCategory_Master.objects.all()
    for cat in subcategories:
        data.append([cat.category,cat.sub_category,cat.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="subcategory_data.pdf"'
    response.write(pdf_data)
    return response

# ************ University View **************

def university(request):
    if request.method == 'POST':
        university = request.POST.get('university')
        status = request.POST.get('status')
        universities = University_Master.objects.create(university=university,status=status)
        universities.save()
        return redirect(reverse('universitylist'))
    else:
        return render(request, 'head/headForm/university.html')


def universitylist(request):
    universities = University_Master.objects.all()
        # pagination code
    paginator = Paginator(universities,4)  # for count data on each page
    page_number = request.GET.get('page')
    universities1 = paginator.get_page(page_number)
    totalpage = universities1.paginator.num_pages     # for going direct last page
    data = {
        'universities':universities1,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }
    return render(request, 'head/headList/university_list.html',context=data)

def update_university(request,id):
    record = University_Master.objects.get(id=id)
    if request.method == 'POST':
        university = request.POST.get('university')
        status = request.POST.get('status')
        record.university = university
        record.status = status
        record.save()
        return redirect(reverse('universitylist'))
    else:
        return render(request,'head/update/university_update.html',context={'record':record})

def delete_university(request,id):
    duni = University_Master.objects.get(id=id)
    duni.delete()
    return redirect(reverse('universitylist'))

def universitylist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="university_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['University','status'])

    universities = University_Master.objects.all()
    for uni in universities:
        writer.writerow([uni.university,uni.status])
    return response

def universitylist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['University', 'Status']]
    universities = University_Master.objects.all()
    for uni in universities:
        data.append([uni.university,uni.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="university_data.pdf"'
    response.write(pdf_data)
    return response

# ************* Collage ***************

def college(request):
    active_universities = University_Master.objects.filter(status='Active')
    if request.method == 'POST':
        university = request.POST.get('university')
        collage = request.POST.get('collage')
        status = request.POST.get('status')
        university = University_Master.objects.get(id=university)
        collages = Collage_Master.objects.create(university=university,collage=collage,status=status)
        collages.save()
        return redirect(reverse('collegelist'))
    else:
        universities = University_Master.objects.all()
        return render(request, 'head/headForm/college.html',{'universities':active_universities})
    

def collegelist(request):
    collage = Collage_Master.objects.all()
    # pagination code
    paginator = Paginator(collage,4)  # for count data on each page
    page_number = request.GET.get('page')
    collages = paginator.get_page(page_number)
    totalpage = collages.paginator.num_pages     # for going direct last page
    data = {
        'collage':collages,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }
    return render(request, 'head/headList/college_list.html',context=data)

def collage_update(request,id):
    university_id = University_Master.objects.filter(status='Active')
    record = Collage_Master.objects.get(id=id)
    if request.method == 'POST':
        university_id = request.POST.get('university')
        collage = request.POST.get('collage')
        status = request.POST.get('status')
        record.university_id = university_id
        record.collage = collage
        record.status = status
        record.save()
        return redirect(reverse('collegelist'))
    else:
        return render(request , 'head/update/collage_update.html',context={'record':record , 'university_id':university_id})
    
def delete_collage(request,id):
    dcol = Collage_Master.objects.get(id=id)
    dcol.delete()
    return redirect(reverse('collegelist'))

def collagelist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="collage_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['University','Collage','Status'])

    collages = Collage_Master.objects.all()
    for col in collages:
        writer.writerow([col.university,col.collage,col.status])
    return response

def collagelist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['University','Collage', 'Status']]
    collages = Collage_Master.objects.all()
    for col in collages:
        data.append([col.university,col.collage,col.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="collage_data.pdf"'
    response.write(pdf_data)
    return response

# ***************** Course ****************
def courselist(request):
    course = Course_Master.objects.all()
        # pagination code
    paginator = Paginator(course,4)  # for count data on each page
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    totalpage = courses.paginator.num_pages     # for going direct last page
    data = {
        'course':courses,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }
    return render(request, 'head/headList/course_list.html', context=data)

def course(request):
    active_categories = Category_Master.objects.filter(status='Active')
    active_subcategories = SubCategory_Master.objects.filter(status='Active')
    if request.method == 'POST':
        course = request.POST.get('course')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        duration = request.POST.get('duration')
        fees = request.POST.get('fees')
        status = request.POST.get('status')

        category = Category_Master.objects.get(id=category)
        sub_category = SubCategory_Master.objects.get(id=sub_category)

        course = Course_Master.objects.create(course=course,category=category,sub_category=sub_category,duration=duration,fees=fees,status=status)
        course.save()
        return redirect(reverse('courselist'))
    else:
        categories = Category_Master.objects.all()
        sub_categories = SubCategory_Master.objects.all()
        return render(request, 'head/headForm/course.html',context={'categories':active_categories , 'sub_categories':active_subcategories})

def course_update(request,id):
    category_id = Category_Master.objects.filter(status='Active')
    sub_category_id = SubCategory_Master.objects.filter(status='Active')
    record = Course_Master.objects.get(id=id)
    if request.method == 'POST':
        course = request.POST.get('course')
        category_id = request.POST.get('category')
        sub_category_id = request.POST.get('sub_category')
        duration = request.POST.get('duration')
        fees = request.POST.get('fees')
        status = request.POST.get('status')
        record.course = course
        record.category_id = category_id
        record.sub_category_id = sub_category_id
        record.duration = duration
        record.fees = fees
        record.status = status
        record.save()
        return redirect(reverse('courselist'))
    else:
        return render(request , 'head/update/course_update.html' , context={'record':record , 'category_id':category_id , 'sub_category_id':sub_category_id})

def course_delete(request,id):
    dc = Course_Master.objects.get(id=id)
    dc.delete()
    return redirect(reverse('courselist'))

def courselist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="course_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Course','Category','Sub-Category','Duration','Status'])

    courses = Course_Master.objects.all()
    for col in courses:
        writer.writerow([col.course,col.category,col.sub_category,col.duration,col.status])
    return response

def courselist_to_pdf(request):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    # Create a table for the data
    data = [['Course','Category','Sub-Category','Duration','Status']]
    courses = Course_Master.objects.all()
    for col in courses:
        data.append([col.course,col.category,col.sub_category,col.duration,col.status])
    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # Create table object and apply style
    table = Table(data)
    table.setStyle(style)
    # Add table to PDF document
    pdf.build([table])
    # Get PDF content from buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    # Create HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="course_data.pdf"'
    response.write(pdf_data)
    return response



def head(request):
    return render(request,'head/headDashboard/base.html')

def head_dashboard(request):
    return render(request,'head/headDashboard/dashboard.html')

def create_master(request):
    createLocation = Location_Master.objects.filter(status='active')
    if request.method == 'POST':
        location_id = request.POST.get('location')
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('status')
        location = Location_Master.objects.get(id=location_id)
        profile = UserProfile.objects.create(username=username,password=password,location_id=location,status=status)
        profile.save()
        return redirect('locationlist')
    else:
        location = Location_Master.objects.all()
        return render(request,'head/headForm/head.html', {'location':createLocation})

def head(request):
    return render(request, 'head/headForm/head.html')








# <<<<<<<<<<<<<<< Master View >>>>>>>>>>>>>>>

# *********** Show count number in cards Dashboard ************
def dashboard(request):
    count = Stu_Admit.objects.count()
    paid_students_count = Stu_Admit.objects.filter(balance_fees=0).count()  
    pending_students_count = Stu_Admit.objects.filter(balance_fees__gt=0).count() 
    followup_count = Fee_followup.objects.count()       

    data = {
        'count':count,
        'paid_students_count':paid_students_count,
        'pending_students_count':pending_students_count,
        'followup_count':followup_count
    }
    return render(request,'master/dashboard.html',context=data)

# ************* Student Inquiry ***************

def inquiry(request):
    inquiry = Stu_Inquiry.objects.all()
    # pagination code
    paginator = Paginator(inquiry,4)  # for count data on each page
    page_number = request.GET.get('page')
    inquries = paginator.get_page(page_number)
    totalpage = inquries.paginator.num_pages     # for going direct last page
    data = {
        'inquiry':inquries,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }
    return render(request,'master/masterList/inquiry_list.html',context=data)

def inquiryform(request):
    active_universities = University_Master.objects.filter(status='Active')
    active_collages = Collage_Master.objects.filter(status='Active')
    courses = Course_Master.objects.filter(status='Active')
    if request.method == 'POST':
        name = request.POST.get('name')
        university = request.POST.get('university')
        collage = request.POST.get('collage')
        course = request.POST.get('course')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        home_mobile_no = request.POST.get('home_mobile_no')
        status = request.POST.get('status')

        university = University_Master.objects.get(id=university)
        collage = Collage_Master.objects.get(id=collage)
        course1 = Course_Master.objects.get(id=course)

        inquiry = Stu_Inquiry.objects.create(name=name,university=university,collage=collage,course=course1,email=email,mobile_no=mobile_no,home_mobile_no=home_mobile_no,status=status)

        inquiry.save()

        return redirect(reverse('inquiry'),inquiry_id=inquiry.id)
    else:
        universities = University_Master.objects.all()
        collages = Collage_Master.objects.all()
        course2 = Course_Master.objects.all()
        data = { 
            'universities':active_universities,
            'collages':active_collages,
            'course2':courses
        }
        return render(request,'master/masterForm/inquiry_form.html',context=data)

def inquiry_update(request,id):
    university_id = University_Master.objects.filter(status='Active')
    collage_id = Collage_Master.objects.filter(status='Active')
    course_id = Course_Master.objects.filter(status='Active')
    record = Stu_Inquiry.objects.get(id=id)
     
    if request.method == 'POST':
        name = request.POST.get('name')
        university_id = request.POST.get('university')
        collage_id = request.POST.get('collage')
        course_id = request.POST.get('course')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        home_mobile_no = request.POST.get('home_mobile_no')
        status = request.POST.get('status')

        record.name = name
        record.university_id = university_id
        record.collage_id = collage_id
        record.course_id = course_id
        record.email = email
        record.mobile_no = mobile_no
        record.home_mobile_no = home_mobile_no
        record.status = status

        record.save()
        return redirect(reverse('inquiry'))
    else:
        return render(request,'master/update/inquiry_update.html',context={'record':record,
        'university_id':university_id,'collage_id':collage_id,'course_id':course_id})

def inquiry_delete(request,id):
    i = Stu_Inquiry.objects.get(id=id)
    i.delete()
    return redirect(reverse('inquiry')) 

def inquirylist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="Inquiry_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Course','University','Collage','Email ID','Mobile No','Home Mobile No','Status'])

    inquiry = Stu_Inquiry.objects.all()
    for i in inquiry:
        writer.writerow([i.name,i.course,i.university,i.collage,i.email,i.mobile_no,i.home_mobile_no,i.status])
    return response

# def inquirylist_to_pdf(request):
#     # Create a BytesIO buffer to store PDF
#     buffer = BytesIO()
#     # Create a PDF document
#     pdf = SimpleDocTemplate(buffer, pagesize=letter)
#     # Create a table for the data
#     data = [['Name','Course','University','Collage','Email ID','Mobile No','Home Mobile No','Status']]
#     inquiry = Stu_Inquiry.objects.all()
#     for i in inquiry:
#         data.append([i.name,i.course,i.university,i.collage,i.email,i.mobile_no,i.home_mobile_no,i.status])
#     # Add style to table
#     style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                         ('GRID', (0, 0), (-1, -1), 1, colors.black)])
#     # Create table object and apply style
#     table = Table(data)
#     table.setStyle(style)
#     # Add table to PDF document
#     pdf.build([table])
#     # Get PDF content from buffer
#     pdf_data = buffer.getvalue()
#     buffer.close()
#     # Create HTTP response with PDF content
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="Inquiry_data.pdf"'
#     response.write(pdf_data)
#     return response

def inquirylist_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Inquiry.pdf"'

    # Define the table data
    data = Stu_Inquiry.objects.all()

    data = [['Name','Course','University','Collage','Email ID','Mobile No','Home Mobile No','Status']]
    inquiry = Stu_Inquiry.objects.all()
    for i in inquiry:
        data.append([i.name,i.course,i.university,i.collage,i.email,i.mobile_no,i.home_mobile_no,i.status])

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    table = Table(data)

    # Style the table
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])  # Add borders
    table.setStyle(style)

    # Add the table to the PDF document
    doc.build([table])

    return response



# ************** Student Admit ****************

def admit_list(request):
    admit = Stu_Admit.objects.all()
        # pagination code
    paginator = Paginator(admit,4)  # for count data on each page
    page_number = request.GET.get('page')
    admits = paginator.get_page(page_number)
    totalpage = admits.paginator.num_pages     # for going direct last page
    data = {
        'admit':admits,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }

    return render(request,'master/masterList/admit_list.html',context=data)

def admitstu(request, id):  # main Function
    # Fetching necessary data
    active_course = Course_Master.objects.filter(status='Active')
    # active_course = Course_Master.objects.filter(duration=id).last()
    active_locations = Location_Master.objects.filter(status='Active')
    record = Stu_Inquiry.objects.get(id=id)

    if request.method == 'POST':
        # Getting form data
        stu_name = request.POST.get('stu_name')
        aadhar_no = request.POST.get('aadhar_no')       
        location_id = request.POST.get('location')
        course_id = request.POST.get('course')
        duration = request.POST.get('duration')
        date = request.POST.get('date')
        total_fees = request.POST.get('total_fees')
        paid_now = request.POST.get('paid_now')
        balance_fees = request.POST.get('balance_fees')
        next_followup_date = request.POST.get('next_followup_date')
        system = request.POST.get('system')
        fee_close = request.POST.get('fee_close')

        # Assigning values to Stu_Inquiry record
        record.stu_name = stu_name
        #record.course_id = course_id  # Assuming course_id is the correct field to assign the course ID
        # record.save()

        # Debugging statements
        print("Balance fees:", balance_fees)

        
        # Debugging statement   
        print("Fee close:", fee_close)

        # Creating Stu_Admit object
        admit = Stu_Admit.objects.create(
            stu_name=record,  # Assuming 'name' is a ForeignKey in Stu_Admit pointing to Stu_Inquiry
            aadhar_no=aadhar_no,
            location_id=location_id,  # Assuming location_id is the correct field to assign the location ID
            course_id=course_id,
            duration=duration,
            date=date,
            total_fees=total_fees,
            paid_now=paid_now,
            balance_fees=balance_fees,
            next_followup_date=next_followup_date,
            system=system,
            fee_close=fee_close
        )

        # Update fee_close based on remaining fees
        if admit.total_fees == admit.paid_now:
            fee_close = 'Yes'
        else:
            fee_close = 'No'


        admit.save()

        return redirect(reverse('admitlist'))
    else:
        # Retrieving other necessary data
        inquiry = Stu_Inquiry.objects.all()
        locations = Location_Master.objects.all()
        courses = Course_Master.objects.all()

        data = {
            'inquiry': record,
            'locations': active_locations,
            'courses': active_course,
            'record': record
        }

        return render(request, 'master/masterForm/admit_form.html', context=data)
    

# def get_duration(request):
#     course_id = request.GET.get('course_id')
#     durations = Course_Master.objects.filter(course_id=course_id)
#     data = list(durations.values('id','category'))
#     return JsonResponse(data, safe=False)

def get_duration(request):
    course_id = request.GET.get('course_id')  # Retrieve course ID from request
    if course_id:
        try:
            course = Course_Master.objects.get(pk=course_id)  # Filter queryset by primary key
            duration = course.duration
            fees = course.fees
            return JsonResponse({'duration': duration, 'fees': fees})
        except Course_Master.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
    else:
        return JsonResponse({'error': 'Course ID not provided'}, status=400)
    
def admit_update(request,id):
    active_course = Course_Master.objects.filter(status='Active')
    active_locations = Location_Master.objects.filter(status='Active')
    # record=Stu_Admit.objects.filter(stu_name_id=id)
    record = Stu_Admit.objects.get(id=id)
    inquiry_record = Stu_Inquiry.objects.get(id=id)
    # inquiry_record=record.stu_name
    if request.method == 'POST':
        # stu_name = request.POST.get('stu_name_id')
        aadhar_no = request.POST.get('aadhar_no')       
        location_id = request.POST.get('location')
        course_id = request.POST.get('course')
        duration = request.POST.get('duration')
        date = request.POST.get('date')
        total_fees = request.POST.get('total_fees')
        paid_now = request.POST.get('paid_now')
        balance_fees = request.POST.get('balance_fees')
        next_followup_date = request.POST.get('next_followup_date')
        system = request.POST.get('system')
        fee_close = request.POST.get('fee_close')

        # try:
        #     instance = Stu_Inquiry.objects.get(name=stu_name)
        # except:
        #     # Handle the case where the Stu_Inquiry record doesn't exist
        #     instance = None

        # instance = Stu_Inquiry.objects.get(name=stu_name)       
        # record.stu_name_id= stu_name_id
        record.aadhar_no = aadhar_no
        record.location_id = location_id
        record.course_id = course_id
        record.duration = duration
        record.date = date
        record.total_fees = total_fees
        record.paid_now = paid_now
        record.balance_fees = balance_fees
        record.next_followup_date =next_followup_date
        record.system = system
        record.fee_close = fee_close
        

        record.save()
        return redirect(reverse('admitlist'))
    
    else:
        return render(request,'master/update/admit_update.html',context={'record':record,'inquiry_record':inquiry_record,'active_course':active_course,'active_locations':active_locations})


# def admitstu(request, id):  # main Function
#     # Fetching necessary data
#     #course = Course_Master.objects.filter(status='Active')
#     # active_course = Course_Master.objects.filter(duration=id).last()
#     active_locations = Location_Master.objects.filter(status='Active')
#     active_subcategory = SubCategory_Master.objects.filter(status='Active')
#     record = Stu_Inquiry.objects.get(id=id)

#     if request.method == 'POST':
#         # Getting form data
#         name = request.POST.get('name')
#         aadhar_no = request.POST.get('aadhar_no')       
#         location_id = request.POST.get('location')
#         #course_id = request.POST.get('course')
#         sub_category_id = request.POST.get('sub_category')
#         duration = request.POST.get('duration')
#         date = request.POST.get('date')
#         total_fees = request.POST.get('total_fees')
#         paid_now = request.POST.get('paid_now')
#         balance_fees = request.POST.get('balance_fees')
#         next_followup_date = request.POST.get('next_followup_date')
#         system = request.POST.get('system')
#         fee_close = request.POST.get('fee_close')

#         # Assigning values to Stu_Inquiry record
#         record.name = name
#         #record.course_id = course_id  # Assuming course_id is the correct field to assign the course ID
#         # record.save()

#         # Creating Stu_Admit object
#         admit = Stu_Admit.objects.create(
#             name=record,  # Assuming 'name' is a ForeignKey in Stu_Admit pointing to Stu_Inquiry
#             aadhar_no=aadhar_no,
#             location_id=location_id,  # Assuming location_id is the correct field to assign the location ID
#             course_id=record.course_id,
#             sub_category_id=sub_category_id,
#             duration=duration,
#             date=date,
#             total_fees=total_fees,
#             paid_now=paid_now,
#             balance_fees=balance_fees,
#             next_followup_date=next_followup_date,
#             system=system,
#             fee_close=fee_close
#         )

#         admit.save()

#         return redirect(reverse('admitlist'))
#     else:
#         # Retrieving other necessary data
#         inquiry = Stu_Inquiry.objects.all()
#         locations = Location_Master.objects.all()
#         courses = Course_Master.objects.all()
#         sub_categorise = SubCategory_Master.objects.all()

#         data = {
#             'inquiry': record,
#             'locations': active_locations,
#             'courses': courses,
#             'sub_categorise': active_subcategory,
#             'record': record
#         }

#         return render(request, 'master/masterForm/admit_form.html', context=data)

def admit_delete(request,id):
    i = Stu_Admit.objects.get(id=id)
    i.delete()
    return redirect(reverse('admitlist'))

def admitlist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="Admission_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Location','Course','Sub-Category','Duration','Date','Aadhar No.','System','Total Fees','Fees paid Now','Balance Fees','Fee Close','Fees Follow-up Date'])

    admit = Stu_Admit.objects.all()
    for a in admit:
        writer.writerow([a.stu_name,a.location,a.course,a.duration,a.date,a.aadhar_no,a.system,a.total_fees,a.paid_now,a.balance_fees,a.fee_close,a.next_followup_date])
    return response

# def admitlist_to_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="Admission.pdf"'

#     # Define the table data
#     data = Stu_Admit.objects.all()

#     data = [['Name','Location','Course','Sub-Category','Duration','Date','Aadhar No.','System','Total Fees','Fees paid Now','Balance Fees','Fee Close','Fees Follow-up Date']]
#     admit = Stu_Admit.objects.all()
#     for a in admit:
#         data.append([a.name,a.location,a.course,a.sub_category,a.duration,a.date,a.aadhar_no,a.system,a.total_fees,a.paid_now,a.balance_fees,a.fee_close,a.next_followup_date])

#     # Create a PDF document
#     doc = SimpleDocTemplate(response, pagesize=landscape(letter))
#     table = Table(data)

#     # Style the table
#     style = TableStyle([('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])  # Add borders
#     table.setStyle(style)

#     col_widths = [doc.width / len(data[0])] * len(data[0])
#     table._argW = col_widths

#     # Allow table to split across pages
    
#     table.splitByRow = 1
#     table.repeatRows = 1 
#     # Add the table to the PDF document
#     doc.build([table])

#     return response
# Enter
def admitlist_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Admission.pdf"'

    # Retrieve data from the database
    admit_list = Stu_Admit.objects.all()

    # Define the table data
    data = [['Name','Location','Course','Duration','Date','Aadhar No.','System','Total Fees','Fees paid Now','Balance Fees','Fee Close','Fees Follow-up Date']]

    # Populate the data list with database records
    for admit in admit_list:
        data.append([admit.stu_name, admit.location, admit.course, admit.duration, admit.date, admit.aadhar_no, admit.system, admit.total_fees, admit.paid_now, admit.balance_fees, admit.fee_close, admit.next_followup_date])

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    table = Table(data)

    # Style the table
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])  # Add borders
    table.setStyle(style) 

    # Adjust column widths
    col_widths = [doc.width / len(data[0])] * len(data[0])
    table._argW = col_widths

    # Allow table to split across pages
    table.splitByRow = 1
    table.repeatRows = 1

    # Add the table to the PDF document
    doc.build([table])

    return response

# ******************** Fees Followup Update *********************

def followup_list(request):
    data = Fee_followup.objects.all()
            # pagination code
    paginator = Paginator(data,4)  # for count data on each page
    page_number = request.GET.get('page')
    data1 = paginator.get_page(page_number)
    totalpage = data1.paginator.num_pages     # for going direct last page
    context = {
        'data':data1,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }

    return render(request,'master/masterList/followUp_list.html',context=context)

def followupdate(request):
    admit_record = Stu_Admit.objects.filter(fee_close = 'No')
    
    if request.method == 'POST':
        today_date = request.POST.get('today_date')
        student_name = request.POST.get('student_name')
        course = request.POST.get('course')
        fees_paid = request.POST.get('fees_paid')
        balance_till = request.POST.get('balance_till')
        now_paid = request.POST.get('now_paid')
        total_balance_pending = request.POST.get('total_balance_pending')
        next_follow_up_date = request.POST.get('next_follow_up_date')

        try:
            instance = Stu_Admit.objects.get(id=student_name)
        except Stu_Admit.DoesNotExist:
            # Handle the case where the query does not find a matching record
            print("No Stu_Admit record found with stu_name:", student_name)
        else:
            follow_up = Fee_followup.objects.create(
            today_date=today_date,
            student_name=instance,
            course=course,
            fees_paid=fees_paid,
            balance_till=balance_till,
            now_paid=now_paid,
            total_balance_pending=total_balance_pending,
            next_follow_up_date=next_follow_up_date
        )

            follow_up.save()
        return redirect(reverse('followuplist'))

    
    else:
        admit = Stu_Admit.objects.all()
        return render(request,'master/masterForm/FollowUpDate.html',context={'admit':admit_record})

# def get_student_details(request):
#     # if request.method == "GET" and request.is_ajax():
#         student_name_id = request.GET.get('id')
#         if student_name_id:
#             try:
#                 student = Stu_Admit.objects.get(id=student_name_id)
#                 data = {
#                     "course": student.course,  # Assuming 'course_name' is a field in Stu_Admit model
#                     "fees_paid": student.paid_now,
#                     "balance_fees": student.balance_fees,
#                 }
#                 return JsonResponse(data)
#             except Stu_Admit.DoesNotExist:
#                 return JsonResponse({"error": "Student not found"}, status=404)
#         return JsonResponse({}, status=400)

def get_student_details(request):
    student_name_id = request.GET.get('student_name_id')  # Retrieve course ID from request
    if student_name_id:
        try:
            data = Stu_Admit.objects.get(pk=student_name_id)  # Filter queryset by primary key
            course_id = data.course.course
            paid_now = data.paid_now
            balance_fees = data.balance_fees
            return JsonResponse({'course_id':course_id,'paid_now': paid_now, 'balance_fees': balance_fees})
        except Stu_Admit.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    else:
        return JsonResponse({'error': 'Student ID not provided'}, status=400)
    


def followuplist_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="Fee_Followup_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Student Name', 'Course', 'Fee Paid', 'Balance Till', 'Now Paid', 'Total Pending Balance', 'Next Followup Date'])

    followup = Fee_followup.objects.all()
    for f in followup:
        # Accessing related fields' attributes if necessary
        student_name = f.student_name.stu_name  # Assuming 'name' is the attribute you want to access
        course = f.course  # Assuming 'name' is the attribute you want to access
        
        # Convert date field to string if necessary
        today_date = str(f.today_date)  # Assuming 'today_date' is a DateField

        writer.writerow([today_date, student_name, course, f.fees_paid, f.balance_till, f.now_paid, f.total_balance_pending, f.next_follow_up_date])
    return response

def followuplist_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Fee_Followup_data.pdf"'

    # Retrieve data from the database
    followup = Fee_followup.objects.all()

    # Define the table data
    data = [['Date','Student Name','Course','Fee Paid','Balance Till','Now Paid','Total Pending Balance','Next Followup Date']]

    # Populate the data list with database records
    for f in followup:
# Accessing related fields' attributes if necessary
        student_name = f.student_name.stu_name  # Assuming 'name' is the attribute you want to access
        course = f.course  # Assuming 'name' is the attribute you want to access

        # Convert date field to string if necessary
        today_date = str(f.today_date)  # Assuming 'today_date' is a DateField

        # Append data to the list
        data.append([today_date, student_name, course, f.fees_paid, f.balance_till, f.now_paid, f.total_balance_pending, f.next_follow_up_date])
    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    table = Table(data)

    # Style the table
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])  # Add borders
    table.setStyle(style) 

    # Adjust column widths
    col_widths = [doc.width / len(data[0])] * len(data[0])
    table._argW = col_widths

    # Allow table to split across pages
    table.splitByRow = 1
    table.repeatRows = 1

    # Add the table to the PDF document
    doc.build([table])

    return response

# ************* CourseWise Report **************

def coursewise(request):
    admit = Stu_Admit.objects.all().order_by('course__course')
                # pagination code
    paginator = Paginator(admit,7)  # for count data on each page
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    totalpage = data.paginator.num_pages     # for going direct last page
    context = {
        'admit':data,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }   

    return render(request,'master/masterList/coursewise_report.html',context=context)

def balance_status(request):
    balance_status = request.GET.get('balance_status','all')  #'complete', or 'pending'
    
    if balance_status == 'complete':
        admits = Stu_Admit.objects.filter(balance_fees=0).order_by('course__course')
    elif balance_status == 'pending':
        admits = Stu_Admit.objects.exclude(balance_fees=0).order_by('course__course')
    else:
        admits = Stu_Admit.objects.all().order_by('course__course')
    
    data = {
        'admits': admits,  # Corrected variable name
        'balance_status': balance_status,
    }
    return render(request, 'master/masterList/coursewise_report.html', data)

def course_wise_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="Course Wise Data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Course', 'Balance Fees'])

    report = Stu_Admit.objects.all().order_by('course__course')
    for a in report:
        writer.writerow([a.stu_name,a.course,a.balance_fees])
    return response

def course_wise_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Course Wise Data.pdf"'

    # Define the table data
    data = Stu_Inquiry.objects.all().order_by('course__course')

    data = [['Name', 'Course', 'Balance Fees']]
    report = Stu_Admit.objects.all()
    for r in report:
        data.append([r.stu_name,r.course,r.balance_fees])

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    table = Table(data)

    # Style the table
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])  # Add borders
    table.setStyle(style)

    # Add the table to the PDF document
    doc.build([table])

    return response


# *************** Amount-Wise Report ***************

def amountwise(request):
    admit = Stu_Admit.objects.filter(balance_fees__gt=0).order_by('-balance_fees')
                    # pagination code
    paginator = Paginator(admit,5)  # for count data on each page
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    totalpage = data.paginator.num_pages     # for going direct last page
    context = {
        'admit':data,
        # 'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }   

    return render(request,'master/masterList/amountwise_report.html',context=context)

def amount_wise_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="Amount Wise Data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Course', 'Balance Fees'])

    report = Stu_Admit.objects.all().order_by('-balance_fees')
    for a in report:
        writer.writerow([a.stu_name,a.course,a.balance_fees])
    return response

def amount_wise_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Amount Wise Data.pdf"'

    # Define the table data
    # data = Stu_Admit.objects.all()

    data = [['Name', 'Course', 'Balance Fees']]
    report = Stu_Admit.objects.all().order_by('-balance_fees')
    for r in report:
        data.append([r.stu_name,r.course,r.balance_fees])

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    table = Table(data)

    # Style the table
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])  # Add borders
    table.setStyle(style)

    # Add the table to the PDF document
    doc.build([table])

    return response


def records(request):
    return render(request,'templates/master/masterList/records.html')




