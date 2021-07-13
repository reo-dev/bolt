# Generated by Django 3.0.8 on 2021-01-26 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_auto_20210126_1424'),
    ]

    sqlCache = []
    reverseSqlCache = []

    categoryList=[
        ["소방용품","media/null",1],
        ["건설용품","media/null",1],
        ["도로용품","media/null",1],
        ["컴퓨터용품","media/null",1],
        ["주방용품","media/null",1],
        ["청소용품","media/null",1],
        ["생활/위생/욕실용품","media/null",1],
        ["가전용품","media/null",1],
        ["사무용품","media/null",1],
        ["배관용품","media/null",1],
        ["의료/헬스케어용품","media/null",1],
        ["자동차용품","media/null",1],
        ["레저/스포츠/여행용품","media/null",1],
        ["냉장고/에어컨/세탁기/청소기/TV","media/null",1],
        ["수유/유아용품","media/null",1],
        ["가구/인테리어/조명","media/null",1],
        ["반려동물용품","media/null",1],
        ["공작기기","media/null",2],
        ["유공압기기","media/null",2],
        ["냉난방/공조기기","media/null",2],
        ["화학/플랜트기기","media/null",2],
        ["밴딩/포장기기","media/null",2],
        ["식품기기","media/null",2],
        ["제어/계측기기","media/null",2],
        ["산업용로봇","media/null",2],
        ["검사기/시험기/실험기","media/null",2],
        ["목공기계","media/null",2],
        ["농기계","media/null",2],
        ["중장비","media/null",2],
        ["특장차","media/null",2],
        ["물류시스템기기","media/null",2],
        ["운반/하역기기","media/null",2],
        ["산업환경장비","media/null",2],
        ["금형/사출기기","media/null",2],
        ["반도체장비","media/null",2],
        ["건설기기","media/null",2],
        ["펌프류","media/null",3],
        ["FA 부품","media/null",3],
        ["동력전달 부품","media/null",3],
        ["제어/계측 부품","media/null",3],
        ["전자/반도체부품","media/null",3],
        ["기타 기계 부품","media/null",3],
        ["기타 부품 및 소재","media/null",3],
        ["씰링 부품","media/null",3],
        ["베어링","media/null",3],
        ["볼트/너트/와샤/나사/스크류","media/null",3],
        ["방진/방음","media/null",3],
        ["전선/전기자재","media/null",3],
        ["건축자재","media/null",3],
        ["전동공구","media/null",4],
        ["충전공구","media/null",4],
        ["에어공구","media/null",4],
        ["용접공구","media/null",4],
        ["연마공구","media/null",4],
        ["엔진공구","media/null",4],
        ["유압공구","media/null",4],
        ["원예공구","media/null",4],
        ["절삭공구","media/null",4],
        ["측량공구","media/null",4],
        ["금형공구","media/null",4],
        ["공작공구","media/null",4],
        ["자동차공구","media/null",4],
    ]

    

    for category in categoryList:
        sqlCache.append(
            """
                insert into public."category_category"
                ("category", "middle_img","maincategory_id")
                values(
                    '{category}',
                    '{middle_img}',
                    '{maincategory_id}'
                );
            """.format(
                category = category[0],
                middle_img=category[1],
                maincategory_id=category[2],
                )
        )

    reverseSqlCache.append(
        """
            delete from public."category_category";
            ALTER SEQUENCE "category_category_id_seq" RESTART WITH 1;
        """
    )

    operations = [
        migrations.RunSQL(
            sql = sqlCache,
            reverse_sql = reverseSqlCache
            )
    ]