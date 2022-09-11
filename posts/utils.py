import calendar

def calculate_month(post, previous_post):
    if post.sent is None:
        post.sent = post.sent_all - previous_post.sent_all
    else:
        post.sent_all = post.sent + previous_post.sent_all
    
    if post.received is None:
        post.received = post.received_all - previous_post.received_all
    else:
        post.received_all = post.received + previous_post.received_all

    if post.produced is None:
        post.produced = post.produced_all - previous_post.produced_all
    else:
        post.produced_all = post.produced + previous_post.produced_all
    
    post.autoconsumption = post.produced - post.sent
    post.autoconsumption_percentage = round((post.produced - post.sent) / post.produced, 2)
    post.consumption = post.produced + post.received - post.sent
    post.consumption_average = round((post.produced + post.received - post.sent) / calendar.monthrange(post.date.year, post.date.month)[1], 2)