# Generated by Django 3.0.8 on 2021-02-02 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0048_modify_proposal_type_20210202_1342'),
    ]

    sqlCache = []
    reverseSqlCache = []

    typeTaskList=[
        [1	,1],
        [1	,2],
        [1	,3],
        [1	,4],
        [1	,5],
        [1	,6],
        [1	,12],
        [2	,1],
        [2	,2],
        [2	,3],
        [2	,4],
        [2	,5],
        [2	,6],
        [2	,11],
        [2	,12],
        [3	,1],
        [3	,2],
        [3	,3],
        [3	,4],
        [3	,5],
        [3	,6],
        [3	,11],
        [3	,12],
        [4	,1],
        [4	,2],
        [4	,3],
        [4	,4],
        [4	,5],
        [4	,6],
        [4	,11],
        [4	,12],
        [5	,1],
        [5	,2],
        [5	,3],
        [5	,4],
        [5	,5],
        [6	,1],
        [6	,2],
        [6	,4],
        [6	,5],
        [6	,6],
        [8	,1],
        [8	,2],
        [8	,4],
        [8	,5],
        [8	,6],
        [13,	16],
        [14,	16],
        [12,	14],
        [12,	15],
        [13,	9],
        [13,	10],
        [13,	13],
        [13,	19],
        [13,	22],
        [13,	31],
        [12,	18],
        [12,	21],
        [12,	30],
        [13,	3],
        [14,	34],
        [14,	3],
        [14,	9],
        [14,	10],
        [14,	11],
        [14,	13],
        [14,	19],
        [14,	22],
        [14,	31],
        [12,	33],
        [13,	11],
        [11,	34],
        [11,	3],
        [11,	9],
        [11,	10],
        [11,	11],
        [11,	13],
        [11,	16],
        [11,	19],
        [11,	22],
        [11,	31],
        [10,	34],
        [10,	3],
        [10,	9],
        [10,	10],
        [10,	11],
        [10,	13],
        [10,	16],
        [10,	19],
        [10,	22],
        [10,	31],
        [9	,33],
        [9	,14],
        [9	,15],
        [9	,18],
        [9	,21],
        [9	,30],
        [8	,32],
        [8	,35],
        [8	,7],
        [8	,8],
        [8	,12],
        [8	,17],
        [8	,20],
        [8	,23],
        [8	,24],
        [8	,25],
        [7	,32],
        [7	,1],
        [7	,2],
        [7	,4],
        [7	,5],
        [7	,6],
        [7	,7],
        [7	,8],
        [7	,35],
        [7	,12],
        [7	,17],
        [7	,20],
        [7	,23],
        [7	,24],
        [7	,25],
        [6	,32],
        [6	,35],
        [6	,7],
        [6	,8],
        [6	,12],
        [6	,17],
        [6	,20],
        [6	,23],
        [6	,24],
        [6	,25],
        [7	,11],
        [7	,9],
        [7	,10],
        [7	,3],
        [8	,11],
        [8	,9],
        [8	,10],
        [8	,3],
        [5	,32],
        [5	,35],
        [5	,6],
        [5	,7],
        [5	,8],
        [5	,12],
        [5	,17],
        [5	,20],
        [5	,23],
        [5	,24],
        [5	,25],
        [4	,32],
        [4	,35],
        [4	,7],
        [4	,8],
        [4	,9],
        [4	,10],
        [4	,17],
        [4	,20],
        [4	,23],
        [4	,24],
        [4	,25],
        [4	,26],
        [4	,27],
        [4	,28],
        [4	,29],
        [3	,32],
        [3	,35],
        [3	,7],
        [3	,8],
        [3	,9],
        [3	,10],
        [3	,17],
        [3	,20],
        [3	,23],
        [3	,24],
        [3	,25],
        [3	,26],
        [3	,27],
        [3	,28],
        [3	,29],
        [2	,32],
        [2	,35],
        [2	,7],
        [2	,8],
        [2	,9],
        [2	,10],
        [2	,17],
        [2	,20],
        [2	,23],
        [2	,24],
        [2	,25],
        [2	,26],
        [2	,27],
        [2	,28],
        [2	,29],
        [1	,32],
        [1	,35],
        [1	,7],
        [1	,8],
        [1	,17],
        [1	,20],
        [1	,23],
        [1	,24],
        [1	,25],
        [1	,26],
        [1	,27],
        [1	,28],
        [1	,29],

        [13,34],
        
        [16,34],
        [16,3],
        [16,9],
        [16,10],
        [16,11],
        [16,13],
        [16,16],
        [16,19],
        [16,22],
        [16,31],

        [15,34],
        [15,3],
        [15,9],
        [15,10],
        [15,11],
        [15,13],
        [15,16],
        [15,19],
        [15,22],
        [15,31],
        



    ]

    

    for typeTask in typeTaskList:
        sqlCache.append(
            """
                insert into public."project_proposaltype_task"
                ("proposaltype_id", "task_id")
                values(
                    '{proposaltype_id}',
                    '{task_id}'
                    );
            """.format(
                proposaltype_id = typeTask[0],
                task_id=typeTask[1]
                )
        )

    reverseSqlCache.append(
        """
            delete from public."project_proposaltype_task";
            ALTER SEQUENCE "project_proposaltype_task_id_seq" RESTART WITH 1;
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