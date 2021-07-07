# Generated by Django 3.0.8 on 2021-02-03 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0050_modify_proposal_type_period_8_20210203_1521'),
    ]
    
    sqlCache = []
    reverseSqlCache = []

    somethingList=[
        ["최낙의 기술고문","15","뭐든지다잘함","01058825882"],
        ["김은구 기술고문","15","뭐든지다잘함","01058825882"],
        ["박영호 기술고문","15","뭐든지다잘함","01058825882"],
        ["김원 기술고문","15","뭐든지다잘함","01058825882"],
        ["신윤수 기술고문","15","뭐든지다잘함","01058825882"],
        ["유정석 기술고문","15","뭐든지다잘함","01058825882"],
        ["노경섭 기술고문","15","뭐든지다잘함","01058825882"],
        ["안철웅 기술고문","15","뭐든지다잘함","01058825882"],
        ["노현수 기술팀장","9","뭐든지다잘함","01058825882"],
        ["최진영 기술이사","10","뭐든지다잘함","01058825882"],
        ["김형규 기술팀장","10","뭐든지다잘함","01058825882"],
    ]

    

    for something in somethingList:
        sqlCache.append(
            """
                insert into public."project_consultant"
                ("name", "year","content","phoneNumber")
                values(
                    '{name}',
                    '{year}',
                    '{content}',
                    '{phoneNumber}'
                );
            """.format(
                name = something[0],
                year=something[1],
                content=something[2],
                phoneNumber = something[3]
                )
        )

    reverseSqlCache.append(
        """
            delete from public."project_consultant";
            ALTER SEQUENCE "project_consultant_id_seq" RESTART WITH 1;
        """
    )

    operations = [
        migrations.RunSQL(
            sql = reverseSqlCache, 
            reverse_sql = reverseSqlCache
        ),
        migrations.RunSQL(
            sql = sqlCache, 
            reverse_sql = reverseSqlCache
        )
    ]
