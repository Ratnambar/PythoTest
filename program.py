# first Program

l=[]

def add():
    for i in range(int(input())):
        l.append(int(input()))
    return sum(l)
add()



#second program

Dict2= {"1" : 50,"2" : 60,"3" : 70}

def Max_in_Dict(Dict2):
    max=0
    d=dict()
    for k,v in Dict2.items():
        if v>max:
            max=v
            key = k
    d[key]=max
    return d

Max_in_Dict(Dict2)
    

#third program

l = [0,0,0,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,1]
def count_max_one(l):
    count=0
    max=0
    for i in range(len(l)):
        if l[i]==1:
            count+=1
            if count>max:
                max=count
        else:
            count=0
    return max

count_max_one(l)   



#fourth program in sql

 create table user(
    -> user_id int not null auto_increment,
    -> username varchar(100) not null,
    -> password varchar(50) not null,
    -> primary key(user_id));

 
 table address
 
 create table addresses( id int not null auto_increment, user_id int, street varchar(100) not null, pincode int(20) not null, country varchar(50) not null, state varchar(50) not null, phone varchar(20) not null, primary key(id), foreign key (user_id) references user(user_id) );
