from app.models import Post,userImage,Product,User
from flask_login import current_user, login_required
from app.extensions import db
import json
from datetime import datetime

def parseList(data,date,user):
    plist1 = []
    plist2 = []
    key1 = data[0].split(" ",1)
    key2 = data[1].split(" ",1)
    purchase_date = date
    for value in data[2:]:
        item = {}
        value=value.split(" ", 1)
        if len(value)==2:
            item[key1[0]] = value[0]
            item[key1[1]]= value[1]
            plist1.append(item)
        elif len(value)==1:
            item[key2[0]] = value[0].split('$')[1]
            plist2.append(item)
    
    plist = []
    for i in range(0,len(plist2)):
        item = {}
        item['Product'] = plist1[i]['Product']
        item['Qty'] = plist1[i]['Qty']
        item['Total'] = plist2[i]['Total']
        item['Date'] = str(purchase_date)
        plist.append(item)
        prod = Product(name=item['Product'],price=(item['Total']),quantity=float(item['Qty']),productname=user)
        db.session.add(prod)
        db.session.commit()
        print("sucessfully commited to db")
    return json.dumps(plist)


def getData():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        uimages = userImage.query.filter_by(timage=user).order_by(userImage.imageDate.desc())
        data = []
        for value in uimages:
            tempVal = value.serialize()
            if 'Lotus Market Mesa' in tempVal['content']:
                val = tempVal['content']
                val = val.split("\n")
                count = 0
                start=0
                end=0
                date = 0
                for tval in val:
                    if 'Qty Product' in tval:
                        start = count
                    elif 'Date:' in tval:
                        date = count
                    elif 'Total:' in tval:
                        end=count
                        break
                    count=count+1
                purch = val[date+1]
                val = val[start:end]
                val = parseList(val,purch,user)
                data.append(val)
        return str(data)