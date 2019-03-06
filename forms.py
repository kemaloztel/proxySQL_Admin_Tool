from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UserForm(FlaskForm):

    username = StringField('username: ')
    password = StringField('password: ')
    active = StringField('active: ')
    use_ssl = StringField('use_ssl: ')
    default_hostgroup = StringField('default_hostgroup: ')
    default_schema = StringField('default_schema: ')
    schema_locked = StringField('schema_locked: ')
    transaction_persistent = StringField('transaction_persistent: ')
    fast_forward = StringField('fast_forward: ')
    backend = StringField('backend: ')
    frontend = StringField('frontend: ')
    max_connections = StringField('max_connections: ')


class IntoForm(FlaskForm):

    hostgroup_id = StringField('hostgroup_id: ')
    hostname = StringField('hostname: ')
    port = StringField('port: ')
    status = StringField('status: ')
    weight = StringField('weight: ')
    compression = StringField('compression: ')
    max_connections = StringField('max_connections: ')
    max_replication_lag = StringField('max_replication_lag: ')
    use_ssl = StringField('use_ssl: ')
    max_latency_ms = StringField('max_latency_ms: ')
    comment = StringField('comment: ')


class ProxyForm(FlaskForm):

    hostname = StringField('hostname: ')
    port = StringField('port: ')
    weight = StringField('weight: ')
    comment = StringField('comment: ')