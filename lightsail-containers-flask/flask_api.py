from flask import Flask, session, request
import boto3
from random import randrange
from datetime import datetime as dt

iam = boto3.client('iam',
                    aws_access_key_id='AKIASMSXSQ3XBAHGPEJT', 
                    aws_secret_access_key='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'
)

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

def create_login_profile(user_name,password):
    iam.create_user( UserName=user_name)
    response = iam.create_login_profile(
    UserName= user_name,
    Password= password,
    PasswordResetRequired=False
    )
    iam.attach_user_policy(
        UserName = user_name,
        PolicyArn='arn:aws:iam::164466165486:policy/EC2_FamilyRestrict'
    )
    return "User Created"

def list_instances_by_tag_value(tagkey, tagvalue):
    client = boto3.client('ec2',
                      region_name="us-east-1",
                    aws_access_key_id='AKIASMSXSQ3XBAHGPEJT', 
                    aws_secret_access_key='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')
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.
 
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    return instancelist

def delete_user(user_name):
    client = boto3.client('ec2',
                      region_name="us-east-1",
                    aws_access_key_id='AKIASMSXSQ3XBAHGPEJT', 
                    aws_secret_access_key='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')
    list = list_instances_by_tag_value('owner','user/'+user_name)
    for l in list:
        try:
            response = client.terminate_instances(InstanceIds=[l], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    iam.detach_user_policy(
        UserName = user_name,
        PolicyArn='arn:aws:iam::164466165486:policy/EC2_FamilyRestrict'
    )
    iam.delete_login_profile(
        UserName= user_name
    )
    iam.delete_user(
        UserName= user_name
    )

@app.before_request
def before_request():
    print("session data: "+ str(session))

@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
    userid = "yash"+str(randrange(100000, 999999))+"qyqyq"
    passwd = "Eric@123"
    session['user_name'] = userid
    session_start_time = dt.now()
    session['start_time'] = session_start_time
    create_login_profile(userid, passwd)
    return userid

@app.route('/deleteuser', methods=['GET', 'POST'])
def deleteuser():
    if request.method == 'POST':
        t_id = request.json['user']
        print('****************************************************************'+t_id)
        delete_user(t_id)
        return "User Deleted"

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)