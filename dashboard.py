from flask import Blueprint,request,jsonify
from sqlalchemy.sql import text
from db import db
import datetime

dashboard_blueprint=Blueprint('dashboard_blueprint',__name__)

# Today's visitors
@dashboard_blueprint.route('/today-visitors')
def todayVisitors():
    currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
    sqlTodayVisitors=text('select count(*) as today_visitors from visitors_log where date="'+currentDate+'"')
    resultData=db.engine.execute(sqlTodayVisitors)
    rawData=resultData.fetchall()
    jsonData=jsonify([dict(row) for row in rawData])
    return jsonData

#overall visitors
@dashboard_blueprint.route('/overall-visitors')
def overallVisitors():
    sqlOverallVisitors=text('select count(*) as overall_visitors from visitors_log')
    resultData=db.engine.execute(sqlOverallVisitors)
    rawData=resultData.fetchall()
    jsonData=jsonify([dict(row) for row in rawData])
    return jsonData

@dashboard_blueprint.route('/male-visitors')
def maleVisitors():
    currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
    sqlMaleVisitors=text('select count(*) as male_visitors from visitors_log where date="'+currentDate+'" and gender=1')
    resultData=db.engine.execute(sqlMaleVisitors)
    rawData=resultData.fetchall()
    jsonData=jsonify([dict(row) for row in rawData])
    return jsonData

@dashboard_blueprint.route('/female-visitors')
def femaleVisitors():
    currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
    sqlFemaleVisitors=text('select count(*) as female_visitors from visitors_log where date="'+currentDate+'" and gender=2')
    resultData=db.engine.execute(sqlFemaleVisitors)
    rawData=resultData.fetchall()
    jsonData=jsonify([dict(row) for row in rawData])
    return jsonData

#table data
@dashboard_blueprint.route('/table-data')
def tableData():
    currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
    txtlabel='' 
    x=''
    for a in range(1,6):
        if a==1:
            txtlabel='Kid'
        elif a==2:
            txtlabel='Teenager'
        elif a==3:
            txtlabel='Youngster'
        elif a==4:
            txtlabel='Adult'
        elif a==5:
            txtlabel='Senior Citizen'
        
        for g in range(1,3):
            # today's visitors
            sqlTodayVisitors=text('select count(*) as today_visitors from visitors_log where date="'+currentDate+'" and gender='+str(g)+' and 	age_group='+str(a)+'')
            resultData=db.engine.execute(sqlTodayVisitors)
            rawData=resultData.fetchall()
            ageGroupGenderToday=rawData[0].today_visitors

            # overall visitors
            sqlOverallVisitors=text('select count(*) as overall_visitors from visitors_log where gender='+str(g)+' and 	age_group='+str(a)+'')
            resultOData=db.engine.execute(sqlOverallVisitors)
            rawOData=resultOData.fetchall()
            ageGroupGenderOverall=rawOData[0].overall_visitors

            gText=''

            if g==1:
                gText="Male"
            elif g==2:
                gText="Female"
            
            x+='{"gender":"'+gText+'","age_group":"'+txtlabel+'","today_visitors":"'+str(ageGroupGenderToday)+'","overall_visitors":"'+str(ageGroupGenderOverall)+'"},'

        # End of the inner for loop
    # End of the outer for loop
    x=x[:-1]
    jsonData='['+x+']'
    return jsonData

# graph 
@dashboard_blueprint.route('/graph-data')
def grpahData():
    x=''
    for m in range(1,13):
        sqlMonthData=text('SELECT COUNT(*) AS monthly_visitors from visitors_log where month(date)="'+str(m)+'"')
        resultData=db.engine.execute(sqlMonthData)
        rawData=resultData.fetchall()
        totalMonthlyVisitors=rawData[0].monthly_visitors

        x+='{"month":"'+str(totalMonthlyVisitors)+'"},'

    x=x[:-1]

    jsonData='['+x+']'
    return jsonData