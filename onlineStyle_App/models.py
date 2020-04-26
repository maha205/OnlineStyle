from django.db import models
from django import forms

# Create your models here.
#suberuser : username: maha_gazalen === password: mg2051997

class Person(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200, primary_key=True  , unique=True )
    mobileno = models.CharField(max_length=200 ) #,db_index = True
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    CLUB_CARD_OFF = 0
    CLUB_CARD_ON = 1
    member_choisces_CLUB_CARD=((CLUB_CARD_OFF,'off') , (CLUB_CARD_ON,'on'))
    CLUB_CARD =models.IntegerField(choices=member_choisces_CLUB_CARD , default=CLUB_CARD_OFF)

    USER = 1 
    ADMIN = 2

    member_choisces=((USER,'user') , (ADMIN,'admin'))
    role = models.IntegerField(choices=member_choisces , default=USER)

    def __str__(self):
           return self.fullname  + ' | ' + str(self.email) + ' | ' + str(self.mobileno) + ' | ' + str(self.address)+ ' | ' + str(self.password)

      
# 1 Cart <-> N Product
class Product(models.Model):
    price = models.FloatField()
    description = models.CharField(max_length=400 , null = True)
    title = models.CharField(max_length=200)
    qty_small = models.IntegerField(default=0)
    qty_medium = models.IntegerField(default=0)
    qty_large = models.IntegerField(default=0)
    qty_xtraLarge = models.IntegerField(default=0)
    
    pic = models.ImageField(null = True, blank=True) 
    
    sales = models.ManyToManyField('Sale', through='ProductINSale')
    category = models.ForeignKey('Category',on_delete=models.CASCADE , null=True )
    def __str__(self):
          return str(self.title)

class Category(models.Model):
      name = models.CharField(max_length=400 , null = True ,unique=True )
      
      NotAvilable = 0 
      Avilable = 1 

      member_choisces=((NotAvilable,'Not Avilable') , (Avilable,'Avilable') )
      status = models.IntegerField(choices=member_choisces , default=NotAvilable)
     
      def __str__(self):
          return str(self.name)



class Cart(models.Model):
      #id auttomatic 
      user = models.ForeignKey(Person,on_delete=models.CASCADE)
      product = models.ForeignKey(Product,on_delete=models.CASCADE)

      qty = models.IntegerField(default=1)

      SMALL = 1 
      MEDIUM = 2
      LARGE = 3 
      XTRALARGE = 4 

      member_choisces=((SMALL,'S') , ( MEDIUM,'M') ,( LARGE,'L'),( XTRALARGE,'XL'))
      SIZE = models.IntegerField(choices=member_choisces , default=SMALL)
 
      Avilable = 1 #add cart 
      notAvilable = 0 #delete cart 
      
      member_choisces_Avulable=((Avilable,'Avilable') , (notAvilable,'notAvilable') )
      cartAvilable = models.IntegerField(choices=member_choisces_Avulable , default=Avilable)
       


# M Sale <->  M Product
class Sale(models.Model):
     discount = models.IntegerField(default=0) # X % discount for the product 
     
     NoSale = 0 
     Oneplus1 = 1 # 1+1 = 50% discount
     Twoplus1 = 2 # 2+1 = 33% discount
     Oneplushalf = 3 # 1+1/2 = 25% discount

     MEMBER_CHOICES = ((NoSale,'None') ,(Oneplus1,'1+1') , (Twoplus1,'2+1') , (Oneplushalf , '1+1/2') ,)
     sale = models.IntegerField(choices=MEMBER_CHOICES,default=NoSale,)

     products = models.ManyToManyField('Product', through='ProductINSale')
     
     

class ProductINSale(models.Model):
     sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
      carts = models.ManyToManyField(Cart)
      date = models.DateTimeField(auto_now=True, blank=True)
      total_price = models.IntegerField(default=0)

     #---------------status-----------------
      Cancle = 0 
      Complete = 1 
      Tracking = 2 

      member_choisces_order=((Cancle,'cancle'),(Tracking,'tracking') , ( Complete,'complete'))
      status = models.IntegerField(choices=member_choisces_order , default=Tracking)

      FreeShipping = models.IntegerField(default=0)


class wishList(models.Model):
       #id auttomatic 
      user = models.ForeignKey(Person,on_delete=models.CASCADE)
      product = models.ForeignKey(Product,on_delete=models.CASCADE)
      
      SMALL = 1 
      MEDIUM = 2
      LARGE = 3 
      XTRALARGE = 4 

      member_choisces=((SMALL,'S') , ( MEDIUM,'M') ,( LARGE,'L'),( XTRALARGE,'XL'))
      SIZE = models.IntegerField(choices=member_choisces , default=SMALL)

