from django.shortcuts import render, redirect
from .models import ShoppingItem,Category,ColorTag,Comment,Company
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

class ShoppingItemList(ListView):
    model = ShoppingItem
    ordering = '-pk'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingItemList, self).get_context_data() ##템플릿에서 필요한 거 담아서 전달
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = ShoppingItem.objects.filter(category=None).count
        return context

class ShoppingItemDetail(DetailView):
    model = ShoppingItem

    def get_context_data(self, **kwargs):
        context = super(ShoppingItemDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = ShoppingItem.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

class ShoppingItemSearch(ShoppingItemList):
    paginate_by = None
    def get_queryset(self):
        q = self.kwargs['q']
        shoppingitem_list = ShoppingItem.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()

        return shoppingitem_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingItemSearch,self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'
        return context



def category_page(request,slug):
    if slug=='no_category':
        category ='미분류'
        ShoppingItemList = ShoppingItem.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        ShoppingItemList =  ShoppingItem.objects.filter(category=category)

    return render(
        request,
        'shoppingmall_main/shoppingitem_list.html',{
            'category' :category,
            'shoppingitem_list' : ShoppingItemList,
            'categories': Category.objects.all(),
            'no_category_post_count': ShoppingItem.objects.filter(category=None).count(),
        }
    )

def company_page(request,slug):

    m_company = Company.objects.get(slug=slug)
    ShoppingItemList = ShoppingItem.objects.filter(m_company=m_company)

    return render(
        request,
        'shoppingmall_main/shoppingitem_list.html',{
            'company' :m_company,
            'shoppingitem_list' : ShoppingItemList,
            'companies': Company.objects.all(),
            'no_category_post_count': ShoppingItem.objects.filter(m_company=None).count(),
        }
    )


def tag_page(request, slug):
    tag = ColorTag.objects.get(slug=slug)
    shoppingitem_list = tag.shoppingitem_set.all()

    return render(request, 'shoppingmall_main/shoppingitem_list.html', {
        'tag' : tag,
        'shoppingitem_list' : shoppingitem_list,
        'categories': Category.objects.all(),
        'no_category_post_count': ShoppingItem.objects.filter(category=None).count

    })

class ShoppingItemUpdate(UpdateView):
    model = ShoppingItem
    fields = ['title', 'information', 'price', 'head_image', 'm_company', 'category','product_number'] #,'tags'

    template_name = 'shoppingmall_main/shoppingitem_update_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ShoppingItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ShoppingItemUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')  # , -> ;로 바꿔준다
            tags_list = tags_str.split(';')  # ;를 기준으로 단어 나누기
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = ColorTag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingItemUpdate, self).get_context_data() ##템플릿에서 필요한 거 담아서 전달
        if self.object.tags.exists():
            tags_str_list = list() #빈 리스트 생성
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = ShoppingItem.objects.filter(category=None).count
        return context

class ShoppingItemCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=ShoppingItem
    fields = ['title', 'information', 'price', 'head_image', 'm_company', 'category','product_number'] #, 'tags'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user #form의 author값을 현재 로그인된 값으로 설정해줌
            response = super(ShoppingItemCreate,self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str :
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';') #, -> ;로 바꿔준다
                tags_list = tags_str.split(';') #;를 기준으로 단어 나누기
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = ColorTag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shoppingmall_main/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingItemCreate, self).get_context_data() ##템플릿에서 필요한 거 담아서 전달
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = ShoppingItem.objects.filter(category=None).count
        return context

def new_comment(request,pk):
    if request.user.is_authenticated:
        shoppingitem=get_object_or_404(ShoppingItem,pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.shoppingitem = shoppingitem
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(shoppingitem.get_absolute_url())
        else:
            raise PermissionDenied

class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    shoppingitem = comment.shoppingitem
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(shoppingitem.get_absolute_url())
    else:
        raise PermissionDenied