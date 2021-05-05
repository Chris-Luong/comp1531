import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, users_all_v1, user_stats_v1, users_stats_v1
from src.channels import channels_list_v2, channels_listall_v2, channels_create_v2
from src.dm import dm_details_v1, dm_list_v1, dm_create_v1, dm_remove_v1, dm_invite_v1, dm_leave_v1, dm_messages_v1
from src.channel import channel_invite_v2, channel_details_v2, channel_messages_v2, channel_join_v2, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_share_v1, message_senddm_v1, \
    message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.other import search_v2, admin_user_remove_v1, admin_userpermission_change_v1, notifications_get_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.clear import clear_v1
import hashlib
from flask_mail import Mail, Message

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
mail = Mail(APP)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
APP.config['MAIL_SERVER']='smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = '1531dorrito@gmail.com'
APP.config['MAIL_PASSWORD'] = 'Wallaby123!'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True

mail = Mail(APP)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/login/v2", methods=["POST"])
def login():
    info = request.get_json()
    email = info["email"]
    password = info["password"]

    user_login = auth_login_v2(email, password)
    return dumps(
        user_login
    )

@APP.route("/auth/register/v2", methods=["POST"])
def register():
    info = request.get_json()
    email = info["email"]
    password = info["password"]
    name_first = info["name_first"]
    name_last = info["name_last"]

    user_registered = auth_register_v2(email, password, name_first, name_last)
    return dumps(
        user_registered
    )

@APP.route("/auth/logout/v1", methods=["POST"])
def logout():
    info = request.get_json()
    token = info["token"]

    user_logout = auth_logout_v1(token)
    return dumps(
        user_logout
    )

@APP.route("/user/profile/v2", methods=["GET"])
def profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    #data = data if data is not None else False

    user_profile = user_profile_v1(token, u_id)
    return dumps(
        user_profile
    )

@APP.route("/user/profile/setname/v2", methods=["PUT"])
def setname():
    info = request.get_json()
    token = info["token"]
    name_first = info["name_first"]
    name_last = info["name_last"]

    set_name = user_profile_setname_v1(token, name_first, name_last)
    return dumps(
        set_name
    )

@APP.route("/user/profile/setemail/v2", methods=["PUT"])
def setemail():
    info = request.get_json()
    token = info["token"]
    email = info["email"]

    set_email = user_profile_setemail_v1(token, email)
    return dumps(
        set_email
    )

@APP.route("/user/profile/sethandle/v1", methods=["PUT"])
def sethandle():
    info = request.get_json()
    token = info["token"]
    handle_str = info['handle']

    set_handle = user_profile_sethandle_v1(token, handle_str)
    return dumps(
        set_handle
    )

@APP.route("/users/all/v1", methods=["GET"])
def users():
    token = request.args.get('token')

    users = users_all_v1(token)
    return dumps(
        users
    )

@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    reset = clear_v1()

    return dumps(
        reset
    )

@APP.route("/channels/list/v2", methods=["GET"])
def list_channels():
    token = request.args.get('token')

    channel_list = channels_list_v2(token)
    return dumps(
        channel_list
    )

@APP.route("/channels/listall/v2", methods=["GET"])
def list_all():
    token = request.args.get('token')

    list_all = channels_listall_v2(token)
    return dumps(
        list_all
    )

@APP.route("/channels/create/v2", methods=["POST"])
def create_channel():
    info = request.get_json()
    token = info["token"]
    name = info["name"]
    is_public = info["is_public"]

    create_channel = channels_create_v2(token, name, is_public)
    return dumps(
        create_channel
    )

@APP.route("/dm/details/v1", methods=["GET"])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')

    dm_details = dm_details_v1(token, dm_id)
    return dumps(
        dm_details
    )

@APP.route("/dm/list/v1", methods=["GET"])
def dm_list():
    token = request.args.get('token')

    dm_list = dm_list_v1(token)
    return dumps(
        dm_list
    )

@APP.route("/dm/create/v1", methods=["POST"])
def dm_create():
    info = request.get_json()
    token = info["token"]
    u_ids = info["u_ids"]
    
    dm_create = dm_create_v1(token, u_ids)
    return dumps(
        dm_create
    )

@APP.route("/dm/remove/v1", methods=["DELETE"])
def dm_remove():
    info = request.get_json()
    token = info["token"]
    dm_id = info["dm_id"]

    remove = dm_remove_v1(token, dm_id)

    return dumps(
        remove
    )

@APP.route("/dm/invite/v1", methods=["POST"])
def dm_invite():
    info = request.get_json()
    token = info["token"]
    dm_id = info["dm_id"]
    u_id = info["u_id"]
    
    dm_invite = dm_invite_v1(token, dm_id, u_id)
    return dumps(
        dm_invite
    )

@APP.route("/dm/leave/v1", methods=["POST"])
def dm_leave():
    info = request.get_json()
    token = info["token"]
    dm_id = info["dm_id"]
        
    dm_leave = dm_leave_v1(token, dm_id)
    return dumps(
        dm_leave
    )

@APP.route("/dm/messages/v1", methods=["GET"])
def dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')

    dm_messages = dm_messages_v1(token, dm_id, start)
    return dumps(
        dm_messages
    )

@APP.route("/channel/invite/v2", methods=["POST"])
def channel_invite():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    u_id = info["u_id"]
    
    channel_invite = channel_invite_v2(token, channel_id, u_id)
    return dumps(
        channel_invite
    )

@APP.route("/channel/details/v2", methods=["GET"])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    channel_details = channel_details_v2(token, channel_id)
    return dumps(
        channel_details
    )

@APP.route("/channel/messages/v2", methods=["GET"])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')

    channel_messages = channel_messages_v2(token, channel_id, start)
    return dumps(
        channel_messages
    )

@APP.route("/channel/join/v2", methods=["POST"])
def channel_join():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
        
    channel_join = channel_join_v2(token, channel_id)
    return dumps(
        channel_join
    )

@APP.route("/channel/addowner/v1", methods=["POST"])
def channel_addowner():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    u_id = info["u_id"]
    
    channel_addowner = channel_addowner_v1(token, channel_id, u_id)
    return dumps(
        channel_addowner
    )

@APP.route("/channel/removeowner/v1", methods=["POST"])
def channel_removeowner():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    u_id = info["u_id"]
    
    channel_removeowner = channel_removeowner_v1(token, channel_id, u_id)
    return dumps(
        channel_removeowner
    )

@APP.route("/channel/leave/v1", methods=["POST"])
def channel_leave():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
        
    channel_leave = channel_leave_v1(token, channel_id)
    return dumps(
        channel_leave
    )

@APP.route("/message/send/v2", methods=["POST"])
def message_send():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    message = info["message"]
        
    message_send = message_send_v2(token, channel_id, message)
    return dumps(
        message_send
    )

@APP.route("/message/edit/v2", methods=["PUT"])
def message_edit():
    info = request.get_json()
    token = info["token"]
    message_id = info["message_id"]
    message = info["message"]
        
    message_edit = message_edit_v2(token, message_id, message)
    return dumps(
        message_edit
    )

@APP.route("/message/remove/v1", methods=["DELETE"])
def message_remove():
    info = request.get_json()
    token = info["token"]
    message_id = info["message_id"]

    message_remove = message_remove_v1(token, message_id)

    return dumps(
        message_remove
    )

@APP.route("/message/share/v1", methods=["POST"])
def message_share():
    info = request.get_json()
    token = info["token"]
    og_message_id = info["og_message_id"]
    message = info["message"]
    channel_id = info["channel_id"]
    dm_id = info["dm_id"]
        
    message_share = message_share_v1(token, og_message_id, message, channel_id, dm_id)
    return dumps(
        message_share
    )

@APP.route("/message/senddm/v1", methods=["POST"])
def message_senddm():
    info = request.get_json()
    token = info["token"]
    dm_id = info["dm_id"]
    message = info["message"]
        
    message_senddm = message_senddm_v1(token, dm_id, message)
    return dumps(
        message_senddm
    )

@APP.route("/search/v2", methods=["GET"])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    
    search = search_v2(token, query_str)
    return dumps(
        search
    )

@APP.route("/admin/user/remove/v1", methods=["DELETE"])
def admin_user_remove():
    info = request.get_json()
    token = info["token"]
    u_id = info["u_id"]

    user_remove = admin_user_remove_v1(token, u_id)

    return dumps(
        user_remove
    )

@APP.route("/admin/userpermission/change/v1", methods=["POST"])
def admin_userpermission_change():
    info = request.get_json()
    token = info["token"]
    u_id = info["u_id"]
    permission_id = info["permission_id"]
        
    userpermission_change = admin_userpermission_change_v1(token, u_id, permission_id)
    return dumps(
        userpermission_change
    )

@APP.route("/notifications/get/v1", methods=["GET"])
def notifications():
    token = request.args.get('token')
        
    notifications = notifications_get_v1(token)
    return dumps(
        notifications
    )

@APP.route("/user/stats/v1", methods=["GET"])
def user_stats():
    token = request.args.get('token')
        
    stats = user_stats_v1(token)
    return dumps(
        stats
    )

@APP.route("/users/stats/v1", methods=["GET"])
def users_stats():
    token = request.args.get('token')
        
    dreams_stats = users_stats_v1(token)
    return dumps(
        dreams_stats
    )

@APP.route("/auth/passwordreset/request/v1", methods=["POST"])
def reset_request():
    info = request.get_json()
    email = info["email"]

    verified_email = auth_passwordreset_request_v1(email)

    msg = Message('Password Reset', sender = '1531dorrito@gmail.com', recipients = [verified_email["email"]])
    msg.body = "Your reset code is: " + str(verified_email["reset_code"])
    mail.send(msg)
    return dumps(
        verified_email
    )

@APP.route("/auth/passwordreset/reset/v1", methods=["POST"])
def reset_password():
    info = request.get_json()
    reset_code = info["reset_code"]
    new_password = info["new_password"]

    password_reset = auth_passwordreset_reset_v1(reset_code, new_password)

    return dumps(
        password_reset
    )

@APP.route("/standup/start/v1",methods=["POST"])
def standup_start():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    length = info["length"]

    standup_start = standup_start_v1(token, channel_id, length)

    return dumps(
        standup_start
    )

@APP.route("/standup/active/v1", methods=["GET"])
def standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
        
    standup_active = standup_active_v1(token, channel_id)

    return dumps(
        standup_active
    )

@APP.route("/standup/send/v1",methods=["POST"])
def standup_send():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    message = info["message"]

    standup_send = standup_send_v1(token, channel_id, message)

    return dumps(
        standup_send
    )

@APP.route("/message/sendlater/v1",methods=["POST"])
def message_sendlater():
    info = request.get_json()
    token = info["token"]
    channel_id = info["channel_id"]
    message = info["message"]
    time_sent = info["time_sent"]

    message_sendlater = message_sendlater_v1(token, channel_id, message, time_sent)

    return dumps(
        message_sendlater
    )

@APP.route("/message/sendlaterdm/v1",methods=["POST"])
def message_sendlaterdm():
    info = request.get_json()
    token = info["token"]
    dm_id = info["dm_id"]
    message = info["message"]
    time_sent = info["time_sent"]

    message_sendlaterdm = message_sendlaterdm_v1(token, dm_id, message, time_sent)

    return dumps(
        message_sendlaterdm
    )

@APP.route("/message/react/v1",methods=["POST"])
def message_react():
    info = request.get_json()
    token = info["token"]
    message_id = info["message_id"]
    react_id = info["react_id"]

    message_react = message_react_v1(token, message_id, react_id)

    return dumps(
        message_react
    )

@APP.route("/message/unreact/v1",methods=["POST"])
def message_unreact():
    info = request.get_json()
    token = info["token"]
    message_id = info["message_id"]
    react_id = info["react_id"]

    message_unreact = message_unreact_v1(token, message_id, react_id)

    return dumps(
        message_unreact
    )

@APP.route("/message/pin/v1",methods=["POST"])
def message_pin():
    info = request.get_json()
    token = info["token"]
    message_id = info["message_id"]

    message_pin = message_pin_v1(token, message_id)

    return dumps(
        message_pin
    )

@APP.route("/message/unpin/v1",methods=["POST"])
def message_unpin():
    info = request.get_json()
    token = info["token"]
    message_id = info["message_id"]

    message_unpin = message_unpin_v1(token, message_id)

    return dumps(
        message_unpin
    )

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
