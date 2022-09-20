from .serializers import PostSerializer


def prepare_posts(posts):
    months = posts.dates('date', 'month')
    sorted_posts = {}
    for month in months:
        sorted_posts[month.month] = PostSerializer(posts.get(date__month=month.month)).data
    return sorted_posts

