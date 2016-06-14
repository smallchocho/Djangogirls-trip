# trips/views.py
from django.shortcuts import redirect
from datetime import datetime
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.db import models
def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': datetime.now(),
    })
def home(request):
    post_list = Post.objects.all()
    return render(request,'home.html',{'post_list':post_list})
def post_detail(request,pk):
    post = Post.objects.get(pk = pk)
    return render(request,'post_detail.html',{'post':post})
def post_new(request):
    if request.method == "POST":
        #檢查request.method是否已經被存入資料，然後透過下面這行把資料都丟入ＰostFrom格式裡頭#
        post_form = PostForm(request.POST)
        #PostForm是我們在froms.py設立的類別，是一個用來寫新ＰＯ文或修改ＰＯ文的表單#
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.created_at = models.DateTimeField(auto_now_add=True)
            post.save()
            return redirect('trips.views.post_detail', pk=post.pk)
    else:
        post_form = PostForm()
    return render(request,'post_edit.html',{'post_form': post_form })
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        #只有進入過blog/post_edit.html，才可能滿足這個條件#
        post_form = PostForm(request.POST,instance=post)#instance是什麼意思？#
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.published_date = models.DateTimeField(auto_now_add=True)
            post.save()
            return redirect('trips.views.post_detail', pk=post.pk)
    else:
        post_form = PostForm(instance=post)#將舊資料插入PostForm中#
    return render(request, 'post_edit.html', {'post_form': post_form})
