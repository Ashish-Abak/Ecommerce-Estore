from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import product,cart,order
from django.db.models import Q
import random
from datetime import datetime,time
import razorpay
from django.core.mail import send_mail
from django.http import StreamingHttpResponse

# Create your views here.
def home(request):
   # userid=request.user.id
    t=datetime.now().time()
    h=time(12, 0)
    context={}
    p=product.objects.filter(is_active=True)
    if t<h:
        context['products']=p
        context['GM']="Good Morning! Ashish"
        return render(request,'index.html',context)
    elif h<=t<time(18,0):
        context['products']=p
        context['GA']="Good Afternoon! Ashish"
        return render(request,'index.html',context)
    else:
        context['products']=p
        context['GE']="Good Evening! Ashish"
        return render(request,'index.html',context)
    # print(p)
    # print(p[0])
    # print(p[0].name)
    # print(p[0].price)
    #context['products']=p
    #return render(request,'index.html',context)
    
def all(request):
    context={}
    p=product.objects.all()
    context['products']=p
    return render(request,'index.html',context)
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def login_user(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid username and password"
                return render(request,'login.html',context)
    return render(request,'login.html')
def logout_user(request):
    logout(request)
    return redirect('/home')
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def pd(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_detail.html',context)
def addtocart(request,pid):
    if request.user.is_authenticated:
        # print("user is logged")
        # return HttpResponse("user logged in")
        u=User.objects.filter(id=request.user.id)
        p=product.objects.filter(id=pid)
        if u.exists() and p.exists():
            q1=Q(uid=u[0])
            q2=Q(pid=p[0])
            c=cart.objects.filter(q1&q2)
            n=len(c)
            context={}
            context['products']=p

            if n==1:
                context['msg']="Product already exist"
            else:
                c=cart.objects.create(uid=u[0],pid=p[0])
                c.save()
                context['success']="Product added successfully"
                return render(request,'product_detail.html',context)
        else:
            context = {'error': "User or product not found"}
        return render(request, '/login', context)
    else:
        return redirect('/login')
def Cart(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    #print(c)
    n=len(c)
    s=0
    for x in c:
        s=s+x.pid.price*x.qty
    context={}
    context['total']=s
    context['np']=n
    context['products']=c
    return render(request,'cart.html',context)
def placeorder(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    #print("oid=",oid)
    for x in c:
        #print(x)
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=order.objects.filter(uid=request.user.id)
    s=0
    n=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['np']=n
    return render(request,'place_order.html',context)
def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_oTkfAYQEfktFwW", "6Skss2O3zauBrlz0MxZKGlyX"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    #print(payment)
    context={'data':payment}
    return render(request,'pay.html',context)
def sendmail(request):
    uemail=request.user.email
    userid=request.user.id
    c=order.objects.filter(uid=userid)
    o="Your order details: \n"
    for x in c:
        o+=x.pid.name+"\n"
        o+=str(x.pid.price)+"\n"
    send_mail(
    "Order placed succesfully",
    o,
    "ashishabak4@gmail.com",
    [uemail],
    fail_silently=False,)
    return redirect('/placeorder')
def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/Cart')
def removes(request,oid):   
    o=order.objects.filter(id=oid)
    o.delete()
    return redirect('/placeorder')
def updateqty(request,qv,cid):
    c=cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/Cart')

def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html'
                  )
def registration(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'registration.html',context)
        elif upass!=ucpass:
            context['errmsg']="password and confirm password nor same"
            return render(request,'registration.html',context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully"
                return render(request,'registration.html',context)
            except Exception:
                context['errmsg']="user with same username already exist"
                return render(request,'registration.html',context)
            return HttpResponse("User created successfully")
    else:
        return render(request,'registration.html')
    return render(request,'registration.html')
