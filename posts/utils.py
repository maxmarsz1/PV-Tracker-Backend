import calendar
from dateutil.relativedelta import relativedelta

def calculate_month(post, user_posts, Post):
    energy_sent_back = 0.7 if post.user.userconfig.pv_power > 10 else 0.8

    try:
        previous_post_date = post.date - relativedelta(months=1)
        previous_post = user_posts.get(date__month=previous_post_date.month, date__year=previous_post_date.year)

        # Setting required data based on previous month
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
    
    # If there is no post in previous month we calculate based only on this month
    except Post.DoesNotExist:
        if post.produced_all is None:
            post.produced_all = post.produced + post.user.userconfig.produced_start
        else:
            post.produced = post.produced_all - post.user.userconfig.produced_start

        if post.received_all is None:
            post.received_all = post.received + post.user.userconfig.received_start
        else:
            post.received = post.received_all -  post.user.userconfig.received_start

        if post.sent_all is None:
            post.sent_all = post.sent + post.user.userconfig.sent_start
        else:
            post.sent = post.sent_all - post.user.userconfig.sent_start


    # Gettting posts from one year back to calculate energy surplus
    # Current post isn't included because it could be edited thus it might differ
    date_year_back = post.date + relativedelta(years=-1, months=+1)
    year_back_posts = user_posts.filter(date__range=[date_year_back, previous_post_date])
    
    # Calculations
    post.autoconsumption = post.produced - post.sent
    post.autoconsumption_percentage = round(post.autoconsumption / post.produced, 2)
    post.consumption = post.produced + post.received - post.sent
    post.consumption_average = round(post.consumption / calendar.monthrange(post.date.year, post.date.month)[1], 2)

    post.energy_surplus = sum([(post.sent * energy_sent_back) - post.received for post in year_back_posts])
    
    # Manualy adding current post data
    post.energy_surplus += (post.sent * energy_sent_back) - post.received
    post.energy_surplus = round(post.energy_surplus, 2)

    post.energy_surplus_cash = round(post.energy_surplus * post.user.userconfig.energy_buy_price, 2)
