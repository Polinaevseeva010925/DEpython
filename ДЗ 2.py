from datetime import datetime

the_moscow_times = "Wednesday, October 2, 2002"
the_guardian = "Friday, 11.10.13"
daily_news = "Thursday, 18 August 1977"
moscow_times_date = datetime.strptime(the_moscow_times, "%A, %B %d, %Y")
guardian_date = datetime.strptime(the_guardian, "%A, %d.%m.%y")
daily_news_date = datetime.strptime(daily_news, "%A, %d %B %Y")
print("The Moscow Times:", moscow_times_date)
print("The Guardian:", guardian_date)
print("Daily News:", daily_news_date)