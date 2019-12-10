from flask import Blueprint, jsonify, request
from project.api.models import User
from project import db
from sqlalchemy import exc

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/ping', methods=['GET'])
def ping_ping():
    return jsonify({'status': 'success', 'message': 'pong!'})


@user_blueprint.route('/user', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_data = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_data), 400

    email = post_data.get('email')
    username = post_data.get('username')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()

            response_data = {
                'status': 'success',
                'message': '%s was added!' % post_data['email']
            }
            return jsonify(response_data), 201

        response_data = {
            'status': 'fail',
            'message': 'Sorry. That email already exists.'
        }
        return jsonify(response_data), 400
    except exc.IntegrityError:
        db.session.rollback()  # 出现异常了，回滚
        response_data = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_data), 400


@user_blueprint.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户的详细信息"""
    if not user_id.isdigit():
        return jsonify({'status': 'fail', 'message': 'Param id error'}), 400

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({
            'status': 'fail',
            'message': 'User does not exist'
        }), 404

    response_object = {
        'status': 'success',
        'data': {
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
    }
    return jsonify(response_object), 200


@user_blueprint.route('/user/list', methods=['GET'])
def user_list():
    """获取用户列表"""
    users = User.query.filter_by(active=1).all()
    data = {
        'users': [{
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'created_at': user.created_at
        } for user in users]
    }
    return jsonify({'data': data, 'status': 'success'}), 200
