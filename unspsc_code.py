import pymongo
from  flask import Flask, render_template,request,jsonify
# import pandas as pd
# import psycopg2
# import json

app = Flask(__name__)
@app.route('/')
def first():
    return render_template('first.html')

@app.route('/res',methods = ['POST', 'GET'])
def fetch():
    res = request.form['code']
    dict1={}
    dict2={}
    dict3={}
    dict4={}
    dict5={}
    dict6={}
    list1=[]
    list2=[]
    class_text=""
    family_text=""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["unspsc"]
    mycol = mydb["CE_CODE"]
    val=int(res)
    five=""
    six=""
    seven=""

    #####finding class
    ans=val/100
    class1=int(ans)*100
    ############ finding family
    ans = val / 10000
    family = int(ans) * 10000
    ########### ce_code table
    for x in mycol.find({"code":int(res)}):
        dict1.update(x)
    del dict1['_id']

    ########### ce_hsn table
    hsn_val=dict1['hsn']
    if hsn_val=="":
        five="Value not found"
        six ="Value not found"
        seven ="Value not found"
    else:
        col = mydb["CE_HSN"]
        count=0
        for x in col.find({"hsn":hsn_val}):
            if len(str(x['hsn']))>=8:
                dict4.update(x)
                count=1

        if count==0:
            digi=int(hsn_val/10000)
            for x in col.find({"hsn":digi}):
                dict4.update(x)
        del dict4['_id']
        five = dict4['hsn']
        six = dict4['text']
        seven = dict4['tax']

    ####### ce_attr table
    codenm = dict1['codenm']
    attr = mydb["CE_ATTR"]
    s=attr.find({"codenm": codenm})
    cou=s.count()
    for x in attr.find({"codenm": codenm}):
        list1.append(x['text'])
        dict6.update(x)
    #del dict6['_id']



    mycol = mydb["CE_CODE"]
    for x in mycol.find({"code": class1}):
        class_text=x['text']
    for x in mycol.find({"code": family}):
        family_text = x['text']

    one=dict1['code']
    two = dict1['text']
    three=class_text
    four=family_text
    # if dict4['hsn']=="":
    #     five="None"
    # else:
    #     five = dict4['hsn']
    # if dict4['text']=="":
    #     six="None"
    # else:
    #     six = dict4['text']
    # if dict4['tax']=="":
    #     seven="None"
    # else:
    #     seven = dict4['tax']
    for i in list1:
        if i not in list2:
            list2.append(i)

    if len(list2)==0:
        list2.append("value_not_found")
    resdict={
        "1_code":one,
        "2_text":two,
        "3_class":three,
        "4_family":four,
        "5_hsncode":five,
        "6_hsntext":six,
        "7_tax":seven,
        "8_text_attribute":list2
    }
    y=jsonify(resdict)
    return y


@app.errorhandler(500)
def internal_error(error):

    return "The entered code has no HSN Value"

@app.errorhandler(404)
def not_found(error):
    return "404 error",404



if __name__ == '__main__':
    app.run(debug=True, port=8000)
