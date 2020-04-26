from django.urls import path
from onlineStyle_App import views

urlpatterns = [
#--------------------------Visitor Path Pages----------------------------
 path('', views.home, name="home"),
 path('login/', views.login, name="login"),
 path('login2/', views.login2, name="login2"),
 path('registr/', views.registr, name="registr"),
 path('products/<categoryid>', views.products , name="products"),
 path('forgotPassword/', views.forgotPassword , name="forgotPassword"),

#--------------------------User Path Pages----------------------------
 path('userHome/',views.userHome, name="userHome"),
 path('productsUser/<categoryid>',views.productsUser, name="productsUser"), #all the product
 path('productQuickView/<list_id>',views.productQuickView, name="productQuickView"),#product to displaye
 path('smallSize/<list_id>',views.smallSize, name="smallSize"),
 path('mediumSize/<list_id>',views.mediumSize, name="mediumSize"),
 path('largeSize/<list_id>',views.largeSize, name="largeSize"),
 path('xtralargeSize/<list_id>',views.xtralargeSize, name="xtralargeSize"),
 path('cart/<list_id>', views.cart , name="cart"),
 path('showCart/',views.showCart, name="showCart"),
 path('deleteCart/<list_id>',views.deleteCart, name="deleteCart"),
 path('addQuantty_Cart/<list_id>',views.addQuantty_Cart, name="addQuantty_Cart"),
 path('subQuantty_Cart/<list_id>',views.subQuantty_Cart, name="subQuantty_Cart"),
 path('Addcart/<list_id>',views.Addcart, name="Addcart"),
 path('checkOut/',views.checkOut, name="checkOut"),
 path('UpdateQty_DoneShopping/',views.UpdateQty_DoneShopping, name="UpdateQty_DoneShopping"),
 path('CancelOrder/',views.CancelOrder, name="CancelOrder"),
 path('cancleProduct/<item_id>',views.cancleProduct, name="cancleProduct"),
 path('OrderOK/',views.OrderOK, name="OrderOK"),
 path('INVOICE/<orderid>',views.INVOICE, name="INVOICE"),
 path('UserHistory/',views.UserHistory, name="UserHistory"),

 #--------------------------Admin Path Pages----------------------------
 path('administration/',views.administration , name="administration"), # home Admin page.

 path('productShow_admin/',views.productShow_admin, name="productShow_admin"),# products mangment page
 path('EditSmallQuantity/<list_id>',views.EditSmallQuantity, name="EditSmallQuantity"),
 path('EditMediumQuantity/<list_id>',views.EditMediumQuantity, name="EditMediumQuantity"),
 path('EditLargeQuantity/<list_id>',views.EditLargeQuantity, name="EditLargeQuantity"),
 path('EditXtraLargeQuantity/<list_id>',views.EditXtraLargeQuantity, name="EditXtraLargeQuantity"),
 path('addItem/',views.addItem, name="addItem"),
 path('deleteItem/<list_id>',views.deleteItem, name="deleteItem"),
 path('sales/',views.sales, name="sales"),# sales details page
 path('MangmentSales/',views.MangmentSales, name="MangmentSales"),# sales mangment page
 path('Editsale/<list_id>',views.Editsale, name="Editsale"),
 path('EditFreeShipping/',views.EditFreeShipping, name="EditFreeShipping"),
 path('MangmentDiscount/',views.MangmentDiscount, name="MangmentDiscount"),
 path('TopProduct/',views.TopProduct, name="TopProduct"),
 path('setTopSale/<itemID>',views.setTopSale, name="setTopSale"),

 path('registrAdmin/',views.registrAdmin , name="registrAdmin"), # home Admin page.
 path('Usersanagement/',views.Usersanagement, name="Usersanagement"),
 path('deleteUser/<username>',views.deleteUser, name="deleteUser"),
 path('displayeUser/<username>',views.displayeUser, name="displayeUser"),
 path('updateUser_Admin/<username>',views.updateUser_Admin, name="updateUser_Admin"),
 path('settingAdmin/',views.settingAdmin, name="settingAdmin"),
 path('orderHistory/<username>',views.orderHistory, name="orderHistory"),
 path('displayOrder/<orderid>',views.displayOrder, name="displayOrder"),
 path('allOrders/',views.allOrders, name="allOrders"),
 path('deleteOrder/<orderID>',views.deleteOrder, name="deleteOrder"),
 path('deleteOrderUser/<orderID>',views.deleteOrderUser, name="deleteOrderUser"),
 path('editOrder/<orderID>',views.editOrder, name="editOrder"),
 path('editOrderComplete/<orderID>',views.editOrderComplete, name="editOrderComplete"),
 path('editOrderCancle/<orderID>',views.editOrderCancle, name="editOrderCancle"), 
 path('editOrderUser/<orderID>',views.editOrderUser, name="editOrderUser"),
 path('editOrderCompleteUser/<orderID>',views.editOrderCompleteUser, name="editOrderCompleteUser"),
 path('editOrderCancleUser/<orderID>',views.editOrderCancleUser, name="editOrderCancleUser"),

 path('reports/',views.reports, name="reports"), #report page
 path('addCustomer/',views.addCustomer, name="addCustomer"),


 #--------------------------Email Path Pages----------------------------
 #path('Send_Email_order/',views.Send_Email_order, name="Send_Email_order"),
 path('emailOrder/',views.emailOrder, name="emailOrder"),

 path('todo/',views.todo , name="todo"),
 path('wishListt/',views.wishListt, name="wishListt"),
 path('addWishlist/<list_id>', views.addWishlist , name="addWishlist"),
 path('deletewish/<list_id>',views.deletewish, name="deletewish"),
 path('settingUser/',views.settingUser, name="settingUser"),
 path('joinClub/',views.joinClub , name="joinClub"),
 path('joinClubOK/',views.joinClubOK , name="joinClubOK"),
 path('addCustomer/',views.addCustomer, name="addCustomer"),
]
