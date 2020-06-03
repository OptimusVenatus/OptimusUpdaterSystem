import os
import os.path
from flask import Flask
from flask_autoindex import AutoIndex


class cdn :
    app = Flask(__name__)
    AutoIndex(app, browse_root=os.path.curdir)
    @app.route('/list')
    def list():
        r=[]
        f=[os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(os.getcwd())
        for f in files]
        for i in range(-1,len(f)-1) :
            s=str(f[i]).replace(str(os.getcwd()),'')
            s=s.replace('\\','/')
            r.append(s[1:len(s)])
        return str(r)

if __name__ == '__main__':
    cdn.app.run()
