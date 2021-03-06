#-*- coding: cp949 -*-
from apps.log.models import *
from apps.account.models import *

from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models import Q

#하루 로그 
def postDayLog():
    #시간별로 데이터를 쌓기 위해서 시간 분기
    today_=datetime.datetime.today()
    h=24
    if today_.hour ==0:
        h=24
    elif today_.hour <=6 :
        h=6
    elif today_.hour <=12 :
        h=12
    elif today_.hour <=18 :
        h=18

    #데이터가 오전 12시 기준으로 6시간 마다 쌓인다.
    new_date = today_ + relativedelta(hours=-h)
    access_cnt =len(AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)))
    access_log =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    access_real_cnt = len(access_log)
    search = SearchText.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    search_cnt = len(search)
    search_user_cnt = len(search.values('ip').order_by().distinct())
    cnt = 0
    for i in search:
        if i.count>=3:
            cnt+=1

    search_success_cnt = round((cnt/search_cnt)*100,2)

    signup_cnt =len(User.objects.filter(date_joined__gte=str(new_date)).filter(date_joined__lte=str(today_)).order_by('id').distinct())
    login_cnt =len(LoginLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct())
    click_cnt =len(clickLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)))

    bounce_cnt=0
    user_log =UserLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    user_log_cnt =len(UserLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)))
    d = user_log_cnt
    n = user_log_cnt 
    three_cnt = 0
    five_cnt = 0
    ten_cnt = 0
    for i in user_log:
        n+=i.visit_cnt
        if i.bounce_rate==True:
            bounce_cnt+=1
        if i.day_cnt >= 10:
            ten_cnt+=1
        if i.day_cnt >= 5:
            five_cnt+=1
        if i.day_cnt >= 3:
            three_cnt+=1
        if i.day_cnt >= 2:
            two_cnt+=1
    access_all =DayLog.objects.filter(created_at__gte=str(new_date+relativedelta(hours=-1))).filter(created_at__lte=str(new_date+relativedelta(hours=+2)))
    access_all_cnt=access_all[0].access_all_cnt
    access_all_two=access_all[0].two_cnt
    access_all_three=access_all[0].three_cnt
    access_all_five=access_all[0].five_cnt
    access_all_ten=access_all[0].ten_cnt
    two_per = (two_cnt+access_all_two)/(access_real_cnt+access_all_cnt) * 100
    print(two_cnt,'+',access_all_two,'/',access_real_cnt,'+',access_all_cnt)
    three_per = (three_cnt+access_all_three)/(access_real_cnt+access_all_cnt) * 100
    print(three_cnt,'+',access_all_three,'/',access_real_cnt,'+',access_all_cnt)
    five_per = (five_cnt+access_all_five)/(access_real_cnt+access_all_cnt) * 100
    print(five_cnt,'+',access_all_five,'/',access_real_cnt,'+',access_all_cnt)
    ten_per = (ten_cnt+access_all_ten)/(access_real_cnt+access_all_cnt) * 100
    print(ten_cnt,'+',access_all_ten,'/',access_real_cnt,'+',access_all_cnt)

    if h==24:
        two_cnt += access_all_two
        three_cnt += access_all_three
        five_cnt += access_all_five
        ten_cnt += access_all_ten
        access_all_cnt += access_real_cnt

    bounce_rate = round((bounce_cnt/user_log_cnt)*100,2)
    pv = round((n/d),2)

    revisit_cnt=0
    for i in access_log:
        x = AccessLog.objects.filter(ip=i['ip'])
        for j in range(len(x)-1):
            if x[j].created_at+relativedelta(months=-1) > x[j+1].created_at:
                revisit_cnt+=1
                break

    revisit_cnt_week=0
    for i in access_log:
        x = AccessLog.objects.filter(ip=i['ip'])
        for j in range(len(x)-1):
            if x[j].created_at+relativedelta(days=-7) > x[j+1].created_at:
                revisit_cnt_week+=1
                break

    revisit_cnt_day=0
    for i in access_log:
        x = AccessLog.objects.filter(ip=i['ip'])
        for j in range(len(x)-1):
            if x[j].created_at+relativedelta(days=-1) > x[j+1].created_at:
                revisit_cnt_day+=1
                break

    x = AccessLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    first_visit_cnt=0
    for i in access_log:
        if len(x.filter(ip=i['ip'])) == 0:
            first_visit_cnt+=1


    DayLog.objects.create(
        access_cnt=access_cnt,
        access_real_cnt=access_real_cnt,
        search_cnt=search_cnt,
        search_user_cnt=search_user_cnt,
        search_success_cnt=search_success_cnt,
        first_visit_cnt=first_visit_cnt,
        signup_cnt=signup_cnt,
        login_cnt=login_cnt,
        click_cnt=click_cnt,
        revisit_cnt=revisit_cnt,
        revisit_cnt_week=revisit_cnt_week,
        revisit_cnt_day=revisit_cnt_day,
        three_cnt=three_cnt,
        two_cnt=two_cnt,
        five_cnt=five_cnt,
        ten_cnt=ten_cnt,
        two_per=two_per,
        three_per=three_per,
        five_per=five_per,
        ten_per=ten_per,
        pv_rate = pv,
        bounce_rate=bounce_rate,
        access_all_cnt=access_all_cnt
        )

#재방문자 기준 로그
def postDayOldVisiterLog():
    today_=datetime.datetime.today()
    h=24
    if today_.hour ==0:
        h=24
    elif today_.hour <=6 :
        h=6
    elif today_.hour <=12 :
        h=12
    elif today_.hour <=18 :
        h=18

    # 현재 기준 자정
    new_date = today_ + relativedelta(hours=-h)
    
    # 유입 숫자
    total =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip')
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    access_cnt=0
    for i in total:
        if len(x.filter(ip=i['ip'])) != 0:
            access_cnt+=1

    # 실 유입 숫자
    real_total =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    access_real_cnt=0
    for i in real_total:
        if len(x.filter(ip=i['ip'])) != 0:
            access_real_cnt+=1
    

    # 검색 카운트
    search_total = SearchText.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    search_cnt=0
    for i in search_total:
        if len(x.filter(ip=i['ip'])) != 0:
            search_cnt+=1

    # 검색 유저 카운트
    search_user_total = SearchText.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    search_user_cnt=0
    for i in search_user_total:
        if len(x.filter(ip=i['ip'])) != 0:
            search_user_cnt+=1


    # 로그인 카운트
    login_total =LoginLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    login_cnt=0
    for i in login_total:
        if len(x.filter(ip=i['ip'])) != 0:
            login_cnt+=1

    # 클릭 카운트
    click_total =clickLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip')
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    click_cnt=0
    for i in click_total:
        if len(x.filter(ip=i['ip'])) != 0:
            click_cnt+=1

    # 이탈율 카운트
    user_out_total =UserLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    bounce_cnt = 0
    user_log_cnt = 0
    n=0
    for i in user_out_total:
        if len(x.filter(ip=i['ip'])) != 0:
            user_log_cnt+=1
            n+=i['visit_cnt']
            if i['bounce_rate']==True:
                bounce_cnt+=1
    bounce_rate = round((bounce_cnt/user_log_cnt)*100,2)
    pv = round(((n+user_log_cnt)/user_log_cnt),2)

    #검색 성공률
    count = 0
    search_cnt_d = 0
    for i in search_total:
        if len(x.filter(ip=i['ip'])) != 0:
            search_cnt_d +=1
            if i['count']>=3:
                count+=1
               
    search_success_cnt = round((count/search_cnt_d)*100,2)
   
    revisit_cnt=0
    for i in real_total:
        x = AccessLog.objects.filter(ip=i['ip'])
        for j in range(len(x)-1):
            if x[j].created_at+relativedelta(months=-1) > x[j+1].created_at:
                revisit_cnt+=1
                break

    revisit_cnt_week=0
    for i in real_total:
        x = AccessLog.objects.filter(ip=i['ip'])
        for j in range(len(x)-1):
            if x[j].created_at+relativedelta(days=-7) > x[j+1].created_at:
                revisit_cnt_week+=1
                break

    revisit_cnt_day=0
    for i in real_total:
        x = AccessLog.objects.filter(ip=i['ip'])
        for j in range(len(x)-1):
            if x[j].created_at+relativedelta(days=-1) > x[j+1].created_at:
                revisit_cnt_day+=1
                break


    DayLogOldVisiter.objects.create(
        access_cnt=access_cnt,
        access_real_cnt=access_real_cnt,
        search_cnt=search_cnt,
        search_user_cnt=search_user_cnt,
        search_success_cnt=search_success_cnt,
        login_cnt=login_cnt,
        click_cnt=click_cnt,
        pv_rate=pv,
        revisit_cnt=revisit_cnt,
        revisit_cnt_week=revisit_cnt_week,
        revisit_cnt_day=revisit_cnt_day,
        bounce_rate=bounce_rate
        )

#신규 방문자 기준 로그
def postDayNewVisiterLog():
    today_=datetime.datetime.today()
    h=24
    if today_.hour ==0:
        h=24
    elif today_.hour <=6 :
        h=6
    elif today_.hour <=12 :
        h=12
    elif today_.hour <=18 :
        h=18

    # 현재 기준 자정
    new_date = today_ + relativedelta(hours=-h)
    
    # 유입 숫자
    total =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip')
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    access_cnt=0
    for i in total:
        if len(x.filter(ip=i['ip'])) == 0:
            access_cnt+=1

    # 실 유입 숫자
    real_total =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    access_real_cnt=0
    for i in real_total:
        if len(x.filter(ip=i['ip'])) == 0:
            access_real_cnt+=1
    

    # 검색 카운트
    search_total = SearchText.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    search_cnt=0
    for i in search_total:
        if len(x.filter(ip=i['ip'])) == 0:
            search_cnt+=1

    # 검색 유저 카운트
    search_user_total = SearchText.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    search_user_cnt=0
    for i in search_user_total:
        if len(x.filter(ip=i['ip'])) == 0:
            search_user_cnt+=1


    # 로그인 카운트
    login_total =LoginLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    login_cnt=0
    for i in login_total:
        if len(x.filter(ip=i['ip'])) == 0:
            login_cnt+=1

    # 클릭 카운트
    click_total =clickLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip')
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    click_cnt=0
    for i in click_total:
        if len(x.filter(ip=i['ip'])) == 0:
            click_cnt+=1

    # 이탈율 카운트
    user_out_total =UserLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values()
    x = UserLog.objects.filter(created_at__lte=str(new_date)).values('ip').order_by().distinct()
    bounce_cnt = 0
    user_log_cnt = 0
    n=0
    for i in user_out_total:
        if len(x.filter(ip=i['ip'])) == 0:
            user_log_cnt+=1
            n+=i['visit_cnt']
            if i['bounce_rate']==True:
                bounce_cnt+=1
    bounce_rate = round((bounce_cnt/user_log_cnt)*100,2)
    pv = round(((n+user_log_cnt)/user_log_cnt),2)

    #검색 성공률
    count = 0
    search_cnt_d = 0
    for i in search_total:
        if len(x.filter(ip=i['ip'])) == 0:
            search_cnt_d +=1
            if i['count']>=3:
                count+=1
               
    search_success_cnt = round((count/search_cnt_d)*100,2)


    DayLogNewVisiter.objects.create(
        access_cnt=access_cnt,
        access_real_cnt=access_real_cnt,
        search_cnt=search_cnt,
        search_user_cnt=search_user_cnt,
        pv_rate=pv,
        search_success_cnt=search_success_cnt,
        login_cnt=login_cnt,
        click_cnt=click_cnt,
        bounce_rate=bounce_rate
        )


#사용자 기준 로그
def postUserLog():

    #시간별로 데이터를 쌓기 위해서 시간 분기
    #사용자 기준 로그를 바탕으로 하루기준 로그가 생성됨. 크론 설정을 보면 사용자 기준 로그가 먼저 쌓임. settings에 있음 맨밑
    today_=datetime.datetime.today()
    h=24
    if today_.hour ==23:
        h=24
    elif today_.hour <=5 :
        h=6
    elif today_.hour <=11 :
        h=12
    elif today_.hour <=17 :
        h=18
    new_date = today_ + relativedelta(hours=-h)

    #사용자 기준 로그는 밑의 두개의 모델을 바탕으로 생성 사용자 기준 로그가 이미 있을 시에 업데이트하기 위해 if 문으로 나눔
    page_access =PageAccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    main_access =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    for i in main_access:
        user =  UserLog.objects.filter(ip=i.ip).filter(created_at__gte=str(new_date))
        if len(user):
            user=user[0]
            user.day_cnt +=1
            if user.main_page=='X':
                user.main_page = 'O'
            user.save()
        else:
            UserLog.objects.create(
                ip=i.ip,
                main_page='O',
                day_cnt=1
            )

    for i in page_access:
        x=i.url.split('/')
        user =  UserLog.objects.filter(ip=i.ip).filter(created_at__gte=str(new_date))
        if len(user):
            user=user[0]
            try:
                if x[4]=='detail':
                    user.search_detail = 'O'
                    user.bounce_rate =False
                    user.visit_cnt += 1
                    user.save()
            except:
                if x[3]=='login' and user.login == 'X':
                    user.login = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate =False
                    user.save()
                elif x[3]=='request' and user.request == 'X':
                    user.request = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='project' and user.project == 'X':
                    user.project = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='magazine' and user.magazine == 'X':
                    user.magazine = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='search' and user.search == 'X':
                    user.search = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='signup' and user.signUp == 'X':
                    user.signUp = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
  
        else:
            try: 
                if x[4]=='detail':
                    UserLog.objects.create(
                        ip=i.ip,
                        search_detail='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
            except:
                if x[3]=='login':
                    UserLog.objects.create(
                        ip=i.ip,
                        login='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
                elif x[3]=='request':
                    UserLog.objects.create(
                        ip=i.ip,
                        request='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
                elif x[3]=='project':
                    UserLog.objects.create(
                        ip=i.ip,
                        project='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
                elif x[3]=='magazine':
                    UserLog.objects.create(
                        ip=i.ip,
                        magazine='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
                elif x[3]=='search':
                    UserLog.objects.create(
                        ip=i.ip,
                        search='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
                elif x[3]=='signup':
                    UserLog.objects.create(
                        ip=i.ip,
                        signUp='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )