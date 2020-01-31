import matplotlib.pyplot as plt
import cx_Oracle
import pandas as pd

conn_str = 'psnavigator/navigate@172.21.170.234/CA528'
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()


query = """select 
    t.schoolname,
    t.teacher_name,
	t.course_name,
    t.course_number,
  sum(CASE WHEN upper(t.grade)  like 'A%' THEN 1 else 0 end) A, 
	sum(CASE WHEN t.grade like 'B%' or t.grade like 'b%' THEN 1 else 0 end) B, 	
	sum(CASE WHEN t.grade like 'C%' or t.grade like 'c%' THEN 1 else 0 end) C, 
	sum(CASE WHEN t.grade like 'D%' or t.grade like 'd%' THEN 1 else 0 end) D, 
	sum(CASE WHEN t.grade like 'F%' or t.grade like 'f%' THEN 1 else 0 end) F,
   /* sum (CASE WHEN t.grade like 'P' then 1 else 0 end) P,*/
sum(CASE WHEN not(t.grade like 'A%' or t.grade like 'B%' or t.grade like 'C%' or t.grade like 'D%'  or t.grade like 'F%' or t.grade like 'a%' or t.grade like 'c%' or t.grade like 'd%' or t.grade like 'f%' or t.grade like'b%'or t.grade like 'P') THEN 1 else 0 end) other 
from

(SELECT
	d.studentid,
	D.storecode,
	d.grade as Grade,
	D.course_name,
	D.course_number,
	/*D.grade_level course_grade_level,*/
	D.schoolname,
	D.teacher_name,
	round (1990+ ( D.termid / 100 )) AS school_year
--B.NAME as "SCHOOL",
FROM
	SCHOOLS B
join STOREDGRADES D on B.school_number  = d.schoolid
WHERE
	B.school_number = 362
	/*AND Z.id = A.fteid */
	--AND D.grade_level > 8 
	--AND D.grade_level <= 12
--AND B.school_number BETWEEN 210 and 382
--AND B.school_number <> 342
AND D.termid between 2800 and 2899
AND D.storecode in ('S1')
AND d.teacher_name is not null
) T
GROUP BY  t.teacher_name, t.schoolname, t.course_name, t.course_number """




#query_results = c.execute(query)

df=pd.read_sql(query, conn)
print(df)

"""fig=plt.figure(figsize=(7,5))
names= ['Ari', "Ben", 'Catherine','Donald']
scores = [89, 36, 59, 97]
scores2=[95, 85, 87, 62]
positions = [0,1,2,3]
positions2=[0.3, 1.3, 2.3, 3.3]
positions3=[0.15, 1.15, 2.15, 3.15]
plt.bar(positions, scores, width=0.3)
plt.bar(positions2, scores2, width=0.3)
plt.xticks(positions3, names)
plt.title("Test Scores")
plt.show()"""

