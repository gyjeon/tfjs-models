from flask import Flask, render_template, request, session, redirect, url_for
import requests
import os


app = Flask(__name__)
app.secret_key = 'Jeon_Family_GPS'

# https://flask-web-weiem.run.goorm.site/

@app.route('/')
def fnRoot():
    if 's_email' in session:
        # return redirect(url_for('gpsTrace')) # 구름에서 사용하면 도메인이 바뀌어 버림. 도메인이 바뀌면 지도 API 호출이 안됨
        return render_template('/kakaoMap/GoToGpsTrace.html')
    else:
        return render_template('/kakaoMap/login.html')

@app.route('/loginProc', methods=['POST','GET'])	
def loginProc():
    s_email = request.form["s_email"]
    pwd = request.form["pwd"]
    if pwd == "!@pmo2041": #비밀번호로 익명 로그인 차단
        session['s_email'] = s_email
        return render_template('/kakaoMap/GoToGpsTrace.html')
    else:
        return render_template('/kakaoMap/login.html', msg="로그인정보가 옳지 않습니다.")
    
@app.route('/logout')
def logout():
    session.pop('s_email', None)
    return render_template('/kakaoMap/login.html')

@app.route("/gpsTraceProc", methods=['POST','GET'])	
def gpsTraceProc():
     if request.method == 'GET':
        # args_dict = request.args.to_dict()
        # print(args_dict)
        email = request.args["email"]
        latitude = request.args["latitude"]
        longitude = request.args["longitude"]
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        timestamp = request.args["timestamp"]

        save_filename = "gps_save_" + email + ".txt"
        with open(save_filename,"a", encoding='utf-8') as f:
                f.write("%s,%s,%s,%s,%s" % (email, latitude, longitude, ip, timestamp +",\n"))
        return ""
     else:
        # num = int(request.form["num"])
        # email = request.form["email"]
        # return "POST로 전달된 데이터({}, {})".format(num, name)
        return ""    

@app.route("/gpsTrace", methods=['POST','GET'])	
def gpsTrace():
    
    email_friend=""
    latitude_friend = ""
    longitude_friend = ""
    ip_friend = ""
    timestamp_friend = ""

    email_friends = []
    latitude_friends = []
    longitude_friends = []
    ip_friends = []
    timestamp_friends = []

    total_Email_friends = ['yung','ksy','juheon','chang','kyung']
    for i in total_Email_friends:
        email_friend = i
        # email_friend = 'ksy'
        # print("세션",session["s_email"])
        # print(email_friend)
        
        if email_friend.strip() != session["s_email"].strip(): #본인은 스킵
            # print("다르다")

            save_filename = "gps_save_" + email_friend + ".txt"
            
            # 파일이 있는지 확인
            if os.path.isfile(save_filename):

                # 정보 가지고 오기
                with open(save_filename,"r", encoding='utf-8') as f:
                    read_file = f.read()

                if len(read_file) > 0:
                    arr_read_file = read_file.split(',')

                    email_friend = arr_read_file[0].strip().rstrip('\n')
                    latitude_friend = arr_read_file[1].strip().rstrip('\n')
                    longitude_friend = arr_read_file[2].strip().rstrip('\n')
                    ip_friend = arr_read_file[3].strip().rstrip('\n')
                    timestamp_friend = arr_read_file[4].strip().rstrip('\n').replace(chr(10),"")
                    
                    email_friends.append(arr_read_file[0])
                    latitude_friends.append(arr_read_file[1].strip().rstrip('\n'))
                    longitude_friends.append(arr_read_file[2].strip().rstrip('\n'))
                    ip_friends.append(arr_read_file[3].strip().rstrip('\n'))
                    timestamp_friends.append(arr_read_file[4].strip().rstrip('\n'))
                    
                    listnum = len(latitude_friends)
                    # print(listnum)
                    
                    
                else:
                    email_friend=""
                    # latitude_friend = "37.55838603055553" #집 37.5583865,126.002003
                    # longitude_friend = "127.00200324712047"
                    # ip_friend = "192.16.0.1"
                    # timestamp_friend = 1677220875017
    
    print(email_friends)
    return render_template('/kakaoMap/gpsTrace.html', email_friends=email_friends,latitude_friends=latitude_friends, longitude_friends=longitude_friends, ip_friends=ip_friends, timestamp_friends=timestamp_friends, listnum=listnum)
    # return render_template('/kakaoMap/gpsTrace.html', email_friend=email_friend,latitude_friend=latitude_friend, longitude_friend=longitude_friend, ip_friend=ip_friend, timestamp_friend=timestamp_friend)


# 서버 아이피
# r = requests.get(r'http://jsonip.com')
# server_ip= r.json()['ip'] 
@app.route('/clientIp', methods=['GET'])
def clientIp():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route("/gps", methods=['POST','GET'])	
def gps():
    return render_template('/gps.html',title='헬로')

@app.route("/kakaoMapApi", methods=['POST','GET'])	
def kakaoMapApi():
    return render_template('/kakaoMap/kakaoMapApi.html',title='헬로')

# 파이썬 명령어로 실행할 수 있음
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

# 명령 실행    
# root@goorm:/workspace/flask_web# python3 /workspace/flask_web/app.py

# 백그라운드에서 실행
# nohup python3 -u /workspace/flask_web/app.py &



# 위도경도 구하기
# http://map.esran.com/