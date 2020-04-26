from .models import Cart
from .models import Category

class FreeShipping():
     #price for  Shipping = 30 ILS when FreeShipping_totalPrice = 0
     def __init__(self ,FreeShipping_totalPrice = 0 ,shippingPrice = 30 ):
         self.FreeShipping_totalPrice = FreeShipping_totalPrice
         self.shippingPrice = shippingPrice
     
     def setFreeShipping_totalPrice(self,FreeShipping_totalPrice):
         self.FreeShipping_totalPrice = float(FreeShipping_totalPrice)
     def setShippingPrice(self,shippingPrice):
         self.shippingPrice = float(shippingPrice)
     def getFreeShipping_totalPrice(self):
         return float(self.FreeShipping_totalPrice)
     def getShippingPrice(self):
         return float(self.shippingPrice)

categorys = Category.objects.all()
userDict = {'categorys':categorys , 'size': Cart.SMALL ,'FreeShipping':FreeShipping(),'od':None,'current_category': None }

def setOrderId(od):
    userDict['od']=od
def setUser(user1):
    userDict['my_user'] = user1
def setCategory(current_category):
    userDict['current_category'] = current_category

def setSize(size): 
    userDict['size'] = size

def add_variable_to_context(request):
    return userDict

   