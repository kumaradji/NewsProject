# from django.contrib.auth.models import User
from news_portal.news.models import *
# from django.db.models import Sum

u1 = User.objects.create_user('u1')
u2 = User.objects.create_user('u2')
a1 = Author.objects.create(authorUser=u1)
a2 = Author.objects.create(authorUser=u2)

c1 = Category.objects.create(name='c1')
c2 = Category.objects.create(name='c2')
c3 = Category.objects.create(name='c3')
c4 = Category.objects.create(name='c4')

p1 = Post.objects.create(author=a2, title='Вредные советы 1',
                         text='Все начинающие мастера пытаются красить краснокочанной капустой и после восторга '
                              'обычно к ним приходит разочарование. Мастерство в любом деле приходит с опытом!')

p2 = Post.objects.create(author=a2, title='Вредные советы 2',
                         text='Представляете вы дарите свой шедевр близкому человеку или продаёте, а ваше изделие при '
                              'первой стирке линяет! Не приятно, правда! Краснокочанная капуста, ежевика, черника, '
                              'виноград и тд. содержат в себе краситель антоциан. Красители, которые подходят для '
                              'кулинарных изделий, обычно для ткани не подходят!')

n1 = Post.objects.create(author=a1, categoryType='AR', title='Вредные советы 3',
                         text='Да, да, растения свои удивительные цвета, танины и всё, что нужно для крашения, '
                              'использует для себя! И поэтому перед тем, как вы задумаете окрашивать ткани. Если '
                              'присутствуют танины, органические кислоты, дубильные вещества — смело можете '
                              'приступать к работе, но предварительно сделайте образец и всё хорошенько обдумайте.')

pc1 = PostCategory.objects.create(post=p1, category=c1)
pc2 = PostCategory.objects.create(post=p1, category=c2)

pc3 = PostCategory.objects.create(post=p2, category=c2)
pc4 = PostCategory.objects.create(post=p2, category=c4)

pc5 = PostCategory.objects.create(post=n1, category=c2)
pc6 = PostCategory.objects.create(post=n1, category=c3)

co1 = Comment.objects.create(user=u1, post=p1, text='о сколько нам')
co2 = Comment.objects.create(user=u2, post=p2, text='открытий чудных')
co3 = Comment.objects.create(user=u1, post=n1, text='готовит просвещенья дух')
co4 = Comment.objects.create(user=u2, post=p1, text='и опыт сын ошибок трудных и гений парадоксов друг')

co1.like()
p1.dislike()
p2.like()
p1.like()
n1.like()
co2.dislike()
co3.like()
co4.like()

a1.update_rating()
a2.update_rating()

a = Author.objects.order_by('-rating')[0]
print(f'Автор: {a.user.username}, рейтинг: {a.rating}')

p = Post.objects.filter(isnews=False).order_by('-rating')[0]

print(
    f'Дата: {p.created}, Автор: {p.author.user.username}, Рейтинг: {p.rating}, Заголовок: {p.title}, Превью: {p.preview()}')

for c in Comment.objects.filter(post_id=p.id):
    print(f'Дата: {c.created}, Автор: {c.user.username}, Рейтинг: {c.rating}, Текст: {c.text}\r\n')
