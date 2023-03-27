from django.shortcuts import render, redirect,HttpResponse
from .databaseConnection import userDetails
from bson.objectid import ObjectId



import requests
from requests.auth import HTTPDigestAuth
from ipify import get_ip

atlas_group_id = "<your group ID aka project ID -- check the Project / Settings section inside Atlas>"
atlas_api_key_public = "<your atlas public API key>"
atlas_api_key_private = "<your atlas private API key>"
ip = get_ip()

resp = requests.post(
    "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
    auth=HTTPDigestAuth(atlas_api_public_key, atlas_api_private_key),
    json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]  # the comment is optional
)
if resp.status_code in (200, 201):
    print("MongoDB Atlas accessList request successful", flush=True)
else:
    print(
        "MongoDB Atlas accessList request problem: status code was {status_code}, content was {content}".format(
            status_code=resp.status_code, content=resp.content
        ),
        flush=True
    )



def home(req):
    id = req.session.get("loginID")
    userData = userDetails.find_one({'_id': ObjectId(oid=id)})
    print(userData)
    if(userData == None):
        return redirect("login")
    name = userData["name"]
    telephone = userData["telephone"]
    email = userData["email"]
    data = {"name": name, "telephone": telephone, "email": email}
    return render(req, "login/home.html", {"userData": data, "isLogged": True})


def login(req):
    id = req.session.get("loginID")
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")
        findemail = userDetails.find_one(
            {"email": email, "password": password})
        if(findemail):
            req.session["loginID"] = str(findemail["_id"])
            return redirect("home")
    return render(req, "login/login.html", {"isLogged": False})


def signup(req):
    if req.method == "POST":
        name = req.POST.get("username")
        email = req.POST.get("emailid")
        telephone = req.POST.get("telephone")
        password = req.POST.get("password")
        confirmPassword = req.POST.get("ConfirmPassword")
        if(password == confirmPassword):
            userData = {"name": name, "email": email,
                        "telephone": telephone, "password": password}
            result = userDetails.insert_one(userData)
            req.session["loginID"] = str(result.inserted_id)
            return redirect("home")

    return render(req, "login/signup.html", {"isLogged": False})


def logout(req):
    gs = req.session.get('loginID')

    if gs != None:
        del req.session['loginID']
        return redirect('login')

    return redirect('home')


def delete(req):
    gs = req.session.get('loginID')
    if gs != None:

        result = userDetails.delete_one({"_id": ObjectId(oid=gs)})
        # print(result.deleted_count, "RRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        del req.session['loginID']
        return redirect('login')
    return redirect('home')


def update(req):
    id = req.session.get('loginID')
    userId = {"_id": ObjectId(oid=id)}
    currentData = userDetails.find_one(userId)
    if(id == None):
        return redirect('login')
    if req.method == "POST":
        name = req.POST.get("username")
        telephone = req.POST.get("telephone")
        password = req.POST.get("password")
        confirmPassword = req.POST.get("ConfirmPassword")
        if password == confirmPassword:
            newData = {"$set": {"name": name,
                                "telephone": telephone, "password": password}}
            userDetails.update_one(userId, newData)
        return redirect('home')
    return render(req, "login/update.html", {"email": currentData["email"], "isLogged": True})
