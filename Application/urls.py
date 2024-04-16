from django.urls import path
from Application import views
# app_name='Application'
urlpatterns = [

    # <<<<<<<<<< login urls >>>>>>>>>>>
    path('',views.image,name='login'),
    # path('image/',views.image,name='image'),
    path('hlogin/',views.admin_login,name='headlogin'),
    path('mlogin/',views.master_login,name='masterlogin'),
    path('logout/',views.admin_logout,name='logout'),
    # path('headlogin/',views.admin_login,name='adminlogin'),

    # <<<<<<<<<<<< master urls >>>>>>>>>>>>>
    path('Master_dash/',views.dashboard,name='dashboard'),

    # list and form urls
    path('records/',views.records,name='records'),

    # ************** Student Inquiry ****************
    path('inquiry/',views.inquiry,name='inquiry'),
    path('inquiryform/',views.inquiryform,name='inquiryform'),
    path('inquiry_update/<int:id>/',views.inquiry_update,name='inquiry_update'),
    path('inquiry_delete/<int:id>/',views.inquiry_delete,name='inquiry_delete'),
    path('inquiryList_csv/',views.inquirylist_to_csv,name='inquiryList_csv'),
    path('inquiryList_pdf/',views.inquirylist_to_pdf,name='inquiryList_pdf'),

    # **************** Student Admit ****************
    path('admit/<int:id>',views.admitstu,name='admit1'),
    path('admitlist/',views.admit_list,name='admitlist'),
    # path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get-durations/', views.get_duration, name='get_durations'),
    path('admit_update/<int:id>/',views.admit_update,name='admit_update'),
    path('delete_admit/<int:id>/',views.admit_delete,name='delete_admit'),
    path('admitlist_to_csv/',views.admitlist_to_csv,name='admitlist_to_csv'),
    path('admitlist_to_pdf/',views.admitlist_to_pdf,name='admitlist_to_pdf'),

    # *************** Follow-up Date *****************
    path('followup/',views.followupdate,name='followup'),
    path('follouplist/',views.followup_list,name='followuplist'),
    path('get-student-details/',views.get_student_details,name='get-student-details'),
    path('Fee_FollowupList_to_csv/',views.followup_list,name='feeFollowupCSV'),
    path('Fee_followupList_to_pdf/',views.followuplist_to_pdf,name='Fee_followupList_to_pdf'),

    # *************** CourseWise Report ******************
    path('coursewise/',views.coursewise,name='coursewise'),
    path('balance_status/',views.balance_status,name='Status'),
    path('course_report_to_csv/',views.course_wise_to_csv,name='course_report_to_csv'),
    path('course_report_to_pdf/',views.course_wise_to_pdf,name='course_report_to_pdf'),

    # *************** AmountWise Report **************
    path('amountwise/',views.amountwise,name='amountwise'),
    path('amount_report_to_csv/',views.amount_wise_to_csv,name='amount_report_to_csv'),
    path('amount_report_to_pdf/',views.amount_wise_to_pdf,name='amount_report_to_pdf'),

    

    # <<<<<<<<<<<< head urls >>>>>>>>>>>
    path('head/',views.head_dashboard,name='head_dashboard'),

    path('create_master/',views.create_master,name='create_master'),

    path('head/', views.head, name='head'),

    # ****** city *****
    path('citylist/',views.citylist,name='citylist'),
    path('city/', views.city, name='city'),
    path('delete_city/<int:id>/', views.delete_city, name = "delete_city"),
    path('update_city/<int:id>/', views.update_city, name='update_city'),
    path('export_csv/',views.citylist_to_csv,name='export_csv'),
    path('export_pdf/',views.citylist_to_pdf,name='export_pdf'),
    path('search_city/',views.search_city,name='search_city'),

    # ******** Location *********
    path('location/', views.location, name='location'),
    path('location_list/', views.locationlist, name='locationlist'),
    path('delete_location/<int:id>/',views.delete_location,name='delete_location'),
    path('update_location/<int:id>/',views.update_location,name='update_location'),
    path('Lexport_csv/',views.locationlist_to_csv,name='Lexport_csv'),
    path('Lexport_pdf/',views.locationlist_to_pdf,name='Lexport_pdf'),

    # ********** Categoty ***********
    path('category/', views.category, name='category'),
    path('category_list/', views.categorylist, name='categorylist'),
    path('update_category/<int:id>/',views.update_category,name='update_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('cateExport_csv/',views.categorylist_to_csv,name='cateExport_csv'),
    path('cateExport_pdf/',views.categorylist_to_pdf,name='cateExport_pdf'),

    # *********** Sub-Category *************
    path('sub-category/', views.sub_category, name='subcategory'),
    path('sub_category_list/', views.subcategorylist, name='subcategorylist'),
    path('update_subcategory/<int:id>/',views.update_subcategory,name='update_subcategory'),
    path('delete_subcategory/<int:id>/',views.delete_subcategory,name='delete_subcategory'),
    path('subcatExport_csv/',views.subcategorylist_to_csv,name='subcatExport_csv'),
    path('subcatExport_pdf/',views.subcategorylist_to_pdf,name='subcatExport_pdf'),

    # *********** University **************
    path('university/', views.university, name='university'),
    path('university_list/', views.universitylist, name='universitylist'),
    path('update_university/<int:id>/',views.update_university,name='update_university'),
    path('delete_university/<int:id>/',views.delete_university,name='delete_university'),
    path('universityExport_csv/',views.universitylist_to_csv,name='universityExport_csv'),
    path('universityExport_pdf/',views.universitylist_to_pdf,name='universityExport_pdf'),

    # ************ Collage *************
    path('college/', views.college, name='college'),
    path('college_list/', views.collegelist, name='collegelist'),
    path('update_collage/<int:id>/',views.collage_update,name='update_collage'),
    path('delete_collage/<int:id>/',views.delete_collage,name='delete_collage'),
    path('collageExport_csv/',views.collagelist_to_csv,name='collageExport_csv'),
    path('collageExport_pdf/',views.collagelist_to_pdf,name='collageExport_pdf'),

    # *************** Course **************
    path('course/', views.course, name='course'),
    path('course_list/', views.courselist, name='courselist'),
    path('update_course/<int:id>/',views.course_update,name='update_course'),
    path('delete_course/<int:id>/',views.course_delete,name='delete_course'),
    path('courseExport_csv/',views.courselist_to_csv,name='courseExport_csv'),
    path('courseExport_pdf/',views.courselist_to_pdf,name='courseExport_pdf'),
    
]
