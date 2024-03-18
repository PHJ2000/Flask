from flask import Blueprint, jsonify, request

from src.model import Member
#from src.database import session
from src.app import db
from src.wtf import (
    CreateMemberForm, UpdateMemberForm,
    DeleteMemberForm, SearchForm, MemberDetailsForm
)
bp = Blueprint('v1_member', __name__)
"""
Blueprint를 가지고, /member로 접근한 URL을 처리하는 파일
GET /member
[params]
searchType all/username/name
searchText

[response]
idx
username
name
createdAt
반환값을 잘 넘겨줌
"""


def format_errors(error_messages):
    return {"error": "; ".join(["; ".join(msgs) for msgs in error_messages.values()])}


@bp.route('', methods=['GET'])
def get_members():
    form = SearchForm.from_json(request.args)
    if not form.validate():
        return jsonify(format_errors(form.errors)), 400

    pre_query = (
        db.session
        .query(Member)
    )

    if form.search_text.data:
        if form.search_type.data == 'username':
            pre_query = (
                pre_query
                .filter(
                    Member.username.like('%' + form.search_text.data + '%')
                )
            )

        if form.search_type.data == 'name':
            pre_query = (
                pre_query
                .filter(
                    Member.name.like('%' + form.search_text.data + '%')
                )
            )

    pre_query_count = (
        pre_query
        .count()
    )

    pre_query_list = (
        pre_query
        .all()
    )

    result = dict(
        pagination=dict(
            totalRecord=pre_query_count
        ),
        items=[
            dict(
                idx=r.idx,
                username=r.username,
                name=r.name,
                created_at=r.created_at
            )
            for r in pre_query_list
        ]
    )

    return jsonify(result)


"""
멤버에 idx가 일치하는 쿼리를 하나 또는 없음으로 반환한다.
"""


def get_member_by_idx(member_idx):
    return db.session.query(Member)\
        .filter(Member.idx == member_idx)\
        .one_or_none()


"""
POST /member
[data]
username: 아이디 (영소문자로 시작하는 4~16자리의 영소문자/숫자 조합)
password: 비밀번호 (8~16자리의 아무 문자)
passwordMatch: 비밀번호 확인 (8~16자리의 아무 문자)
name: 이름 (2~10자리의 한글)
"""


@bp.route('', methods=['POST'])
def create_member():
    form = CreateMemberForm.from_json(request.json)

    if not form.validate():
        return jsonify(format_errors(form.errors)), 400

    m = Member(
        username=form.username.data,
        password=form.password.data,
        name=form.name.data
    )

    try:
        db.session.add(m)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)  # 오류 출력
        return jsonify(dict(
            error='Register failed'
        )), 500

    return jsonify(dict(
        data=[
            dict(
                idx=m.idx,
                username=m.username,
                password=m.password,
                name=m.name
            )
        ]
    )), 201


"""
member_idx가 일치하는 멤버를 반환한다.
"""


# GET /member/<int:member_idx>
@bp.route('/<int:member_idx>', methods=['GET'])
def get_member_idx(member_idx):
    m = db.session.query(Member)\
        .filter(Member.idx == member_idx)\
        .one_or_none()

    if not m:
        return jsonify(dict(
            msg='Member not found'
        )), 404

    return jsonify(
        dict(
            data=[
                dict(
                    idx=m.idx,
                    username=m.username,
                    name=m.name,
                    created_at=m.created_at
                )
            ]
        )
    ), 200


"""
member_idx에 해당하는 멤버를 수정한다.
"""


# PUT /member/<int:member_idx>
@bp.route('/<int:member_idx>', methods=['PUT'])
def update_member(member_idx):
    form = UpdateMemberForm(member_idx, **request.json)

    if not form.validate():
        return jsonify(format_errors(form.errors)), 400

    m = db.session.query(Member)\
        .filter(Member.idx == member_idx)\
        .one_or_none()

    if not m:
        return jsonify(dict(
            msg='Member not found'
        )), 404

    # 데이터베이스에 멤버 추가 시도
    try:
        m.password = form.password.data
        m.name = form.name.data
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)  # 오류 출력
        return jsonify(dict(
            msg='Update failed'
        )), 500

    return jsonify()


"""
member_idx에 해당하는 멤버를 삭제한다.
"""


# DELETE /member/<int:member_idx>
@bp.route('/<int:member_idx>', methods=['DELETE'])
def delete_member(member_idx):
    m = db.session.query(Member)\
        .filter(Member.idx == member_idx)\
        .one_or_none()

    if not m:
        return jsonify(dict(
            msg='Member not found'
        )), 404

    try:
        db.session.delete(m)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)  # 오류 출력
        return jsonify(dict(
            msg='Deletion failed'
        )), 500

    return jsonify()
