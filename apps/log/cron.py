#-*- coding: cp949 -*-
from apps.log.models import *
from apps.account.models import *
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models import Q

def postDayLog():
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

    new_date = today_ + relativedelta(hours=-h)
    access_cnt =len(AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)))
    access_log =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct()
    access_real_cnt = len(access_log)
    search = SearchText.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    search_cnt = len(search)
    search_user_cnt = len(search.values('ip').order_by().distinct())
    count = 0
    for i in search:
        if i.text== None:
            pass
        else:
            x=Partner.objects.filter(user__is_active=True).filter(Q(name__contains=i.text) | Q(info_company__contains=i.text) | Q(history__contains=i.text) | Q(category_middle__category__contains=i.text))
            if len(x) >= 3:
                count+=1
    search_success_cnt = round((count/search_cnt)*100,2)

    signup_cnt =len(User.objects.filter(date_joined__gte=str(new_date)).filter(date_joined__lte=str(today_)).order_by('id').distinct())
    login_cnt =len(LoginLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)).values('ip').order_by().distinct())
    click_cnt =len(clickLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)))

    bounce_cnt=0
    user_log =UserLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    user_log_cnt =len(UserLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_)))
    d = user_log_cnt
    n = user_log_cnt 
    for i in user_log:
        n+=i.visit_cnt
        if i.bounce_rate==True:
            bounce_cnt+=1

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
        pv_rate = pv,
        revisit_cnt_week=revisit_cnt_week,
        bounce_rate=bounce_rate
        )


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
    for i in user_out_total:
        if len(x.filter(ip=i['ip'])) != 0:
            user_log_cnt+=1
            if i['bounce_rate']==True:
                bounce_cnt+=1
    bounce_rate = round((bounce_cnt/user_log_cnt)*100,2)

    #검색 성공률
    count = 0
    search_cnt_d = 0
    for i in search_total:
        if len(x.filter(ip=i['ip'])) != 0:
            search_cnt_d +=1
            print(i['text'])
            if i['text']== None:
                pass
            else:
                y=Partner.objects.filter(user__is_active=True).filter(Q(name__contains=i['text']) | Q(info_company__contains=i['text']) | Q(history__contains=i['text']) | Q(category_middle__category__contains=i['text']))
                print(len(y))
                if len(y) >= 3:
                    count+=1
    print(count,search_cnt_d)
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


    DayLogOldVisiter.objects.create(
        access_cnt=access_cnt,
        access_real_cnt=access_real_cnt,
        search_cnt=search_cnt,
        search_user_cnt=search_user_cnt,
        search_success_cnt=search_success_cnt,
        login_cnt=login_cnt,
        click_cnt=click_cnt,
        revisit_cnt=revisit_cnt,
        revisit_cnt_week=revisit_cnt_week,
        bounce_rate=bounce_rate
        )
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
    for i in user_out_total:
        if len(x.filter(ip=i['ip'])) == 0:
            user_log_cnt+=1
            if i['bounce_rate']==True:
                bounce_cnt+=1
    bounce_rate = round((bounce_cnt/user_log_cnt)*100,2)

    #검색 성공률
    count = 0
    search_cnt_d = 0
    for i in search_total:
        if len(x.filter(ip=i['ip'])) == 0:
            search_cnt_d +=1
            print(i['text'])
            if i['text']== None:
                pass
            else:
                y=Partner.objects.filter(user__is_active=True).filter(Q(name__contains=i['text']) | Q(info_company__contains=i['text']) | Q(history__contains=i['text']) | Q(category_middle__category__contains=i['text']))
                print(len(y))
                if len(y) >= 3:
                    count+=1
    print(count,search_cnt_d)
    search_success_cnt = round((count/search_cnt_d)*100,2)


    DayLogNewVisiter.objects.create(
        access_cnt=access_cnt,
        access_real_cnt=access_real_cnt,
        search_cnt=search_cnt,
        search_user_cnt=search_user_cnt,
        search_success_cnt=search_success_cnt,
        login_cnt=login_cnt,
        click_cnt=click_cnt,
        bounce_rate=bounce_rate
        )





def postUserLog():
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
    page_access =PageAccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    main_access =AccessLog.objects.filter(created_at__gte=str(new_date)).filter(created_at__lte=str(today_))
    for i in main_access:
        user =  UserLog.objects.filter(ip=i.ip).filter(created_at__gte=str(new_date))
        if len(user):
            user=user[0]
            if user.main_page=='X':
                user.main_page = 'O'
                user.save()
        else:
            UserLog.objects.create(
                ip=i.ip,
                main_page='O',
            )

    for i in page_access:
        x=i.url.split('/')
        user =  UserLog.objects.filter(ip=i.ip).filter(created_at__gte=str(new_date))
        if len(user):
            user=user[0]
            try:
                if x[4]=='detail' and user.producer_detail == 'X':
                    user.producer_detail = 'O'
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
                elif x[3]=='manufacturer' and user.manufacturer == 'X':
                    user.manufacturer = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='magazine' and user.magazine == 'X':
                    user.magazine = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='phoneClick' and user.phone_click == 'X':
                    user.phone_click = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
                elif x[3]=='producer' and user.producer == 'X':
                    user.producer = 'O'
                    user.visit_cnt += 1
                    user.bounce_rate = False
                    user.save()
  
        else:
            try: 
                if x[4]=='detail':
                    UserLog.objects.create(
                        ip=i.ip,
                        producer_detail='O',
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
                elif x[3]=='manufacturer':
                    UserLog.objects.create(
                        ip=i.ip,
                        manufacturer='O',
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
                elif x[3]=='phoneClick':
                    UserLog.objects.create(
                        ip=i.ip,
                        phone_click='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )
                elif x[3]=='producer':
                    UserLog.objects.create(
                        ip=i.ip,
                        producer='O',
                        bounce_rate=False,
                        visit_cnt = 1
                    )


