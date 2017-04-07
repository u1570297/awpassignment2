from django.http import HttpResponse
from django.conf import settings
from django.template import Template, Context
from django.shortcuts import render
import sqlite3
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage


#create database tables
def db(request):
	#with connection.cursor() as cursor:
	#	cursor.execute("CREATE TABLE admin ( admin_name , admin_password )")
	#	cursor.execute("CREATE TABLE category ( cat_id INTEGER PRIMARY  KEY, cat_name VARCHAR(255) )")
	#	cursor.execute("CREATE TABLE post ( p_id INTEGER PRIMARY  KEY, p_name VARCHAR(255), p_desc TEXT, p_image VARCHAR(255), p_catid INTEGER )")
	#	cursor.execute("CREATE TABLE comment ( c_id INTEGER PRIMARY  KEY, c_name VARCHAR(255), c_desc TEXT, c_email VARCHAR(100), c_pid INTEGER, c_status INTEGER )")
	#	cursor.execute("DROP TABLE comment")
	#	cursor.execute("INSERT INTO admin(admin_name, admin_password) values ('admin@gmail.com', '123456')")
 	return HttpResponse('post comment has been created')

#******	login ********
@csrf_exempt
def login(request):
	if request.method == 'POST':
		admin_name 	=	request.POST['admin_name']
		password 	=	request.POST['password']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("SELECT * FROM admin WHERE admin_name = '"+admin_name+"' AND admin_password = '"+password+"'")
			sql 	=	sql.fetchone()

			# if user authenticated
			if(sql):
				request.session['name'] 		= admin_name
   				return HttpResponseRedirect("/add_category/")

   			#if user does not authenticated
			else:
				return HttpResponseRedirect("/login/")

	fp 		= 	open("stylesgap/templates/login.html")
	t 		= 	Template(fp.read())
	fp.close()
	html	= 	t.render(Context())
	return HttpResponse(html)

#****** logout *******
def logout(request):
	del request.session['name']
	return HttpResponseRedirect('/dashboard/')

#******* add category *******
@csrf_exempt
def add_category(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	# when submit button clicked
	if request.method == 'POST':
		cat_name 	=	request.POST['cat_name']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("INSERT INTO category (cat_name) VALUES ('"+cat_name+"')")

	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())
	#***** include add_category page template *****
	tem 	= 	open("stylesgap/templates/add_category.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html
	return HttpResponse(html)

#******* view category *******
def view_category(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include view_category page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	tem 	= 	open("stylesgap/templates/view_category.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* delete category *******
def delete_category(request, id):
	with connection.cursor() as cursor:
		cursor.execute("DELETE FROM category WHERE cat_id = '"+id+"'")
		return HttpResponseRedirect('/view_category/')

#******* edit category *******
@csrf_exempt
def edit_category(request, id):

	# when submit button clicked
	if request.method == 'POST':
		cat_name 	=	request.POST['cat_name']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("UPDATE category SET cat_name = '"+cat_name+"' WHERE cat_id = '"+id+"'")
			return HttpResponseRedirect('/view_category/')

	with connection.cursor() as cursor:
		rec =	cursor.execute("SELECT * FROM category WHERE cat_id = '"+id+"'")
		rec = 	rec.fetchone()
	
	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include edit_category page template *****
	tem 	= 	open("stylesgap/templates/edit_category.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': rec,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* add post *******
@csrf_exempt
def add_post(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	# when submit button clicked
	if request.method == 'POST':
		p_name 		=	request.POST['p_name']
		p_desc 		=	request.POST['p_desc']
		p_catid 	=	request.POST['p_catid']
		filename 	=	''
		if len(request.FILES):
			myfile 	= 	request.FILES['myfile']
			if len(request.FILES) :
				fs 		= 	FileSystemStorage()
				filename= 	fs.save(myfile.name, myfile)
				uploaded_file_url 	= 	fs.url(filename)
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("INSERT INTO post (p_name, p_desc, p_image, p_catid) VALUES ('"+p_name+"', '"+p_desc+"', '"+filename+"', '"+p_catid+"')")		

	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include add_post page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	tem 	= 	open("stylesgap/templates/add_post.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* view post *******
def view_post(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include view_post page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT p.*, c.cat_name FROM post p, category c WHERE c.cat_id = p.p_catid"):
			result.append(x)
	tem 	= 	open("stylesgap/templates/view_post.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* delete post *******
def delete_post(request, id):
	with connection.cursor() as cursor:
		cursor.execute("DELETE FROM post WHERE p_id = '"+id+"'")
		return HttpResponseRedirect('/view_post/')

#******* edit post *******
@csrf_exempt
def edit_post(request, id):

	with connection.cursor() as cursor:
		rec =	cursor.execute("SELECT * FROM post WHERE p_id = '"+id+"'")
		rec = 	rec.fetchone()
		result 	=	[]
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)	

	# when submit button clicked
	if request.method == 'POST':
		p_name 		=	request.POST['p_name']
		p_desc 		=	request.POST['p_desc']
		p_catid 	=	request.POST['p_catid']
		filename	=	rec[3]
		if len(request.FILES):
			myfile 	= 	request.FILES['myfile']
			if len(request.FILES) :
				fs 		= 	FileSystemStorage()
				filename= 	fs.save(myfile.name, myfile)
				uploaded_file_url 	= 	fs.url(filename)
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("UPDATE post SET p_name = '"+p_name+"' , p_desc = '"+p_desc+"', p_image = '"+filename+"', p_catid ='"+p_catid+"' WHERE p_id = '"+id+"'")		
			return HttpResponseRedirect('/view_post/')

	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include edit_post page template *****
	tem 	= 	open("stylesgap/templates/edit_post.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': rec, 'category': result, }))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* view comments *******
def view_comment(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	#***** include header *****
	header	= 	open("stylesgap/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include view_comment page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM comment"):
			result.append(x)
	tem 	= 	open("stylesgap/templates/view_comment.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#**** index *****
def index(request):

	#***** include header *****
	result	=	[]
	result	=	[]
	post 	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("stylesgap/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result,}))

	#***** include index page template *****
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
		for p in cursor.execute("SELECT * FROM post ORDER BY p_id DESC  LIMIT 5"):
			post.append(p)
	tem 	= 	open("stylesgap/templates/index.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result, 'post': post, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("stylesgap/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** blog *****
def blog(request):

	#***** include header *****
	result	=	[]
	post 	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("stylesgap/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result,}))

	#***** include blog page template *****
	with connection.cursor() as cursor:
		for p in cursor.execute("SELECT * FROM post"):
			post.append(p)
	tem 	= 	open("stylesgap/templates/blog.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result, 'post': post, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("stylesgap/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** contact *****
def contact(request):

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("stylesgap/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result,}))

	#***** include contact page template *****
	tem 	= 	open("stylesgap/templates/contact.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("stylesgap/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** blog detail *****
@csrf_exempt
def blogdetail(request, id):

	if request.method == 'POST':
		c_name 		=	request.POST['c_name']
		c_desc 		=	request.POST['c_comment']
		c_email 	=	request.POST['c_email']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("INSERT INTO comment(c_name, c_email, c_desc, c_pid) VALUES ('"+c_name+"', '"+c_email+"', '"+c_desc+"', '"+id+"') ")		

	#***** include header *****
	result	=	[]
	recent 	= 	[]
	comment = 	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("stylesgap/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result,}))

	#***** include blogdetail page template *****
	with connection.cursor() as cursor:
		rec =	cursor.execute("SELECT * FROM post WHERE p_id = '"+id+"'")
		rec = 	rec.fetchone()
		for x in cursor.execute("SELECT * FROM post ORDER BY p_id DESC LIMIT 5"):
			recent.append(x)
		for c in cursor.execute("SELECT * FROM comment WHERE c_pid = '"+id+"'"):
			comment.append(c)
	tem 	= 	open("stylesgap/templates/blogdetail.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'detail': rec, 'recent': recent, 'comment': comment, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("stylesgap/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** post against category *****
def catpost(request, id):

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("stylesgap/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result,}))

	#***** include blog with category filter page template *****
	post 	=	[]
	with connection.cursor() as cursor:
		for p in cursor.execute("SELECT * FROM post WHERE p_catid = '"+id+"'"):
			post.append(p)
	tem 	= 	open("stylesgap/templates/blog.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'post': post, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("stylesgap/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)
