from flask import Flask, render_template, request, redirect, url_for, sessions, session, json, jsonify, flash
from forms import LoginForm, UserForm, IntoForm, ProxyForm
from flask_wtf.csrf import CSRFProtect
from printscreen import servers_print, proxy_print, users_print
from useroperation import adduser, rmuser, activeuser, deactiveuser, veri_ekle, user_config_load, user_config_save, \
    update_user
from serveroperation import add, clear, cevrimici, offlinesoft, offlinehard, server_config_load, server_config_save, \
    update_server
from proxyoperation import proxy_config_save, proxy_config_load, remove_proxy, add_proxy, update_proxy
from navbar import populate_pools_session, populate_proxy_session
from errorhandlers import errors

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.register_blueprint(errors)


@app.route("/")
@app.route("/homepage", methods=['GET', 'POST'])
def anasayfa():
    pools = populate_pools_session ()
    servers = populate_proxy_session ()

    if request.method == 'POST':
        session['host'] = request.form['server_select']

    return render_template('layout.html', pools=pools, servers=servers)


@app.route("/mysql/server", methods=['GET', 'POST'])
def mysql():
    pools = populate_pools_session ()
    servers = populate_proxy_session ()

    host = session.get ('host', 'not set')
    try:
        return render_template('/printers/mysqlservers.html', serverlists=servers_print(host), pools=pools, servers=servers)
    except:
        return render_template('/errors/connect_error.html')


@app.route("/proxy/server", methods=['GET'])
def proxysqlservers():
    pools = populate_pools_session()
    servers = populate_proxy_session()

    x = session.get('host', 'not set')
    try:
        return render_template('/printers/proxyservers.html', proxylist=proxy_print(x), pools=pools, servers=servers)
    except:
        return render_template('/errors/connect_error.html')

@app.route ("/mysql/user")
def users():
    pools = populate_pools_session()
    servers = populate_proxy_session()

    y = session.get('host', 'not set')
    try:
        return render_template('/printers/mysqlusers.html', userlists=users_print(y), pools=pools, servers=servers)
    except:
        return render_template('/errors/connect_error.html')


@app.route('/summary')
def summary():
    d = {'deneme': 1234}
    return jsonify(d)


@app.route("/mysql/user/operation", methods=['GET', 'POST'])
def user_operation():
    if request.method == 'POST':
        if request.form['user_button'] == 'Add':
            return render_template('/insert/adduser.html')
        elif request.form['user_button'] == 'Remove':
            degerler = request.form.getlist('selectbox')
            if degerler:
                for item in degerler:
                    username, backend, frontend = item.split(':')
                    rmuser(username, backend, frontend)
            else:
                flash('Please select one in order to remove')

        elif request.form['user_button'] == 'Active':
            degerler = request.form.getlist('selectbox')
            if degerler:
                for item in degerler:
                    username, backend, frontend = item.split (':')
                    activeuser(username, backend, frontend)
            else:
                flash('Please select one for active')


        elif request.form['user_button'] == 'Deactive':
            degerler = request.form.getlist('selectbox')
            if degerler:
                for item in degerler:
                    username, backend, frontend = item.split (':')
                    deactiveuser(username, backend, frontend)
            else:
                flash ('Please select one for deactive')

        elif request.form['user_button'] == 'Update':
            degerler = request.form.getlist('selectbox')
            if degerler:
                for item in degerler:
                    u, b, f = item.split(':')
                try:
                    return render_template('/update/updatemysqluser.html', username=u, backend=b, frontend=f)
                except:
                    flash(' Please select one in order to update !', 'message')

        else:
            pass
    x = session.get('host', 'not set')
    return render_template('mysqlusers.html', userlists=users_print(x))


@app.route ("/proxy/operation", methods=['GET', 'POST'])
def proxy_operation():
    if request.method == 'POST':
        if request.form['proxy_button'] == 'Remove':
            degerler = request.form.getlist('selectedcheck')
            if degerler:
                for item in degerler:
                    hostname, port = item.split('_')
                    remove_proxy (hostname, port)
            else:
                flash (' Please select one in order to remove !')

        elif request.form['proxy_button'] == 'Update':
            degerler = request.form.getlist('selectedcheck')
            for item in degerler:
                k, l = item.split('_')
            try:
                return render_template('/update/updateproxy.html', hostname=k, port=l)
            except:
                flash(' Please select one in order to update !')

        elif request.form['proxy_button'] == 'Add':
            return render_template('/insert/addproxy.html')

    x = session.get('host', 'not set')
    return render_template('/printers/proxyservers.html', proxylist=proxy_print (x))


@app.route ("/mysql/server/operation", methods=['GET', 'POST'])
def server_operation():
    if request.method == 'POST':
        if request.form['postButton'] == 'Delete':
            degerler = request.form.getlist('selected')
            for item in degerler:
                hg, hostname, port = item.split ('_')
                clear(hg, hostname, port)

        if request.form['selectType'] == 'ONLINE':
            degerler = request.form.getlist('selected')
            for item in degerler:
                hg, hostname, port = item.split('_')
                cevrimici(hg, hostname, port)

        elif request.form['selectType'] == 'OFFLINE_SOFT':
            degerler = request.form.getlist('selected')
            for item in degerler:
                hg, hostname, port = item.split('_')
                offlinesoft(hg, hostname, port)

        elif request.form['selectType'] == 'OFFLINE_HARD':
            degerler = request.form.getlist('selected')
            for item in degerler:
                hg, hostname, port = item.split('_')
                offlinehard(hg, hostname, port)

        if request.form['postButton'] == 'Add':
            return render_template('/insert/addserver.html')

        elif request.form['postButton'] == 'Update':
            degerler = request.form.getlist('selected')
            for item in degerler:
                hg, hn, p = item.split('_')
                return render_template('/update/updatemysqlserver.html', hostgroup_id=hg, hostname=hn, port=p)

        else:
            pass

    x = session.get('host', 'not set')
    return render_template('/printers/mysqlservers.html', serverlists=servers_print(x))


@app.route ('/mysql/config', methods=['POST'])
def servers_config():
    if request.form['config'] == 'Load_Runtime':
        server_config_load()
        x = session.get('host', 'not set')
        return render_template('/printers/mysqlservers.html', serverlists=servers_print(x))
    elif request.form['config'] == 'Save_Disk':
        server_config_save()
        x = session.get('host', 'not set')
        return render_template('/printers/mysqlservers.html', serverlists=servers_print(x))
    else:
        pass


@app.route('/proxy/config', methods=['POST'])
def proxy_config():
    if request.form['config'] == 'Load_Runtime':
        proxy_config_load()
        x = session.get('host', 'not set')
        return render_template('/printers/proxyservers.html', proxylist=proxy_print(x))
    elif request.form['config'] == 'Save_Disk':
        proxy_config_save()
        x = session.get('host', 'not set')
        return render_template('/printers/proxyservers.html', proxylist=proxy_print(x))
    else:
        pass


@app.route('/mysql/user/operation/config', methods=['POST'])
def users_config():
    if request.form['config'] == 'Load_Runtime':
        user_config_load()
        x = session.get('host', 'not set')
        return render_template('mysqlusers.html', userlists=users_print(x))
    elif request.form['config'] == 'Save_Disk':
        user_config_save()
        x = session.get('host', 'not set')
        return render_template('/printers/mysqlusers.html', userlists=users_print(x))
    else:
        pass


@app.route('/mysql/server/operation/addedserver', methods=['POST'])
def added():
    form = IntoForm (request.form)  # IntoForm imported from server_form.py
    if request.method == "POST":
        add (form)
        x = session.get ('host', 'not set')
        return render_template('/printers/mysqlservers.html', serverlists=servers_print(x))
    else:
        print ('Formda sorun var')


@app.route('/mysql/user/operation/addeduser', methods=['POST'])
def addeduser():
    form = UserForm (request.form)  # UserForm imported from user_form.py
    if request.method == "POST":
        adduser(form)
        x = session.get ('host', 'not set')
        return render_template('/printers/mysqlusers.html', userlists=users_print(x))
    else:
        print ('Formda sorun var')


@app.route('/proxy/operation/addedproxy', methods=['POST'])
def addedproxy():
    form = ProxyForm (request.form)
    if request.method == 'POST':
        try:
            add_proxy(form)
            x = session.get('host', 'not set')
            return render_template('/printers/proxyservers.html', proxylist=proxy_print (x))
        except:
            return render_template('error.html')

    else:
        print ('Formda sorun var')


@app.route('/proxy/operation/updatedproxy/<hostname>/<port>', methods=['POST'])
def updatedproxy(hostname, port):
    form = ProxyForm(request.form)
    print(form)
    try:
        update_proxy(form, hostname, port)
        x = session.get('host', 'not set')
        return render_template('/printers/proxyservers.html', proxylist=proxy_print (x))
    except Exception as e:
        print(e)
        return render_template('/errors/update_error.html', error=e)


@app.route('/mysql/server/operation/updated_mysql_server/<hg_id>/<hostname>/<port>', methods=['POST'])
def updated_mysql_server(hg_id, hostname, port):
    form = IntoForm(request.form)
    try:
        update_server(form, hg_id, hostname, port)
        x = session.get('host', 'not set')
        return render_template('/printers/mysqlservers.html', serverlists=servers_print(x))
    except Exception as e:
        print(e)
        return render_template('/errors/update_error.html', error=e)


@app.route('/mysql/user/operation/updated_mysql_user/<uname>/<bckend>/<frntend>', methods=['POST'])
def updated_mysql_user(uname, bckend, frntend):
    form = UserForm(request.form)
    try:
        update_user(form, uname, bckend, frntend)
        x = session.get('host', 'not set')
        return render_template('/printers/mysqlusers.html', userlists=users_print(x))
    except Exception as e:
        print(e)
        return render_template('/errors/update_error.html', error=e)



@app.route ("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # LoginForm imported from forms.py
    if form.validate_on_submit():
        if form.email.data == 'admin@ebay.com' and form.password.data == '12345':
            return redirect(url_for('anasayfa'))
    return render_template('login.html', title='Login', form=form)
