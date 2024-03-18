from sqlalchemy.orm import declarative_base
import sqlalchemy as sa
from datetime import datetime

base = declarative_base()


class Member(base):
    __tablename__ = 'Member'

    idx = sa.Column(
        sa.Integer,
        primary_key=True,
        default=None,
        comment='PK'
    )
    username = sa.Column(
        sa.VARCHAR(16),
        nullable=True,
        default=None,
        comment='아이디'
    )
    password = sa.Column(
        sa.CHAR(41),
        nullable=True,
        default=None,
        comment='비밀번호'
    )
    name = sa.Column(
        sa.VARCHAR(30),
        nullable=True,
        default=None,
        comment='이름'
    )
    created_at = sa.Column(
        sa.DATETIME,
        nullable=True,
        default=datetime.now().isoformat(),
        comment='생성시간'
    )
