from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from .models import Box
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,QueryDict
from mystore.forms import LoginForm
from django.contrib.auth import authenticate, login
import json
from django.contrib.auth.decorators import login_required

class BoxView(View):
    def check_conditions(self,avg_area,avg_vol):
        check = False
        if avg_area > 100:
            check = True
        if avg_vol >1000:
            check = True
        import datetime
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        if len(Box.objects.filter(created_on__gte=start_week))>100:
            check = True
        return check
    def get_box_data(self,box_data,is_staff):
        res = []
        if is_staff:
            for box in box_data:
                res.append({
                    'Length': box.length,
                    'Width': box.width,
                    'Height': box.height,
                    'Area': 2 * (box.length * box.height + box.length * box.width + box.width * box.height),
                    'Volume': box.length * box.height * box.width,
                    'Created By': str(box.created_by),
                    'Updated By': str(box.updated_by)
                })
        else:
            for box in box_data:
                res.append({
                    'Length':box.length,
                    'Width':box.width,
                    'Height':box.height,
                    'Area':2*(box.length*box.height+box.length*box.width+box.width*box.height),
                    'Volume':box.length*box.height*box.width,
                })
        return res


    def avg_area(self,box_obj,avg_area):
        for box in box_obj:
            avg_area = avg_area + (2*(box.length*box.height+box.length*box.width+box.width*box.height))
        return avg_area/(len(box_obj)+1)

    def avg_volume(selfself,box_obj,avg_vol):
        for box in box_obj:
            avg_vol = avg_vol + (box.length*box.height*box.width)
        return avg_vol/(len(box_obj)+1)

    def login(self,request):
        from django.contrib.auth import authenticate, login
        username = 'matumba'
        password = 'msdhoni78'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

    def get(self,request):
        box_data = Box.objects.all()
        res = []
        response = self.get_box_data(box_data,request.user.is_staff)
        return HttpResponse(json.dumps(response),content_type='application/json',status=200)

    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('login requried to create box',status=401)
        else:
            try:
                User.objects.get(pk=request.user.id,is_staff=True)
            except ObjectDoesNotExist:
                return HttpResponse('user is not a staff')
            length = request.POST['length']
            width = request.POST['width']
            height = request.POST['height']
            box_data = Box.objects.all()
            curr_area = 2*(int(length)*int(width)+int(length)*int(height)+int(width)*int(height))
            curr_vol = int(length)*int(width)*int(height)
            avg_area = self.avg_area(box_data,curr_area)
            avg_vol = self.avg_volume(box_data,curr_vol)
            check = self.check_conditions(avg_area,avg_vol)
            if not check:
                box_data = Box(length=length,width=width,height=height,created_by_id=request.user.pk,updated_by_id=request.user.pk)
                box_data.save()
                return HttpResponse('box created',status=201)
            else:
                return HttpResponse('condition not fulfilled')

    def put(self,request,box_id):
        if not request.user.is_authenticated():
            return HttpResponse('login requried to update a box',status=401)
        try:
            User.objects.get(pk=request.user.id, is_staff=True)
        except ObjectDoesNotExist:
            return HttpResponse('user is not a staff')

        data = QueryDict(request.body)
        try:
            box_object = Box.objects.get(pk=box_id,is_deleted=False)
        except ObjectDoesNotExist:
            return HttpResponse('invalid box id')
        box_object.width = data['width']
        box_object.height = data['height']
        box_object.length = data['length']
        box_object.updated_by_id = request.user.pk
        box_data = Box.objects.all()
        curr_area = 2 * (int(box_object.length) * int(box_object.width) + int(box_object.length) * int(box_object.height) + int(box_object.width) * int(box_object.height))
        curr_vol = int(box_object.length) * int(box_object.width) * int(box_object.height)
        avg_area = self.avg_area(box_data, curr_area)
        avg_vol = self.avg_volume(box_data, curr_vol)
        check = self.check_conditions(avg_area, avg_vol)
        if not check:
            box_object.save()
            return HttpResponse('box updated successfully')
        else:
            return HttpResponse('condition not fulfilled')
    def box_filter(self,length=None,width=None,height=None,area=None,volume=None,created_by=None,date=None,is_greater=None):
        if is_greater != None:
            if length:
                return Box.objects.filter(length__gte=length)
            if width:
                return Box.objects.filter(width__gte=width)
            if height:
                return Box.objects.filter(height__gte=height)
            if area:
                return Box.objects.filter(area__gte=area)
            if volume:
                return Box.objects.filter(voulume__gte=volume)
            if created_by:
                return Box.objects.filter(created_by=created_by)
            if date:
                return Box.objects.filter(date__gte=date)
        else:
            if length:
                return Box.objects.filter(length__lte=length)
            if width:
                return Box.objects.filter(width__lte=width)
            if height:
                return Box.objects.filter(height__lte=height)
            if area:
                return Box.objects.filter(area__lte=area)
            if volume:
                return Box.objects.filter(voulume__lte=volume)
            if created_by:
                return Box.objects.filter(created_by=created_by)
            if date:
                return Box.objects.filter(date__lte=date)


class DetailView(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('login requried to fetch user box')
        user = request.user
        if user.is_staff:
            box_data = Box.objects.filter(created_by_id=user.pk)
            get_box = BoxView()
            response = get_box.get_box_data(box_data,user.is_staff)
            if response:
                return HttpResponse(json.dumps(response),content_type='application/json',status=200)
            else:
                return  HttpResponse('no box found for the given user')
        else:
            return HttpResponse('user is not a staff')

    def put(self,request,box_id):
        if not request.user.is_authenticated():
            return HttpResponse('login requried to delete a box')
        try:
            box_data = Box.objects.get(pk=box_id,created_by_id=request.user.pk)
        except ObjectDoesNotExist:
            return HttpResponse('only creator can delete')
        box_data.is_deleted = True
        box_data.save()
        return HttpResponse('box deleted successfully')

class LoginView(View):
    def post(self,request):
        user = request.POST['username']
        password = request.POST['password']
        from django.contrib.auth import authenticate, login
        user = authenticate(username=user, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('login success',status=200)
        else:
            return HttpResponse('invalid credentials')






