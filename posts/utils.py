import calendar

def calculate_month(post, previous_post):
    post.sent = post.sent_all - previous_post.sent_all
    post.received = post.received_all - previous_post.received_all
    post.produced = post.produced_all - previous_post.produced_all
    post.autoconsumption = post.produced - post.sent
    post.autoconsumption_percentage = (post.produced - post.sent) / post.produced
    post.consumption = post.produced + post.received - post.sent
    post.consumption_average = round((post.produced + post.received - post.sent) / calendar.monthrange(post.date.year, post.date.month)[1], 2)