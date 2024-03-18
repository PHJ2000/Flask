from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, validators
from wtforms.validators import InputRequired, AnyOf, NumberRange, Length, EqualTo, Regexp, ValidationError
from src.database import session
from src.model import Member


class SearchForm(FlaskForm):
    search_type = StringField(
        'search_type', validators=[]
    )

    search_text = StringField(
        'search_text', validators=[]
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.search_type.validators = [
            InputRequired(
                message="Search type is required."
            ),
            validators.AnyOf(
                ['all', 'username', 'name']
            ),
            validators.Length(
                min=3,
                max=8,
                message = "Search type must be between 3 to 8 characters long."
            )
        ]

        self.search_text.validators = [
            InputRequired(
                message="Search text is required."
            ),
            validators.Length(
                max=16,
                message="Search text must be up to 50 characters long."
            )
        ]


class CreateMemberForm(FlaskForm):
    username = StringField(
        'username', validators=[]
    )

    password = PasswordField(
        'password', validators=[]
    )

    password_match = PasswordField(
        'password_match', validators=[]
    )

    name = StringField(
        'name', validators=[]
    )

    def __init__(self, *args, **kwargs):
        super(CreateMemberForm, self).__init__(*args, **kwargs)

        self.username.validators = [
            InputRequired(
                message="Username is required."
            ),
            validators.Regexp(
                r'^(?=.*\d)[a-z][a-z0-9]{3,15}$',
                message="Username must be 4-16 characters, start with a letter, and include a number."
            )
        ]

        self.password.validators = [
            InputRequired(
                message="Password is required."
            ),
            validators.Length(
                min=8,
                max=16,
                message="Password must be between 8 and 16 characters long."
            )
        ]

        self.password_match.validators = [
            InputRequired(
                message="Password confirmation is required."
            ),
            validators.EqualTo(
                'password',
                message="Passwords must match"
            )
        ]

        self.name.validators = [
            InputRequired(
                message="Name is required."
            ),
            validators.Regexp(
                '^[가-힣]{2,10}$',
                message="Name must be in Korean and between 2 and 10 characters long"
            )
        ]

    def validate_username(self, field):
        if session.query(Member).filter(Member.username == field.data).first():
            raise ValidationError('Username already exists.')


class MemberDetailsForm(FlaskForm):
    member_idx = IntegerField(
        'member Index', validators=[]
    )

    def __init__(self, *args, **kwargs):
        super(MemberDetailsForm, self).__init__(*args, **kwargs)

        self.member_idx.validators = [
            NumberRange(
                min=1,
                max=999999,
                message="Member index must be between 1 and 999999."
            )
        ]


class UpdateMemberForm(FlaskForm):
    member_idx = IntegerField(
        'member Index', validators=[]
    )

    old_password = PasswordField(
        'old Password', validators=[]
    )

    new_password = PasswordField(
        'New Password', validators=[]
    )

    new_password_match = PasswordField(
        'Confirm New Password', validators=[]
    )

    name = StringField(
        'Name', validators=[]
    )

    def __init__(self, member_idx=None, *args, **kwargs):
        super(UpdateMemberForm, self).__init__(*args, **kwargs)
        self.member_idx = member_idx

        self.member_idx.validators = [
            NumberRange(
                min=1,
                max=999999,
                message="Member index must be between 1 and 999999."
            )
        ]

        self.old_password.validators = [
            InputRequired(
                message="Old password is required."
            ),
            validators.Length(
                min=8,
                max=16,
                message="Old Password must be between 8 and 16 characters long"
            )
        ]

        self.new_password.validators = [
            InputRequired(
                message="New password is required."
            ),
            validators.Length(
                min=8,
                max=16,
                message="New Password must be between 8 and 16 characters long"
            )
        ]

        self.new_password_match.validators = [
            InputRequired(
                message="Confirmation of new password is required."
            ),
            validators.EqualTo(
                'newPassword',
                message="New passwords must match"
            )
        ]

        self.name.validators = [
            InputRequired(
                message="Name is required."
            ),
            validators.Regexp(
                '^[가-힣]{2,10}$',
                message="Name must be in Korean and between 2 and 10 characters long"
            )
        ]

    def validate_old_password(self, field):
        if session.query(Member).filter(Member.password == field.data).first():
            raise ValidationError('Old Password already exists.')

    def validate_new_password(self, field):
        if field.data == self.old_password.data:
            raise ValidationError('New password must be different from the old password.')


class DeleteMemberForm(FlaskForm):
    member_idx = IntegerField(
        'member Index', validators=[]
    )

    def __init__(self, *args, **kwargs):
        super(DeleteMemberForm, self).__init__(*args, **kwargs)

        self.member_idx.validators = [
            NumberRange(
                min=1,
                max=999999,
                message="Member index must be between 1 and 999999."
            )
        ]


'''
    def validate_oldPassword(self, field):
        # 데이터베이스에서 현재 로그인한 사용자의 비밀번호를 가져오는 로직
        # 여기서는 flask_login의 current_user를 사용
        user_password_hash = current_user.password

        # 입력된 oldPassword와 데이터베이스의 비밀번호를 비교
        if not check_password_hash(user_password_hash, field.data):
            raise validators.ValidationError('Old password is incorrect.')
'''
