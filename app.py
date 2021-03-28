import pymongo
from  flask import Flask, render_template,request,jsonify,json
import base64

app = Flask(__name__)

list1=[]
data = {}

@app.route('/')
def display():
    return render_template('json_image.html')


@app.route('/uuu',methods = ['POST', 'GET'])
def fetch():
    data.clear()
    res = request.form['code']
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["unspsc_images"]
    mycol = mydb["image_store"]
    list1.clear()
    val = int(res)
    for x in mycol.find({"code": str(val)}):
        first=x['imgpath']
        list1.append(first)
    # print(list1)
    length=len(list1)
    # print(length)
    for i in range(0, length):
        resstr = "C:\\Users\\80246\\Desktop\\images_unspsc\\" + str(list1[i])
        z=open(resstr, mode='rb')
        ima = z.read()
        y="img"+str(i)
        #data[y] = base64.encodebytes(ima).decode('utf-8')
        data[y]=base64.b64encode(ima).decode('utf-8')
    return jsonify(data)



if __name__ == '__main__':
    app.run()
