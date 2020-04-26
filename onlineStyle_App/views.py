from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from onlineStyle_App.Loginform import LoginForm
from onlineStyle_App.registrForm import RegistrForm
from onlineStyle_App.addItemForm  import addItemForm
from onlineStyle_App.EditFreeShippingForm  import EditFreeShippingForm
from onlineStyle_App.EditSaleForm import EditSaleForm 
from django.shortcuts import redirect
from .models import Person
from .models import Product
from .models import Cart
from .models import ProductINSale
from .models import Sale
from .models import Order
from .models import wishList
from .models import Category
import pymongo
# import scipy.misc
# import matplotlib.pyplot as plt

from django.contrib import messages
from django.contrib.auth import authenticate
import onlineStyle_App.context_processors as cp
from django.apps import apps #static file

#------------------------------------Send Gmail Email --------------------------
from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail as sm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from _datetime import timedelta, timezone
import datetime

#----------------------------------------------MongoDB-------------------------------------------------
#-------------------------------------insert all the user in mySQL to MongoDB--------------------------
# def insert():
#          mycol = connection_MongoDB_Person()
#          users = Person.objects.all()
#          for user in users:
#               email = user.email
#               fullname = user.fullname
#               address = user.address
#               mobileno = user.mobileno
#               password=user.password
#               role=user.role
#               mydict = { "email":email, "fullname": fullname, "address" : address  , "password": password , "role":role }       
#               x = mycol.insert_one(mydict)

#-------------------------------------Connection MongoDB--------------------
def connection_MongoDB_Person():
     #client = pymongo.MongoClient("mongodb+srv://maha_gazalen:mg2051997@cluster0-qbr0s.mongodb.net/test?retryWrites=true&w=majority")
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     mydb = client["onlineStyle-MongoDB-DataBase"]   
     mycol = mydb["Person"]
     return mycol

def connection_MongoDB_Product():
     #client = pymongo.MongoClient("mongodb+srv://maha_gazalen:mg2051997@cluster0-qbr0s.mongodb.net/test?retryWrites=true&w=majority")
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     mydb = client["onlineStyle-MongoDB-DataBase"]   
     mycol = mydb["Product"]
     return mycol

#-------------------------------------Search User From MongoDB--------------------
def isExisting_User(username):
     mycol = connection_MongoDB_Person()
     myUser = {"email" : username}
     mydoc = mycol.find(myUser)

     for user in mydoc:
        return user

     return {}

def insertAllProduct():
     mycol = connection_MongoDB_Product()
     products = Product.objects.all()
     for product in products:
          title = product.title
          description = product.description
          price = product.price
          qty_small = product.qty_small
          qty_medium =product.qty_medium 
          qty_large = product.qty_large
          qty_xtraLarge = product.qty_xtraLarge
          mydict = { "title" : title , "description" : description , "price": price ,"qty_small":qty_small , "qty_medium":qty_medium , "qty_large":qty_large,"qty_xtraLarge":qty_xtraLarge}
          x = mycol.insert_one(mydict)
          

     
#------------------------------------------------------------------------------
def send_email(email,orderid):
        subject = 'Thank you for choosing OnlineStyle to see youre order please click the following link '
        text_content = 'Thank you .'
        html_content ='<a href="http://127.0.0.1:8000/emailOrder/">Click here </a>'
        from_email = settings.EMAIL_HOST_USER
        to=email
        msg = EmailMultiAlternatives(subject ,text_content,from_email,[to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

#--------------------------------------------STATIC METHODS ---------------------------------------------
#-----------return the price after the sale - list_id = the id for the product 
def priceAfterSale(item_id):
     item = Product.objects.get(pk=item_id) 
     discount = 0 #mas sale can discount the price of the product
     items = ProductINSale.objects.filter(product=item).values() #all the sales for this product
     
     if items:
       for product in items:
          sale = Sale.objects.get(pk=product["sale_id"])
          discount = sale.discount
     return {'product_id': item_id ,'price': round(item.price * ( 100 - discount)/100 , 2) , 'sale': discount} #return the price after the sale and the discount 

def getItem(list_id):
     return (Product.objects.get(pk=list_id))

def emailOrder(request):
     order=Order.objects.get(pk=cp.userDict["od"])
     subtotal = (order.total_price) - order.FreeShipping
     carts = order.carts.values()
     all_products = []
     salesProducts=[]
     for cart in carts:
          product = Product.objects.get(pk=cart["product_id"])
          all_products.append(product)
          user = Person.objects.get(pk=cart["user_id"])
          salesProducts.append(priceAfterSale(cart["product_id"]))
     return render(request,"emailOrder.html" , {'order':order ,'carts':carts ,'user':user , 'all_products':all_products ,'salesProducts':salesProducts ,'subtotal':subtotal})


def AddProductINSale(productID,discount):
     sale=Sale.objects.filter(discount=discount)
     if not sale: #this discount existe
          sale=Sale(discount=discount)
          sale.save()
     else : 
          sale = sale.get()
     product=Product.objects.get(pk=productID)
     ProductINSale.objects.create(sale=sale,product=product)

def countProductInAllOrders(productID):
     orders = Order.objects.all() #all the orders
     count = 0 
     for order in orders:
          carts = order.carts.values() #all the carts in this order
          for cart in carts:
               if cart["product_id"] == productID:
                    count+=1;
     return count 
#----------------------------------------------------------------------------------------------------------
    
#----------------------- 3 pages for home : home => Visitor ; userHome = > User ; administration => Admin
#------------- Visitor Home
def home(request):
     return render(request,"home.html",)

#------------- User Home   
def userHome(request):
     return render(request,"userHome.html")

#------------- Admin Home   
def administration(request):
     user=Person.objects.get(pk=request.session['username'])
     return render(request,"administrationHome.html",{'user':user})
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------- login and rigster ----------------------------------------
def login(request ):
     if request.method == 'POST':
      MyLoginForm = LoginForm(request.POST or None)
      if MyLoginForm.is_valid():
           username = MyLoginForm.cleaned_data['username']
           password = MyLoginForm.cleaned_data['password']
        
           try:
            user = Person.objects.get(pk=username)
            request.session['username'] = username
            if user.password == password and user.email == username and user.role == 1: #user - login
                    return render(request, "userHome.html")
            elif user.password == password and user.email == username and user.role == 2: #admin -login
                return render(request, "administrationHome.html")
            else:
                messages.success(request, ('The password you entered is incorrect'))
                return render(request, 'login.html',{'alertMessage':"The password you entered is incorrect!!!"})

           except Person.DoesNotExist:
             messages.success(request, ('The user does not exist in the system!!!'))
             return render(request, 'login.html',{'alertMessage':"The user does not exist in the system!!!"})

      else:
         return render(request, 'login.html')
     else:
       return render(request, 'login.html')

def login2(request ):
     if request.method == 'POST':
        MyLoginForm = LoginForm(request.POST or None)
        if MyLoginForm.is_valid():
            username = MyLoginForm.cleaned_data['username']
            password = MyLoginForm.cleaned_data['password']
            user = isExisting_User(username)
            if user:
                request.session['username'] = username
                if user["password"] == password  and user["role"] == 1: #user - login
                     return render(request, "userHome.html")
                elif user["password"] == password  and user["role"] == 2: #admin - login
                     return render(request, "administrationHome.html")
                else:
                     messages.success(request, ('The password you entered is incorrect'))
                     return render(request, 'login2.html',{'alertMessage':"The password you entered is incorrect!!!"})
            else:
                 messages.success(request, ('The user does not exist in the system!!!'))

     return render(request, 'login2.html')


#-----------------------register create new account 
def registr(request):
     if request.method == 'POST':
          MyRegistrForm = RegistrForm(request.POST or None)

          if MyRegistrForm.is_valid():
               MyRegistrForm.save()
               return render(request,'userHome.html')
          
          else:
               messages.success(request, ('Please fill out all the fields.!!'))
               return render(request,'registr.html')
     else:
          return render(request,'registr.html')
#-------------Add new admin 
def registrAdmin(request):
     if request.method == 'POST':
          MyRegistrForm = RegistrForm(request.POST or None)      

          if MyRegistrForm.is_valid():
               MyRegistrForm.save()
               email = MyRegistrForm.cleaned_data['email']
               admin= Person.objects.filter(email=email).update(role=Person.ADMIN)
               return render(request,'administrationHome.html')
          else:
               messages.success(request, ('Please fill out all the fields.!!'))
               return render(request,'registrAdmin.html')
     else:
          return render(request,'registrAdmin.html')    

# def addCustomer(request):
#      return render(request,"addCustomer.html")
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------Cart Shopping-----------------------------------------

#-----------Add to cart from productsUser.html that the size is S defult data     
def cart(request,list_id):
     cp.setSize(Cart.SMALL)
     cart = Cart.objects.filter(user=request.session['username'],product=Product.objects.get(pk=list_id),cartAvilable=Cart.Avilable)
     if cart:
       if cart.get().SIZE == cp.userDict["size"]: #if we have this product in the same size 
        cart.update(qty = cart.get().qty+1) 
       else:
          c = Cart(user=request.session['username'], product=Product.objects.get(pk=list_id))
          c.save()

     else:
        user = Person.objects.get(pk=request.session['username'])
        c = Cart(user=user, product=Product.objects.get(pk=list_id)) 
        c.save()
     return redirect('showCart')

#-----------Add to cart from productQuickView.html that the user choose the size
def Addcart(request,list_id):
     cart = Cart.objects.filter(user=request.session['username'],product=Product.objects.get(pk=list_id),cartAvilable=Cart.Avilable)
     if cart:
       if cart.get().SIZE == cp.userDict["size"]:#if we have this product in the same size
         cart.update(qty = cart.get().qty+1)
       else:
          c = Cart(user=request.session['username'], product=Product.objects.get(pk=list_id))
          c.save()
          Cart.objects.filter(id=c.id).update(SIZE= cp.userDict["size"])
          cp.setSize(Cart.SMALL)
       
     else :
       user = Person.objects.get(pk=request.session['username'])
       c = Cart(user=user, product=Product.objects.get(pk=list_id))
       c.save()
       Cart.objects.filter(id=c.id).update(SIZE= cp.userDict["size"])
       cp.setSize(Cart.SMALL)
     return redirect('showCart')

#----------- update the size to SMALL 
def smallSize(request,list_id):
     cp.setSize(Cart.SMALL)
     item=Product.objects.get(pk=list_id)
     price =priceAfterSale(list_id)["price"]
     return render(request , "productQuickView.html", {'item': item , 'price':price})

#----------- update the size to MEDIUM
def mediumSize(request,list_id):
     cp.setSize(Cart.MEDIUM )  
     item=Product.objects.get(pk=list_id)
     price =priceAfterSale(list_id)["price"]
     return render(request , "productQuickView.html", {'item': item , 'price':price})

#----------- update the size to LARGE
def largeSize(request,list_id):
     cp.setSize(Cart.LARGE)
     item=Product.objects.get(pk=list_id)
     price =priceAfterSale(list_id)["price"]
     return render(request , "productQuickView.html", {'item': item , 'price':price})

#----------- update the size to XTRALARGE
def xtralargeSize(request,list_id):
     cp.setSize(Cart.XTRALARGE)
     item=Product.objects.get(pk=list_id)
     price =priceAfterSale(list_id)["price"]
     return render(request , "productQuickView.html", {'item': item , 'price':price})

#-----------displaye the cart 
def showCart(request):
     username=request.session['username']
     user = Person.objects.get(pk=username)
     all_products = Cart.objects.filter(user = user, cartAvilable=Cart.Avilable).values()
     items = []
     saleList = [] 
     totalPrice = 0
    
     for item in all_products:
          priceAftersale = priceAfterSale(item["product_id"])
          product =Product.objects.get(pk=item["product_id"])
          items.append(product)
          totalPrice += (item["qty"]*priceAftersale["price"])

          if priceAftersale["price"] != product.price: #we have a discount 
               DicSale = {"id" : item["product_id"]  , "price" : priceAftersale ,"sale" :True, "discount" : priceAftersale["sale"]}
          else:
               DicSale = {"id" : item["product_id"]  , "price" : priceAftersale ,"sale" :False, "discount" : priceAftersale["sale"]}
          
          saleList.append(DicSale)
     
     totalPrice = round(totalPrice,2)
     if totalPrice < float(cp.userDict["FreeShipping"].getFreeShipping_totalPrice()) or float(cp.userDict["FreeShipping"].getFreeShipping_totalPrice()) == 0:
               totalPrice = round(totalPrice,2) +  float(cp.userDict["FreeShipping"].getShippingPrice())

     return render(request,"showCart.html",{"products":all_products , "items":items ,"totalPrice":totalPrice , 'saleList' : saleList ,'email':username} )

#----------------------delete the cart 
def deleteCart(request,list_id):
     carts = Cart.objects.filter(user=request.session['username'],product=Product.objects.get(pk=list_id),cartAvilable = Cart.Avilable).update(cartAvilable = Cart.notAvilable)   
     messages.success(request, ('Item Has Been Deleted!'))
     return redirect('showCart')

#----------------------add  Quantty to the cart 
def addQuantty_Cart(request,list_id):
     cart = Cart.objects.get(pk=list_id)
     product = Product.objects.get(pk=cart.product_id)
     qty = cart.qty + 1 
     if cart.SIZE == Cart.SMALL and qty > product.qty_small:
          messages.success(request, ('The maximum quantity Small is: ' + ' '+  str(product.qty_small)))
     elif cart.SIZE == Cart.MEDIUM and qty > product.qty_medium:
          messages.success(request, ('The maximum quantity Medium is: ' + ' '+ str(product.qty_medium)))    
     elif cart.SIZE == Cart.LARGE and qty > product.qty_large:
          messages.success(request, ('The maximum quantity Large is: ' + ' '+  str(product.qty_large)))    
     elif cart.SIZE == Cart.XTRALARGE and qty > product.qty_xtraLarge:
          messages.success(request, ('The maximum quantity xtraLarge is: ' + ' '+  str(product.qty_xtraLarge)))
     
     else:
       Cart.objects.filter(id=list_id).update(qty= qty)
       messages.success(request, ('Item Has Add Quantty !'))
     return redirect('showCart')

#----------------------sub  Quantty from the cart 
def subQuantty_Cart(request,list_id):
     cart = Cart.objects.get(pk=list_id)
     if cart.qty > 1:
       qty = cart.qty -1 
       Cart.objects.filter(id=list_id).update(qty= qty)
       messages.success(request, ('Item Has Sub Quantty !'))
     
     else:
           messages.success(request, ('The minimum you can order is 1 !!!'))

     return redirect('showCart')
#----------------------------------------------------------------------------------------------------------

#-------------------------------------------displaye the products------------------------------------------
#-------------products that the visitor can see
def products(request,categoryid):
      category = Category.objects.get(pk=categoryid)
     # all_products = Product.objects.values()
      all_products = Product.objects.filter(category=category).values()
     #saleListDic = [{'productId':"" , "newPrice_AfterSale": 0 }]
      saleList = [] 

      for item  in  all_products:
          priceAftersale = priceAfterSale(item["id"])
          if priceAftersale["price"] != item["price"]:
            DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :True , "discount" : priceAftersale["sale"]}
          else:
            DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :False , "discount" : priceAftersale["sale"]}
          saleList.append(DicSale)
      return render(request,"products.html",{'all_products' : all_products , 'saleList' : saleList ,'categoryName':category.name} ) 

#-------------products that the user can see
def productsUser(request,categoryid):
     cp.setCategory(categoryid)
     category = Category.objects.get(pk=categoryid)
     all_products = Product.objects.filter(category=category).values()
    # all_products = Product.objects.values()
     #saleListDic = [{'productId':"" , "newPrice_AfterSale": 0 }]
     saleList = [] 

     for item  in  all_products:
          priceAftersale = priceAfterSale(item["id"])
          if priceAftersale["price"] != item["price"]:
            DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :True , "discount" : priceAftersale["sale"]}
          else:
            DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :False , "discount" : priceAftersale["sale"]}
          saleList.append(DicSale)
     return render(request,"productsUser.html",{'all_products' : all_products , 'saleList' : saleList,'categoryName':category.name } ) 

#------------the user can see the product Quick View
def productQuickView(request,list_id):
     item=Product.objects.get(pk=list_id)
     price =priceAfterSale(list_id)["price"]
     return render(request , "productQuickView.html", {'item': item , 'price':price})

#-------------the products that the admin can see
def productShow_admin(request):
     all_products = Product.objects.values()
     #saleListDic = [{'productId':"" , "newPrice_AfterSale": 0 }]
     saleList = [] 

     for item  in  all_products:
          priceAftersale = priceAfterSale(item["id"])
          if priceAftersale["price"] != item["price"]:
                DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :True , "discount" : priceAftersale["sale"]}
          else:
            DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :False , "discount" : priceAftersale["sale"]}
          saleList.append(DicSale)
     return render(request,"productShow_admin.html",{'all_products' : all_products , 'saleList' : saleList})

#-------------add item to the list products
     
def addItem(request):
#          submitted = False
#     if request.method == 'POST':
#         form = ProductForm(request.POST , request.FILES)# MUST ADD FOR FILE UPLOAD OTHERWISE ERROR
#         if form.is_valid():
#           form.save()
#           all_items = Product.objects.all
#           submitted = True
#           messages.success(request, ('Product item Has Been Added'))
#           return render(request, 'productList.html', {'all_items': all_items, "form": form, 'submitted': submitted})
#     else:
#         all_items = Product.objects.all
#         form = ProductForm()
#         return render(request, 'productList.html', {'all_items': all_items, "form": form, 'submitted': submitted})
     submitted = False
     if request.method == 'POST':
          MyaddItemForm = addItemForm(request.POST , request.FILES)

          if MyaddItemForm.is_valid():
               MyaddItemForm.save()
               all_items = Product.objects.all
               submitted = True
               messages.success(request, ('Item Has Been Added!'))
               return redirect('productShow_admin')
          
          else:
               all_items = Product.objects.all
               form = addItemForm()
               messages.success(request, ('Please fill out all the fields.!!'))
               return render(request,'addItem.html',{'all_items': all_items, "form": form, 'submitted': submitted})
     else:
          all_items = Product.objects.all
          form = addItemForm()
          return render(request,'addItem.html',{'all_items': all_items, "form": form, 'submitted': submitted})

#-------------edit the small quantity
def EditSmallQuantity(request,list_id):
     if request.method == 'POST':
          item = Product.objects.get(pk=list_id)
          MyeditItemForm = addItemForm(request.POST or None, instance=item)
          
          if MyeditItemForm.is_valid():
               MyeditItemForm.save()
               messages.success(request, ('The S Quantity Has Been Edited!'))
               return redirect('productShow_admin')

          else:
           messages.success(request, ('Something is wrong!'))
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditSmallQuantity.html', {'item': item})
     else:
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditSmallQuantity.html', {'item': item})

#-------------edit the medium quantity
def EditMediumQuantity(request,list_id):
     if request.method == 'POST':
          item = Product.objects.get(pk=list_id)
          MyeditItemForm = addItemForm(request.POST or None, instance=item)
          
          if MyeditItemForm.is_valid():
               MyeditItemForm.save()
               messages.success(request, ('The M Quantity Has Been Edited!'))
               return redirect('productShow_admin')

          else:
           messages.success(request, ('Something is wrong!'))
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditMediumQuantity.html', {'item': item})
     else:
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditMediumQuantity.html', {'item': item})

#-------------edit the large quantity
def EditLargeQuantity(request,list_id):
     if request.method == 'POST':
          item = Product.objects.get(pk=list_id)
          MyeditItemForm = addItemForm(request.POST or None, instance=item)
          
          if MyeditItemForm.is_valid():
               MyeditItemForm.save()
               messages.success(request, ('The L Quantity Has Been Edited!'))
               return redirect('productShow_admin')

          else:
           messages.success(request, ('Something is wrong!'))
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditLargeQuantity.html', {'item': item})
     else:
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditLargeQuantity.html', {'item': item})

#-------------edit the XtraLarge quantity
def EditXtraLargeQuantity(request,list_id):
     if request.method == 'POST':
          item = Product.objects.get(pk=list_id)
          MyeditItemForm = addItemForm(request.POST or None, instance=item)
          
          if MyeditItemForm.is_valid():
               MyeditItemForm.save()
               messages.success(request, ('The XL Quantity Has Been Edited!'))
               return redirect('productShow_admin')

          else:
           messages.success(request, ('Something is wrong!'))
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditXtraLargeQuantity.html', {'item': item})
     else:
           item = Product.objects.get(pk=list_id)
           return render(request, 'EditXtraLargeQuantity.html', {'item': item})

#-------------edit the sale quantity          
def Editsale(request,list_id):
     if request.method == 'POST':
          item = Product.objects.get(pk=list_id)
          MyeditItemForm = addItemForm(request.POST or None, instance=item)
          
          if MyeditItemForm.is_valid():
               MyeditItemForm.save()
               messages.success(request, ('The Sale Has Been Edited!'))
               return redirect('productShow_admin')

          else:
           messages.success(request, ('Something is wrong!'))
           item = Product.objects.get(pk=list_id)
           return render(request, 'Editsale.html', {'item': item})
     else:
           item = Product.objects.get(pk=list_id)
           return render(request, 'Editsale.html', {'item': item})

#-------------delete item        
def deleteItem(request,list_id):
     item = Product.objects.get(pk=list_id)
     carts = Cart.objects.filter(product = item,cartAvilable=Cart.Avilable)
     if carts:
           messages.success(request, ('Are you cure? this product in cart!'))
     else:
       item.delete()
       messages.success(request, ('Item Has Been Deleted!'))
     return redirect('productShow_admin')
#----------------------------------------------------------------------------------------------------------

#---------------------------------------------forgot Password-----------------------------------------------
def forgotPassword(request):
     return render(request,"ForgotPassword.html")

def reports(request):
     return render(request , "reports.html")

def todo(request):
   return render(request,"todo.html")

def clcQtys(itemID , qtys , size):
     flag = -1  #flag to check if the user can order the qty that he wants or not ( -1 he can)
     item = Product.objects.get(pk=itemID)

     if size == 1:
            maxQty=item.qty_small - qtys
     if size == 2:
            maxQty=item.qty_medium - qtys
     if size == 3:
            maxQty=item.qty_large - qtys
     if size == 4:
            maxQty=item.qty_xtraLarge - qtys

     if maxQty < 0:
         flag = maxQty + qtys  # == item qty that can order 
     
     return (flag)   

def updateQtyBySize(itemID ,cartID , qtys , size):
     item = Product.objects.get(pk=itemID)
     if size == Cart.SMALL : #"s"
            qty=item.qty_small - qtys
            if qty <  0 :
              Cart.objects.filter(id=cartID).update(qty=item.qty_small)
              Product.objects.filter(id=itemID).update(qty_small=0)
            else: 
               Product.objects.filter(id=itemID).update(qty_small=qty)
               Cart.objects.filter(id=cartID).update(qty= qtys)

     if size == Cart.MEDIUM :#"m"
            qty=item.qty_medium - qtys
            if qty < 0 :
                 Cart.objects.filter(id=cartID).update(qty= item.qty_medium)
                 Product.objects.filter(id=itemID).update(qty_medium=0)
            else:
              Product.objects.filter(id=itemID).update(qty_medium=qty)
              Cart.objects.filter(id=cartID).update(qty= qtys)

     if size == Cart.LARGE:#"l"
            qty=item.qty_large - qtys
            if qty < 0 :
                 Cart.objects.filter(id=cartID).update(qty= item.qty_large)
                 Product.objects.filter(id=itemID).update(qty_large=0)
            else:
                Product.objects.filter(id=itemID).update(qty_large=qty)
                Cart.objects.filter(id=cartID).update(qty= qtys)

     if size == Cart.XTRALARGE: #"xl"
            qty=item.qty_xtraLarge - qtys
            if qty < 0 :
                 Cart.objects.filter(id=cartID).update(qty=item.qty_xtraLarge)
                 Product.objects.filter(id=itemID).update(qty_xtraLarge=0)
            else:
               Product.objects.filter(id=itemID).update(qty_xtraLarge=qty)
               Cart.objects.filter(id=cartID).update(qty= qtys)

def checkOut(request):
     user=request.session['username']
     all_products = Cart.objects.filter(user = user,cartAvilable=Cart.Avilable).values()

     for item in all_products:
          qty = clcQtys(item["product_id"],item["qty"],item["SIZE"])
          Product_displaye = Product.objects.get(pk=item["product_id"])
          d=item["product_id"]

          if qty != -1: 
            return render(request,"notEnought.html",{'qty':Product_displaye.title,'ok':qty,'item_id':d})
     return render(request,"checkOut.html")    

def OrderOK(request):
     user=request.session['username']
     all_products = Cart.objects.filter(user = user,cartAvilable=Cart.Avilable).values()
     order=Order()
     order.save()
     Order.objects.filter(id=order.id).update(date = datetime.datetime.now())
     cp.setOrderId(order.id)
     totalPrice = 0

     for item in all_products:
          updateQtyBySize(item["product_id"] ,item["id"],item["qty"] , item["SIZE"] )
          cart = Cart.objects.filter(user=request.session['username'],product=Product.objects.get(pk=item["product_id"]),cartAvilable=Cart.Avilable)
          order.carts.add(cart.get())
          cart.update(cartAvilable=Cart.notAvilable)
          priceAftersale = priceAfterSale(item["product_id"])
          totalPrice += (priceAftersale["price"] * item["qty"])
          
     totalPrice = round(totalPrice,2)
     if totalPrice < float(cp.userDict["FreeShipping"].getFreeShipping_totalPrice()) or float(cp.userDict["FreeShipping"].getFreeShipping_totalPrice()) == 0:
               totalPrice = round(totalPrice,2) +  float(cp.userDict["FreeShipping"].getShippingPrice())
               Order.objects.filter(id=order.id).update(FreeShipping = int(cp.userDict["FreeShipping"].getShippingPrice()))


     updateOrder = Order.objects.filter(id=order.id).update(total_price = totalPrice)
     send_email(request.session['username'],order.id)
     return redirect('INVOICE',orderid = order.id)

#delete all the products in cart
def CancelOrder(request):
     all_cart = Cart.objects.filter(user=request.session['username'],cartAvilable=Cart.Avilable).values()

     for cart in all_cart:
          Cart.objects.filter(id = cart['id']).update(cartAvilable=Cart.notAvilable) 
         
     return render(request,"userHome.html")
#delete the product that the user cancle the order for it 
def cancleProduct(request,item_id):
     Cart.objects.filter(user=request.session['username'],product=Product.objects.get(pk=item_id),cartAvilable=Cart.Avilable).update(cartAvilable = Cart.notAvilable)     
     return redirect('showCart')

def UpdateQty_DoneShopping(request):
      #order the true qty 
     user=request.session['username']
     all_products = Cart.objects.filter(user = user,cartAvilable=Cart.Avilable).values()

     for item in all_products:
        qty = clcQtys(item["product_id"] , item["qty"],item["SIZE"])
        if qty == -1 :
             qty = item["qty"]
        Cart.objects.filter(user=request.session['username'],product=Product.objects.get(pk=item["product_id"]),cartAvilable=Cart.Avilable).update(qty= qty)
    
     return redirect('showCart')

#------------------------------------------Sales----------------------------------------------
def sales(request):   
     return render(request,"sales.html")       

def EditFreeShipping(request ):
     if request.method == 'POST':
           FreeShippingForm = EditFreeShippingForm(request.POST or None )
           if FreeShippingForm.is_valid():
               priceShipping=FreeShippingForm.cleaned_data['priceShipping']
               priceAmonut= FreeShippingForm.cleaned_data['priceAmonut']

               cp.userDict["FreeShipping"].setFreeShipping_totalPrice(priceAmonut)
               cp.userDict["FreeShipping"].setShippingPrice(priceShipping)
               messages.success(request, ('Free Shipping Has Been Edited'))
               return render(request, "sales.html")
           else:
             return render(request,"EditFreeShipping.html")
     else:
       return render(request,"EditFreeShipping.html")

def MangmentDiscount(request):
     all_products = Product.objects.values()
     #saleListDic = [{'productId':"" , "newPrice_AfterSale": 0 }]
     saleList = [] 

     for item  in  all_products:
          priceAftersale = priceAfterSale(item["id"])
          if priceAftersale["price"] != item["price"]:
                DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :True , "discount" : priceAftersale["sale"]}
          else:
            DicSale = {"id" : item["id"]  , "price" : priceAftersale["price"] ,"sale" :False , "discount" : priceAftersale["sale"]}
          saleList.append(DicSale)
     return render(request,"MangmentDiscount.html",{'all_products' : all_products , 'saleList' : saleList})
       
def Editsale(request,list_id):
     if request.method == 'POST':
          item = Product.objects.get(pk=list_id)
          MyEditSaleForm = EditSaleForm(request.POST or None)
          
          if MyEditSaleForm.is_valid():
               discount=MyEditSaleForm.cleaned_data['discount']
               AddProductINSale(list_id,discount)
               messages.success(request, ('The Sale Has Been Edited!'))
               return redirect('MangmentDiscount')

          else:
           messages.success(request, ('Please fill out the field.!!'))
           item = Product.objects.get(pk=list_id)
           return render(request, 'Editsale.html', {'item': item})
     else:
           item = Product.objects.get(pk=list_id)
           return render(request, 'Editsale.html', {'item': item})

def MangmentSales(request):   
     return render(request,"MangmentSales.html")

def TopProduct(request):
     orders = Order.objects.all() #all the orders
     TopProduct_ID = 0 
     MaxCount = 0
     for order in orders:
          carts = order.carts.values() #all the carts in this order
          for cart in carts:
               count = countProductInAllOrders(cart["product_id"])
               if count > MaxCount:
                    MaxCount = count
                    TopProduct_ID = cart["product_id"]

     topProduct = Product.objects.get(pk=TopProduct_ID)
     return render(request,"topProduct.html",{'item': topProduct , 'ID':TopProduct_ID})

def setTopSale(request,itemID):
       if request.method == 'POST':
          item = Product.objects.get(pk=itemID)
          MyEditSaleForm = EditSaleForm(request.POST or None)
          
          if MyEditSaleForm.is_valid():
               discount=MyEditSaleForm.cleaned_data['discount']
               AddProductINSale(itemID,discount)
               messages.success(request, ('The Sale Has Been Edited!'))
               return render(request,"sales.html")

          else:
           messages.success(request, ('Please fill out the field.!!'))
           item = Product.objects.get(pk=itemID)
           return render(request, 'setTopSale.html', {'item': item})
       else:
           item = Product.objects.get(pk=itemID)
           return render(request, 'setTopSale.html', {'item': item})


def Usersanagement(request):
     users=Person.objects.all()
     return render(request,"Usersanagement.html",{'users':users})     

def deleteUser(request, username):
     Person.objects.filter(pk=username).delete()
     messages.success(request, ('User Has Been Deleted!'))
     return redirect('Usersanagement')   

def displayeUser(request,username):
     user=Person.objects.get(pk=username)
     return render(request ,"displayeUse.html",{'user':user})

def updateUser_Admin(request,username):
     user=Person.objects.get(pk=username)
     if request.method == 'POST':
           MySettingForm = RegistrForm(request.POST or None, instance=user)
           if MySettingForm.is_valid():
                MySettingForm.save()
                messages.success(request, ('Your Info Has Been Edited!'))
     return render(request,"updateUser_Admin.html",{'user':user , 'email':user.email})

def settingAdmin(request):
     user=Person.objects.get(pk=request.session['username'])
     if request.method == 'POST':
           MySettingForm = RegistrForm(request.POST or None, instance=user)
           if MySettingForm.is_valid():
                MySettingForm.save()
                messages.success(request, ('Your Info Has Been Edited!'))
     return render(request,"updateUser_Admin.html",{'user':user , 'email':request.session['username']})

def orderHistory(request,username):
     customer = Person.objects.get(pk=username)
     orderForUser=[]
      
     orders = Order.objects.all()
     for order in orders:
          carts = order.carts.values() #all the carts in this order
          for cart in carts:
               if cart["user_id"] == username:
                    orderForUser.append(order)
     return render(request,"orderHistory.html",{ 'orders': orderForUser ,'user' :customer})

def displayOrder(request,orderid):
     order=Order.objects.get(pk=orderid)
     subtotal = (order.total_price) - order.FreeShipping
     carts = order.carts.values()
     all_products = []
     salesProducts=[]
     for cart in carts:
          product = Product.objects.get(pk=cart["product_id"])
          all_products.append(product)
          user = Person.objects.get(pk=cart["user_id"])
          salesProducts.append(priceAfterSale(cart["product_id"]))
     return render(request,"displayOrder.html" , {'order':order ,'carts':carts ,'user':user , 'all_products':all_products ,'salesProducts':salesProducts ,'subtotal':subtotal})


def allOrders(request):      
     orders = Order.objects.all()
     users =[]
     for order in orders:
          carts = order.carts.values() #all the carts in this order
          for cart in carts:
               user=Person.objects.get(pk=cart["user_id"])
               Dic = {'orderId': order.id , 'fullname' :user.fullname , 'email' :user.email}
               if Dic not in users:
                 users.append(Dic) 
     return render(request,"allOrders.html" , { 'orders': orders , 'users' : users})

def deleteOrder(request,orderID):
   Order.objects.filter(id=orderID).delete()
   messages.success(request, ('Order Has Been Deleted!'))
   return redirect('allOrders')

def deleteOrderUser(request,orderID):
   order = Order.objects.get(pk=orderID)
   carts = order.carts.values()
   for cart in carts:
        user = cart["user_id"]
   Order.objects.filter(id=orderID).delete()
   messages.success(request, ('Order Has Been Deleted!'))
   return redirect('orderHistory', username = user)

def editOrder(request,orderID):
   order=Order.objects.get(pk=orderID)
   carts = order.carts.values()
   for cart in carts:
        user = Person.objects.get(pk=cart["user_id"])
   return render(request,"editOrder.html",{'user':user , 'order' : order})

def editOrderCancle(request,orderID):
   order = Order.objects.filter(id=orderID).update(status=Order.Cancle)
   messages.success(request, ('Status Order Has Been Edited To Cancle!'))
   return redirect('allOrders')

def editOrderComplete(request,orderID):
   order = Order.objects.filter(id=orderID).update(status=Order.Complete)
   messages.success(request, ('Status Order Has Been Edited To Complete!'))
   return redirect('allOrders')

def editOrderUser(request,orderID):
   order=Order.objects.get(pk=orderID)
   carts = order.carts.values()
   for cart in carts:
        user = Person.objects.get(pk=cart["user_id"])
   return render(request,"editOrderUser.html",{'user':user , 'order' : order})

def editOrderCancleUser(request,orderID):
   order = Order.objects.filter(id=orderID).update(status=Order.Cancle)
   order=Order.objects.get(pk=orderID)
   carts = order.carts.values()
   for cart in carts:
        user = cart["user_id"]   
   messages.success(request, ('Status Order Has Been Edited To Cancle!'))
   return redirect('orderHistory',username=user)

def editOrderCompleteUser(request,orderID):
   order = Order.objects.filter(id=orderID).update(status=Order.Complete)
   order=Order.objects.get(pk=orderID)
   carts = order.carts.values()
   for cart in carts:
        user = cart["user_id"]
   messages.success(request, ('Status Order Has Been Edited To Complete!'))
   return redirect('orderHistory' ,username=user)

  
def addWishlist(request,list_id):
     w1 = wishList.objects.filter(user=request.session['username'],product=Product.objects.get(pk=list_id))
     if  w1:
       messages.success(request, ('Item already in youre wishlist'))
       return redirect('productsUser',categoryid= cp.userDict["current_category"])
     else:
       w = wishList(user= Person.objects.get(pk=request.session['username']), product=Product.objects.get(pk=list_id))
       w.save()
       wishList.objects.filter(id=w.id).update(SIZE= cp.userDict["size"])

       return redirect('wishListt')
       

def wishListt(request):
     all_products = wishList.objects.filter(user=request.session['username']).values()
     items = []
     saleList = [] 

     for item in all_products:
          priceAftersale = priceAfterSale(item["product_id"])
          product =Product.objects.get(pk=item["product_id"])# getItem(item["product_id"])
          items.append(product)
          if priceAftersale["price"] != product.price: #we have a discount 
               DicSale = {"id" : item["product_id"]  , "price" : priceAftersale ,"sale" :True, "discount" : priceAftersale["sale"]}
          else:
               DicSale = {"id" : item["product_id"]  , "price" : priceAftersale ,"sale" :False, "discount" : priceAftersale["sale"]}
          
          saleList.append(DicSale)

     return render(request,"wishListt.html",{"products":all_products , "items":items ,'saleList' : saleList } )

def deletewish(request,list_id):
     wishList.objects.filter(user=request.session['username'],product=Product.objects.get(pk=list_id)).delete()   
     messages.success(request, ('Item Has Been Deleted!'))
     return redirect('wishListt')

def settingUser(request):
     user=Person.objects.get(pk=request.session['username'])
     if request.method == 'POST':
           MySettingForm = RegistrForm(request.POST or None, instance=user)
           if MySettingForm.is_valid():
                MySettingForm.save()
                messages.success(request, ('Your Info Has Been Edited!'))
     return render(request,"updateUser.html",{'user':user , 'email':request.session['username']})

def INVOICE(request,orderid):
     order=Order.objects.get(pk=orderid)
     subtotal = (order.total_price) - order.FreeShipping
     carts = order.carts.values()
     all_products = []
     salesProducts=[]
     for cart in carts:
          product = Product.objects.get(pk=cart["product_id"])
          all_products.append(product)
          user = Person.objects.get(pk=cart["user_id"])
          salesProducts.append(priceAfterSale(cart["product_id"]))
     return render(request,"INVOICE.html" , {'order':order ,'carts':carts ,'user':user , 'all_products':all_products ,'salesProducts':salesProducts ,'subtotal':subtotal})

def UserHistory(request):
     customer = Person.objects.get(pk=request.session['username'])
     orderForUser=[]
      
     orders = Order.objects.all()
     for order in orders:
          carts = order.carts.values() #all the carts in this order
          for cart in carts:
               if cart["user_id"] == request.session['username']:
                    orderForUser.append(order)
     return render(request,"UserHistory.html",{ 'orders': orderForUser ,'user' :customer})

def joinClub(request):
   return render(request,"joinClub.html")

def joinClubOK(request):
   user=request.session['username']  
   Person.objects.filter(email=user).update(CLUB_CARD = 1)
   messages.success(request, ('Thank You For Joined to the club.'))
   return render(request,"userHome.html")

def addCustomer(request):
     if request.method == 'POST':
          MyRegistrForm = RegistrForm(request.POST or None)
          if MyRegistrForm.is_valid():
               mycol = connection_MongoDB_Person()
               MyRegistrForm.save()
               mydict = { "fullname":MyRegistrForm.cleaned_data['fullname'], "email":MyRegistrForm.cleaned_data['email'],"mobileno" :MyRegistrForm.cleaned_data['mobileno'] , "address":MyRegistrForm.cleaned_data['address'] ,"password" :MyRegistrForm.cleaned_data['password'],"role": 1}       
               x = mycol.insert_one(mydict)
               return redirect('Usersanagement')
          else:
              messages.success(request, ('Please fill out all the fields.!!'))
              return render(request,'addCustomer.html')
     else:
          return render(request,'addCustomer.html')