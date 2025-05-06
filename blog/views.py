from django.shortcuts import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from blog.models import Post

class PostCreate(CreateView):
    model = Post
    fields = ['name', 'description', 'image']
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:post_list')

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object

class PostUpdateView(UpdateView):
    model = Post
    fields = ['name', 'description', 'image']
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs.get('pk')])

class PostDeliteViev(DeleteView):
    model = Post
    template_name = 'post_delite.html'
    success_url = reverse_lazy('blog:post_list')