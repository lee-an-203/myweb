import os
os.getcwd()
# '/Users/tuandung/python2204/django_web/myweb'
# CURD: Create, Update, Read, Delete
# C: Create bằng lệnh
student1 = Student(name="Ronaldo", age=37, gender=True, email="ronaldo@gmailc.om", phone="0123456789", address="Anh")
student1.save()

# Lưu ý: khi tạo object từ class như trên, thì phải thêm một lệnh nữa để thêm record vào table <obj>.save()

Student.objects.all() # Tương đương với SELECT * FROM Student;
# <QuerySet [<Student: Student object (1)>]>
# Lưu ý: 'objects' phải có 's'

student2 = Student.objects.create(name="Messi", age=34, gender=True, email="messi@gmail.com", phone="01234", address="Pháp")
# READ bằng lệnh
students = Student.objects.all()
for student in students:
    print(student.name)

# Lưu ý: tên biến nên có liên quan với tên class:)) viết thường dạng số nhiều
# Lấy số nhiều, tên biến tiếng anh dạn số nhiều. Khi dùng qua vòng lặp thì sẽ là số ít.
# Các bạn sẽ biết chính xác tên class

# Read detail 1 Student
# SELECT * FROM Student WHERE id=1;
student = Student.objects.get(id=1)
student.__dict__
#{'_state': <django.db.models.base.ModelState object at 0x000002C1D5939960>, 'id': 1, 'name': 'Ronaldo', 'age': 37, 'gender': True, 'email': 'ronaldo@gmailcom', 'phone': '0123456789', 'address': 'Anh'}
student = Student.objects.get(id=1) # .get là trả về duy nhất 1 object
student
#<Student: Ronaldo>
student = Student.objects.filter(id=1)
student
#<QuerySet [<Student: Ronaldo>]>
student = Student.objects.filter(id=1) # .filter thì trả về 1 danh sách

student = Student.objects.filter(pk = 1) # id=pk

#startswith
students = Student.objects.filter(name__startswith = "M") #Bắt đầu bằng chữ M

#endswith
students = Student.objects.filter(name__endswith = "M") #Bắt đầu bằng chữ M

# UPDATE
Student.objects.get(pk=1)
# <Student: Ronaldo>
student.__dict__
# {'_state': <django.db.models.base.ModelState object at 0x000002C1D593BDF0>, 'id': 3, 'name': 'Mbape', 'age': 21, 'gender': True, 'email': 'mbape@gmailcom', 'phone': '0123456', 'address': 'Pháp'}
ronaldo = Student.objects.get(name="Ronaldo")
ronaldo.name = "Cristiano Ronaldo"
ronaldo.save()

# DELETE
Student.objects.get(pk=3).delete()

# Quan hệ nhiều-1:
from myapp.models import Reporter, Article
reporter1 = Reporter.objects.create(first_name="Ronaldo", last_name="Critiano",email="ronaldo@gmail.com")
reporter2 = Reporter.objects.create(first_name="Messi", last_name="Leoniel",email="messi@gmail.com")
reporter1
# <Reporter: Ronaldo Critiano>
from django.utils.timezone import now
ar1 = Article(headline="Headline1", pub_date=now(), reporter=reporter1)
ar1.save()
ar2 = Article(headline="Headline2", pub_date=now(), reporter=reporter1)
ar2.save()
reporter1
# <Reporter: Ronaldo Critiano>
reporter1.article_set.create(headline="Headline3", pub_date=now())
# <Article: Headline3>
# reporter1.article_set.all() tương đương với Article.objects.filter(reporter=reporter1) # = SELECT * FROM Article WHERE Report.id = Article
for item in reporter1.article_set.all():
    print(item.headline, item.pub_date)

# Headline1 2022-07-24
# Headline2 2022-07-24
# Headline3 2022-07-24

# Quan hệ nhiều nhiều:
from myapp.models import Publication, Article
p1 = Publication(title="title1")
p1.save()
p2 = Publication.objects.create(title="title2")
Publication.objects.all()
# <QuerySet [<Publication: title1>, <Publication: title2>]>
p3 = Publication.objects.create(title="title3")
a1 = Article.objects.create(headline="headline1")
a2 = Article.objects.create(headline="headline2")
Article.objects.all()
# <QuerySet [<Article: headline1>, <Article: headline2>]>
a1.publications
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x105a0f880>
a1.publications.add(p1,p2)
p1.article_set.add(a2,a1)
a1.publications.add(p1,p2,p3)
p1.article_set.all()
# <QuerySet [<Article: headline1>, <Article: headline2>]>
a1.publications.all()
# <QuerySet [<Publication: title1>, <Publication: title2>, <Publication: title3>]>
