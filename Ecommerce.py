import itertools
from operator import attrgetter
import json
import atexit
filename="/home/yonder/Documents/code/projects/Ecommerce/data.json"
validobjects=["shop","template","customer"]
autosave=True
autoload=True
oldid=[]
with open(filename,"r") as file:
    parse=json.load(file)
    if len(parse)>0:
        for x in parse:
            for y in range(len(parse[x])):
                oldid.append(parse[x][y]["id"])
    else:
        oldid.append(0)            
oldid.sort(reverse=True)
idmax=oldid[0]+1
id_gen=itertools.count(idmax)
def genid():
    return next(id_gen)
class save:
    objectstosave=[]
    def __init__(self):
        save.objectstosave.append(self)
    @classmethod
    def save_all_items(self,clear=False):
        if clear:
            with open(filename,"w") as file:
                json.dump({},file,indent=4)
            print("Data wiped clean")
            return     
        olddata={}
        for x in self.objectstosave:
            if x in system.customers or x in system.shops or x in system.templates:
                category=x.__class__.__name__
                if category in validobjects:
                    if category not in olddata:
                        olddata[category]=[]
                    olddata[category].append(x.__dict__)    
        with open(filename,"w") as file:
            json.dump(olddata,file,indent=4)
        print("Saving is done succesfully")        
class template(save):
    def __init__(self,name,price,id=None):
        if id is None:
            id=genid()
        self.id=id
        self.name=name
        self.price=price
        super().__init__()
class functions(save):
    def __init__(self,shops=None,customers=None,templates=None):
        if shops is None:
            shops=[]
        if customers is None:
            customers=[]
        if templates is None:
            templates=[]                        
        self.shops=shops
        self.customers=customers
        self.templates=templates
    def sort_all(self):
            self.shops.sort(key=attrgetter('id'))
            self.templates.sort(key=attrgetter('id'))
            self.customers.sort(key=attrgetter('id'))     
    def save(self):
        self.save_all_items()           
    def change_tempname(self,newname,id):
        if self.checktempbyname(newname):
            print(f"Template with name {newname} already eixsts")
        else:
            print(f"template ({self.gettempdetail(id,1)}) renamed to :{newname}")
            self.get_template_object(id).name=newname
            
    def change_customername(self,newname,id):
        if self.checkcustomerbyid(id):
            print(f"Customer ({self.getcustomerobj(id).name}) renamed to :{newname}")
            self.getcustomerobj(id).name=newname
            
    def change_customerfunds(self,id,value,type):
        if self.checkcustomerbyid(id):
            if value<=0:
                print("Value cannot be less than 1")
                return
            if type==1:
                print(f"Customer ({self.getcustomerobj(id).name}) Networth increased by :{value}")
                self.getcustomerobj(id).nworth+=value
            elif type==2:
                if self.getcustomerobj(id).nworth>0 and self.getcustomerobj(id).nworth>=value:
                    print(f"Customer ({self.getcustomerobj(id).name}) Networth decreased by :{value}")
                    self.getcustomerobj(id).nworth-=value
                else:
                    print("Not enough funds")                                                    
    
    def change_shop(self, value,id,type):
        if type==1:
            if self.checkshopbyid(id):
                print(f"Shop ({self.getshopobj(id).name}) renamed to :{value}")
                self.getshopobj(id).name=value 
        elif type==2:
            if value<=0:
                print("Value cannot be less than 1")
                return
            else:
                if self.checkshopbyid(id):
                    print(f"Shop ({self.getshopobj(id).name}) space incresased by :{value}")
                    self.getshopobj(id).space+=value 
        elif type==3:
            if value<=0:
                print("Value cannot be less than 1")
                return
            else:
                if self.checkshopbyid(id):
                    if self.getshopobj(id).space>value:
                        print(f"Shop ({self.getshopobj(id).name}) space decreased by :{value}")
                        self.getshopobj(id).space-=value
                    elif self.getshopobj(id).space==value:
                        print("You cannot reduce the space to 0 ")    
                    else:
                        print(f"You cannot adjust space, Remove item(s) from {self.getshopobj(id).name} first!")     
    def get_template_object(self,id):
        for x in self.templates:
            if x.id==id:
                return x       
    def add_shops(self,name,space):
        if space>0:
            self.shops.append(shop(name,space))
            print(f"Shop: {name} added with space {space}")
        else:
            print("Shop cannot have space less than 1")    
    def print_free_templates(self,sendback=False):
        if len(self.templates)>0:
            a=False
            for x in self.templates:
                if self.checkiftemplateisused(x.name):
                    continue
                else:
                    a=True
                    if sendback!=True:
                        print(f"{x.id}) {x.name} : $ {x.price}")
            if sendback:
                return a
    def printaddsupplytemplates(self,shopobj,sendback=False):
        if len(self.templates)>0:
            a=False
            for x in self.templates:
                if shopobj.checkforduplicateobjects(x.name,True):
                    continue
                else:
                    a=True
                    if sendback!=True:
                        print(f"{x.id}) {x.name} : $ {x.price}")
            if sendback:
                return a
                                   
    def remove_shops(self,id):
            print(f"Shop: {self.getshopobj(id).name} removed")
            for x in self.customers:
                for y in x.orders:
                    if self.checkshopbyid(x.orders[y][2])!=True:
                        x.orders[y][2]=None
            self.shops = [t for t in self.shops if t.id != id]
    def checkshopbyid(self,id):
        for x in self.shops:
            if x.id==id:
                return True
    def getshopobj(self,id):
        if self.checkshopbyid(id):
            for x in self.shops:
                if x.id==id:
                    return x
    def checkcustomerbyid(self,id):
        for x in self.customers:
            if x.id==id:
                return True
    def getcustomerobj(self,id):
        if self.checkcustomerbyid(id):
            for x in self.customers:
                if x.id==id:
                    return x
    def checkiftemplateexists(self,id):
        for x in self.templates:
            if x.id==id:
                return True            
    def checkiftemplateisused(self,name):
        if self.checktempbyname(name):
            for x in self.shops:
                for a in x.objs:
                    if a==name:
                        return True
            for x in self.customers:
                for a in x.orders:
                    if a==name:
                        return True                
    def showmenucustomers(self):
        print(f"Current number of customers:{len(self.customers)}")
        show=[]
        for x in self.customers:
            show.append(f"ID: {x.id}, Name: {x.name}, Networth: {x.nworth},",)
        print(f"Customers: {show}" )
    def showmenushops(self):
        print(f"Current number of shops:{len(self.shops)}")
        show=[]
        for x in self.shops:
            show.append(f"ID: {x.id}, Name: {x.name}, current objects: {x.objs}, Space: {x.space}",)
        print(f"Shops: {show}" )
    def printemp(self):
        if len(self.templates)>0:
            for x in self.templates:
                print(f"{x.id}) {x.name} : $ {x.price}")
        else:
            print("None")
    def checktempbyname(self,name):
        for x in self.templates:
            if x.name==name:
                return True
            
    def deletetemp(self,id):
        print(f"Template: {self.gettempdetail(id,1)} deleted")
        self.templates=[x for x in self.templates if x.id!=id]
    def get_all_shop_objects(self,sendback=False):
        data={}
        for x in self.shops:
            if x.objs:
                for key,value in x.objs.items():
                    if (f"{x.id}, Shop name:{x.name}") in data:
                        data[f"{x.id}, Shop name:{x.name}"].append([f"Item: {key}", f"Left: {value[0]}, Price: {value[1]}"])
                    else:
                        data[f"{x.id}, Shop name:{x.name}"]=[[f"Item: {key}", f"Left: {value[0]}, Price: {value[1]}"]]
        if sendback:
            return data
        else:                
            print(data)
            
    def addtemplate(self,name,price):
        l=genid()
        self.templates.append(template(name,price))
        print(f"Object {name} priced at {price} added to template with id: {l}") 
        
    def add_customer(self,name,networth):
        self.customers.append(customer(name,networth))
        print(f"Customer: {name} added with networth:{networth}")
        
    def remove_customer(self,id):
        if self.checkcustomerbyid(id):
            print(f"Customer: {self.getcustomerobj(id).name} deleted")
            self.customers=[t for t in self.customers if t.id!=id]
    def gettempdetail(self,id,detail):
        if self.checkiftemplateexists(id):
            if detail==1:
                for x in self.templates:
                    if x.id==id:
                        return x.name
            elif detail==2:
                for x in self.templates:
                    if x.id==id:
                        return x.price                                           
class shop(save):
    def __init__(self,name,space,objects=None,totalsales=None,id=None):
        if id is None:
            id=genid()
        self.id=id
        self.name=name
        self.space=space
        if objects is None:
            objects={}
        if totalsales is None:
            totalsales={}    
        self.objs=objects
        self.totalsales=totalsales
        super().__init__()   
    def checkforduplicateobjects(self,templatename,sendback=False):
        for x in system.shops:
                if x ==self:
                    continue
                if templatename in x.objs:
                    if sendback !=True:
                        print(f"Object already in {x.name} and cannot be added please chnage quanitties there or wait for it to finish")
                    return True
                
    def add_supply(self,a,b,c,d=False):
        if self.space>=b and a!="" and b!="" and c!="":
            if self.checkforduplicateobjects(a):
                    return
            if a not in self.objs:
                self.objs[a]=[b,c]
                self.space-=b
                print(f"Object: {a} added to {self.name} ,quantity {b} priced at {c} each")
                if d:
                    return True
            else:
                self.increase_quantity(a,b)
                if d:
                    return True
        else:
            print("Not enough space")
            if d:
                return False
    def remove_obj(self,a,b):
        if a in self.objs:
            if self.objs[a][0]>=b:
                if self.objs[a][0]==b:
                    self.space+=b
                    print(f" Object {a} cleared complety")
                    del self.objs[a]
                elif self.objs[a][0]>b:
                    self.objs[a][0]-=b
                    self.space+=b
                    print(f"{b} product(s) Removed from Shop: {self.name} of type {a}")                    
            else:
                print(f"You cannot remove {b} quantity from here , only quantity: {self.objs[a][0]} exists")
        else:
            print("object not found") 
    def increase_quantity(self,a,b):
        if a in self.objs:
            self.space-=b
            self.objs[a][0]+=b
            print(f"Object: {self.objs[a]} increased to {self.objs[a][0]}")

    def gen_total(self,default=True):
        if default:
            if self is not None and len(self.totalsales)!=0:
                sumi=0
                for i in self.totalsales:
                    print(f"{self.totalsales[i][0]} of Items {i} sold for {self.totalsales[i][1]*self.totalsales[i][0]}")
                    sumi+=self.totalsales[i][1]*self.totalsales[i][0]
                print(f"total revenue of:{self.name} is $ {sumi} ")    
            else:
                print(f"No Sales Happened till yet in {self.name}")
        else:
            if self is not None and len(self.totalsales)!=0:
                sumi=0
                for i in self.totalsales:
                    sumi+=self.totalsales[i][1]*self.totalsales[i][0]
                return sumi    
            else:
                return 0
    def add_to_sales(self,type,priceofobj,quantity):
        if type not in self.totalsales:
            self.totalsales[type]=[quantity, priceofobj]
        else:
            self.totalsales[type][0]+=quantity
    def del_from_sales(self,type,quantity):
        if type in self.totalsales:
            if self.totalsales[type][0]==quantity:
                del self.totalsales[type]
            else:
                self.totalsales[type][0]-=quantity
    def get_shop_items(self,sendback=False):
        cou=0
        citem={}
        for key,value in self.objs.items():
            cou+=1
            citem[cou]=[key, value[0]] 
        if sendback:
            return citem
        else:
            print(citem)
class customer(save):
    def __init__(self,name,networth,orders=None,id=None):
        if id==None:
            id=genid()
        self.id=id 
        self.name=name
        self.nworth=networth
        if orders is None:
            orders={}
        self.orders=orders
        super().__init__()
    def add_order_to_self(self,quantity,priceofobj,shopobj,type):
        if type not in self.orders:
            self.orders[type]=[quantity,priceofobj,shopobj.id]
        else:
            self.orders[type][0]+=quantity
            self.orders[type][2]=shopobj.id
    def decrease_nworth(self,c,v):
        self.nworth-=c*v          
    def order(self, sid, type, quantity):
        if system.checkshopbyid(sid):
            shopobj=system.getshopobj(sid)
            try:
                if shopobj.objs[type][0]>=quantity:
                    priceofobj=shopobj.objs[type][1]
                    if priceofobj*quantity<=self.nworth:
                        self.decrease_nworth(priceofobj,quantity)
                        self.add_order_to_self(quantity,priceofobj,shopobj,type)
                        shopobj.space+=quantity     
                        if shopobj.objs[type][0]==quantity:
                            print(f"You bought {quantity} {type}")
                            del shopobj.objs[type]
                            shopobj.add_to_sales(type,priceofobj,quantity)
                            
                        elif shopobj.objs[type][0]>quantity:
                            shopobj.objs[type][0]-=quantity
                            print(f"You bought {quantity} {type}")
                            shopobj.add_to_sales(type,priceofobj,quantity)
                    else:
                        print("Not enough funds to process the trsnsction")
                else:
                    print(f"Not enoguh quantityt of {type} only {shopobj.objs[type][0]} is left")
            except KeyError:
                print(f"Object {type} is cucrently not in {shopobj.name}")
        else:
            print(f"Shop with id:{sid} doesnt eixsts")    
    def delete_order_from_self(self,type,quantity):
        if quantity==self.orders[type][0]:
            del self.orders[type]
        elif self.orders[type][0]>quantity:
            self.orders[type][0]-=quantity
    def increase_nworth(self,c,v):
        self.nworth+=c*v
    def refund(self,type,quantity):
            if type in self.orders and self.orders[type][0]>=quantity:
                shopobj=system.getshopobj( self.orders[type][2])
                if shopobj not in system.shops:
                    print("Shop not found refund codunt be processed")
                    return 
                ref=False
                if shopobj.space>=quantity:
                        if type in shopobj.objs and shopobj.objs[type][1]==self.orders[type][1]:
                            shopobj.objs[type][0]+=quantity
                            self.increase_nworth(quantity,self.orders[type][1])
                            shopobj.space-=quantity
                            self.delete_order_from_self(type,quantity)                           
                            ref=True
                        elif type not in shopobj.objs:
                            if shopobj.add_supply(type,quantity,self.orders[type][1],True):
                                self.increase_nworth(quantity,self.orders[type][1])
                                self.delete_order_from_self(type,quantity)                           
                                ref=True               
                if ref:
                    print("Refund processed successfully")
                    shopobj.del_from_sales(type,quantity)
                else:
                    print("Please contact shop owner")
            else:
                print("You didnt buy this item " if type not in self.orders else "Not enoguh quantity")
    def printrefundableorders(self,sendback=False):
        cou=0
        citem={}
        for key,value in self.orders.items():
            if system.checkshopbyid(value[2]):
                cou+=1
                citem[cou]=[key, value[0]]
            else:
                continue          
        if sendback:
            return citem
        else:
            print(citem)
    def printviewableorders(self,sendback=False):
        data={}
        for key,value in self.orders.items():
            if system.checkshopbyid(value[2]):
                if (f"Shop name:{system.getshopobj(value[2]).name}") in data:
                    data[f"Shop name:{system.getshopobj(value[2]).name}"].append([f"Item: {key}", f"Quantity: {value[0]}, Price: {value[1]}"])
                else:
                    data[f"Shop name:{system.getshopobj(value[2]).name}"]=[[f"Item: {key}", f"Quantity: {value[0]}, Price: {value[1]}"]]
            else:
                if (f"Non refundable orders:") in data:
                    
                    data[f"Non refundable orders:"].append([f"Item: {key}", f"Quantity: {value[0]}, Price: {value[1]}"])
                else:
                    data[f"Non refundable orders:"]=[[f"Item: {key}", f"Quantity: {value[0]}, Price: {value[1]}"]]                                    
        if sendback:
            return data
        else:                
            print(data)                        
system=functions()
if autosave:
    atexit.register(system.save_all_items)
def load_data():
    with open(filename,"r") as file:
        old=json.load(file)
        for key in old:
            if key in validobjects:
                if key==validobjects[2]:
                    for y in range(len(old[key])):
                        system.customers.append(customer(old[key][y]["name"],old[key][y]["nworth"],old[key][y]["orders"],old[key][y]["id"]))
                        for z in old[key][y]["orders"]:
                            if old[key][y]["orders"][z][2]=="null":
                                old[key][y]["orders"][z][2]=None
                elif key==validobjects[0]:
                    for y in range(len(old[key])):
                        system.shops.append(shop(old[key][y]["name"],old[key][y]["space"],old[key][y]["objs"],old[key][y]["totalsales"],old[key][y]["id"]))
                elif key==validobjects[1]:
                    for y in range(len(old[key])):
                        system.templates.append(template(old[key][y]["name"],old[key][y]["price"],old[key][y]["id"]))  
if autoload:
    load_data()
    print("Persistance loaded")                                                  
Emptyerror="Input field(s) are empty"
iderror="Invlaid id Entered"
templaterror="Invalid template credentials"
noobjectspresent="The shop doesnt have any objects"
defaulterror="Invalid input"
def er(code=defaulterror):
    print(code)
while True:
    system.sort_all()
    print("Main menu\n1)Shop Managemnt\n2)Customer role\n3)Load data\n4)Save data\n5)Wipe clean data\n6)Exit ")
    try:
        n=int(input("Enter function"))
        if n==1:
            while True:
                system.showmenushops()
                print("1)Add shops\n2)Delete Shops\n3)Add Supply\n4)Remove Supply\n5)Generate revenue \n6)Add template \n7)Alter template\n8)Alter shop\n9)Return to main menu")
                try:
                    m=int(input("Enter number: "))
                    if m==1:
                        if len(system.templates)>0:
                            name=input("Enter shop name: ")
                            space=int(input("Enter maxiumum spcace: "))
                            if name!="" and space!="" and name.isalpha() and space>0: 
                                system.add_shops(name,space)
                                continue
                            else:
                                er(Emptyerror if name=="" or space=="" else defaulterror) if space>0 else er()
                                continue
                        else:
                            print("No templates")
                            continue     
                    elif m==2:
                            if len(system.shops)>0:
                                id=int(input("Enter shop id: "))
                                if id!="" and system.checkshopbyid(id):
                                    system.remove_shops(id)
                                    continue
                                else:
                                    er(iderror if id!="" else Emptyerror)
                                    continue
                            else:
                                print("No shops")
                                continue    
                    elif m==3 and len(system.shops)>0:
                        if len(system.templates)>0:
                            system.showmenushops()
                            id=int(input("Enter shop id: "))
                            if id!="" and system.checkshopbyid(id) and system.getshopobj(id).space>0:
                                if system.printaddsupplytemplates(system.getshopobj(id),True):
                                    system.printaddsupplytemplates(system.getshopobj(id),False)
                                    tid=int(input("Enter Template id: "))
                                    ob=system.getshopobj(id)
                                    print(f"Current storage left in {ob.name}: {ob.space}")
                                    quantity=int(input("Enter quantity: "))
                                    if system.checkiftemplateexists(tid) and tid !="" and quantity!="" and quantity>0:
                                        ob.add_supply(system.gettempdetail(tid,1),quantity,system.gettempdetail(tid,2))
                                        continue
                                    else:
                                        er(templaterror if tid!="" else Emptyerror)
                                        continue
                                else:
                                    print("No free template(s) add them first")            
                            else:
                                er(iderror if id=="" else "no space in the shop")
                                continue
                        else:
                            print("No templates")
                            continue    
                    elif m==4 and len(system.shops)>0:
                            data=system.get_all_shop_objects(True)
                            if len(data)>0:
                                system.showmenushops()
                                id=int(input("Enter shop id: "))
                                if id!="" and system.checkshopbyid(id) and len(system.getshopobj(id).objs)>0:
                                    ob=system.getshopobj(id)
                                    ob.get_shop_items()
                                    citem=ob.get_shop_items(True)
                                    tid=int(input("Enter Id of the Product: "))
                                    if tid in citem and tid!="":
                                        for x in citem:
                                            if x==tid:
                                                tempname=citem[x][0]
                                        quantity=int(input("Enter quantity: "))
                                        if tempname in ob.objs and quantity!="" and quantity>0:
                                            ob.remove_obj(tempname,quantity)
                                            continue
                                        else:
                                            er(templaterror if quantity!="" else Emptyerror)
                                            continue
                                    else:
                                        er(iderror if tid not in citem else Emptyerror)
                                        continue            
                                else:
                                    er(iderror if id=="" else noobjectspresent)
                                    continue
                            else:
                                print("All Shops are empty")
                                continue 
                    elif m==5 and len(system.shops)>0:
                        print("Enter id(s) of the shops to calculate revenue(s) for")
                        ids=input("Enter id of the shop: ")
                        numbers = []
                        for x in ids.split():
                            try:
                                numbers.append(int(x))
                            except ValueError:
                                continue
                        sumrevenue=0
                        con=True
                        for x in numbers:
                            if system.checkshopbyid(x)!=True:
                                con=False
                                break
                        if con:
                            for x in numbers:
                                system.getshopobj(x).gen_total()
                                sumrevenue+=system.getshopobj(x).gen_total(False)
                            print(f"Total revenue acroos all selected shop(s) {sumrevenue}")
                            continue         
                        else:
                            print("Invalid id(s) enter entered")
                            continue                 
                    elif m==6:
                        name=input("Enter name of the prodcut: ")
                        p=int(input(f"Enter price of 1 product ({name}): "))
                        if name!="" and p!="" and name.isalpha():
                            if system.checktempbyname(name)!=True:    
                                system.addtemplate(name,p)
                                continue
                            else:
                                print(f"template with name {name} already exists")
                                continue        
                        else:
                            er(Emptyerror if type(name)==str else defaulterror)
                            continue
                    elif m==7:
                            if len(system.templates)>0 and system.print_free_templates(True):
                                    system.print_free_templates()
                                    id=int(input("Enter id of the template to be altered: "))
                                    if id!="" and system.checkiftemplateexists(id):
                                        while True:
                                            for key, value in system.get_template_object(id).__dict__.items():
                                                print(f"{key}: {value}")
                                            print("What do you want to chnage?\n1)Remove this template\n2)Rename template\n3)Back")
                                            try:
                                                do=int(input("Enter function: "))
                                                if do==1:
                                                    if system.checkiftemplateisused(system.gettempdetail(id,1)):
                                                        print(f"Template: {system.gettempdetail(id,1)} is being used")
                                                        continue
                                                    else:
                                                        system.deletetemp(id)
                                                        break
                                                elif do==2:
                                                    newname=input("Enter newname of the template: ")
                                                    if newname.isalpha():
                                                        system.change_tempname(newname,id)
                                                        continue
                                                    else:
                                                        er(Emptyerror if newname=="" else defaulterror)
                                                        continue
                                                elif do==3:
                                                    break
                                                else:
                                                    er()
                                                    continue        
                                            except ValueError:
                                                er()
                                                continue
                                    else:
                                        er(iderror)
                                        continue
                            else:
                                print("no template(s) to alter")
                                continue
                    elif m==8 and len(system.shops)>0:
                        id=int(input("Enter Id of the shop: "))
                        if id!="" and system.checkshopbyid(id):
                            while True:
                                print("Shop details: ")
                                for key, value in system.getshopobj(id).__dict__.items():
                                    print(f"{key}: {value}")
                                print("1)Change name\n2)Increase space\n3)Decrease space\n4)back")
                                try:
                                    do=int(input("What to change? :"))
                                    if do==1:
                                        newname=input("Enter desired new name: ")
                                        if newname!="" and newname.isalpha():
                                                system.change_shop(newname,id,1)
                                                continue
                                        else:
                                            er(Emptyerror)
                                            continue
                                    elif do==2:
                                        print("Increase space:")
                                        newquantity=int(input("Enter quantity"))
                                        if newquantity!="" and newquantity>0:
                                            system.change_shop(newquantity,id,2)
                                            continue
                                        else:
                                            er(Emptyerror) if newquantity>0 else er()
                                    elif do==3:
                                        print("Decrease space:")
                                        newquantity=int(input("Enter quantity"))
                                        if newquantity!="" and newquantity>0:
                                            system.change_shop(newquantity,id,3)
                                            continue
                                        else:
                                            er(Emptyerror) if newquantity>0 else er()                                        
                                    elif do==4:
                                        break
                                    else:
                                        er()
                                        continue
                                except ValueError:
                                    er()
                                    continue    
                        else:
                            er(iderror if id!="" else Emptyerror)
                    elif m==9:
                        break                 
                    else:
                        er() if len(system.shops)>0 else print("No Shops")            
                except ValueError:
                        er()           
        elif n==2:
            while True:
                system.showmenucustomers()    
                print("1)Add customer\n2)Remove customer\n3)Order item\n4)refund item\n5)View orders\n6)Alter customer\n7)Back")
                try:
                    k=int(input("Enter function: "))
                    if k==1:
                        name=input("Enter Name: ")
                        networth=int(input("Enter Networth: "))
                        if name!="" and networth!="" and name.isalpha():
                            system.add_customer(name,networth)
                            continue
                        else:
                            er(Emptyerror if name=="" or networth=="" else defaulterror)
                            continue
                    if k==2 and len(system.customers)>0:
                            id=int(input("Enter id of the customer: "))
                            if id!="" and system.checkcustomerbyid(id):
                                system.remove_customer(id)
                                continue
                            else:
                                er(Emptyerror if id=="" else iderror)    
                                continue    
                    if k==3 and len(system.customers)>0:
                            data=system.get_all_shop_objects(True)
                            if len(data)>0 :                                
                                id=int(input("Enter id of the customer: "))                               
                                if id!="" and system.checkcustomerbyid(id) and system.getcustomerobj(id).nworth>0:
                                    print(f"Networth: {system.getcustomerobj(id).nworth}")
                                    system.get_all_shop_objects()
                                    am=int(input("Enter id of the shop: "))
                                    if len(system.getshopobj(am).objs)>0:
                                        if am!="" and system.checkshopbyid(am):
                                            system.getshopobj(am).get_shop_items()
                                            citem=system.getshopobj(am).get_shop_items(True)
                                            tid=int(input("Enter Object id: "))
                                            sfsd=int(input("Enter quantity: "))
                                            if tid in citem and tid !="" and sfsd!="" and sfsd>0:
                                                prodname=citem[tid][0]
                                                print(am)
                                                system.getcustomerobj(id).order(am,prodname,sfsd)
                                                continue 
                                            else:
                                                er(templaterror if tid not in citem else Emptyerror) if sfsd>0 else er()
                                                continue     
                                        else:
                                            er(Emptyerror if am=="" else iderror)
                                            continue
                                    else:
                                        print("Shop doesnt have any item")
                                        continue    
                                else:
                                    er(iderror if system.getcustomerobj(id).nworth>0 else "No funds")
                                    continue
                            else:
                                print("Nothing is out for sale" )
                                continue    
                    if k==4 and len(system.customers)>0:
                                print("Intitiate refund")
                                id=int(input("Enter id of the customer: "))                               
                                if id!="" and system.checkcustomerbyid(id) and len(system.getcustomerobj(id).orders)>0:
                                    system.getcustomerobj(id).printrefundableorders()
                                    citem=system.getcustomerobj(id).printrefundableorders(True)
                                    if len(citem)>0:
                                        tid=int(input("Enter Object id: "))
                                        sfsd=int(input("Enter quantity: "))
                                        if tid in citem and tid !="" and sfsd!="" and sfsd>0:
                                            prodname=citem[tid][0]
                                            system.getcustomerobj(id).refund(prodname,sfsd)
                                            continue 
                                        else:
                                            er(templaterror) if sfsd>0 else er()
                                            continue
                                    else:
                                        print("No item(s) are elligible for return please contact marketplace owner")
                                        continue    
                                else:
                                    er(Emptyerror if id=="" else iderror) if len(system.getcustomerobj(id).orders)>0 else print(f"{system.getcustomerobj(id).name} has'nt placed any order")
                                    continue  
                    if k==5 and len(system.customers)>0:
                                id=int(input("Enter id of the customer: "))                               
                                if id!="" and system.checkcustomerbyid(id) and len(system.getcustomerobj(id).orders)>0: 
                                        print(f"Networth: {system.getcustomerobj(id).nworth}")
                                        print(f"total objects bought: {len(system.getcustomerobj(id).orders)}")
                                        system.getcustomerobj(id).printviewableorders()
                                        continue                
                                else:
                                    er(Emptyerror if id=="" else iderror) if len(system.getcustomerobj(id).orders)>0 else print(f"{system.getcustomerobj(id).name} has'nt placed any order")
                                    continue                                
                    elif k==6 and len(system.customers)>0:
                        system.showmenucustomers()
                        id=int(input("Enter id of the customer: "))
                        if system.checkcustomerbyid(id):
                            while True:
                                print("Customer details: ")
                                for key, value in system.getcustomerobj(id).__dict__.items():
                                    print(f"{key}: {value}")
                                print("What do you want to change?\n1)Change name\n2)Add funds\n3)Withdraw funds\n4)Back")
                                try:
                                    do=int(input("Enter function: "))
                                    if do==1:
                                        newname=input("Enter new name of the customer: ")
                                        if newname.isalpha():
                                            system.change_customername(newname,id)
                                            continue
                                        else:
                                            er(Emptyerror)
                                            continue    
                                    elif do==2:
                                        print("Increase funds: ")
                                        quantity=int(input("Enter value: "))
                                        if quantity!="" and quantity>0:
                                            system.change_customerfunds(id,quantity,1)
                                            continue
                                        else:
                                            er(Emptyerror) if quantity>0 else er()
                                            continue    
                                    elif do==3:
                                        print("Withdraw funds: ")
                                        quantity=int(input("Enter value: "))
                                        if quantity!="" and quantity>0:
                                            system.change_customerfunds(id,quantity,2)
                                            continue
                                        else:
                                            er(Emptyerror) if quantity>0 else er()
                                            continue                                          
                                    elif do==4:    
                                        break
                                    else:
                                        er()
                                        continue
                                except ValueError:
                                    er()
                                    continue    
                        else:
                            er(iderror)
                            continue    
                    elif k==7:
                        break     
                    else:
                        er() if len(system.customers)>0 else print("No customers")                                                    
                except ValueError:
                    er()        
        elif n==3:
            if autoload:
                print("Already loaded")
            else:    
                load_data()
                print("Data loaded")
        elif n==4:
            if autosave:
                print("Will save on exit")
            else:    
                system.save_all_items()
        elif n==5:
            print("1)Yes\n2)no")
            warn=int(input("Are you sure?: "))
            if warn!="":
                if warn==1:
                    system.save_all_items(True)
                    continue
                elif warn==2:
                    continue 
            else:
                er()
                continue
        elif n==6:
            break        
        else:
            er()
            continue
    except ValueError:
        er()          
