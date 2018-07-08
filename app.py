import tornado.ioloop
import tornado.web
import tornado.log

import os
import boto3

client = boto3.client(
  'ses',
  region_name='us-east-1',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)

from jinja2 import \
    Environment, PackageLoader, select_autoescape
  
ENV = Environment(
    loader=PackageLoader('myapp', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        name = self.get_query_argument('name', 'Vistor')
        self.render_template("hello.html", {'name': name})


def send_email(name, email, comments):
    response = client.send_email(
      Destination={
        'ToAddresses': ['joshua.j.ladwig@gmail.com'],
      },
      Message={
        'Body': {
          'Text': {
            'Charset': 'UTF-8',
            'Data': '{} from {} would like to say: {}.'.format(name, email, comments),
          },
        },
        'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
      },
      Source='joshua.j.ladwig@gmail.com',
    )


class FormHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        name = self.get_query_argument('name', 'Page2')
        self.render_template("form.html", {'name': name})
        
    def post(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        first_name = self.get_body_argument('first_name', None)
        user_email = self.get_body_argument('user_email', None)
        user_message = self.get_body_argument('message', None)
        error = ''
        # form args = {first_name, last_name, user_email, message}
        if first_name:
            send_email(first_name, user_email, user_message)
            self.redirect('/form_submitted', {})
        else:
            if(not first_name):
                error = 'You need to enter your name!'
                self.render_template("form.html", {'error':error})


class TipCalcHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        name = self.get_query_argument('name', 'Page2')
        self.render_template("tip_calc.html", {'name': name})
        
    def post(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        bill_total = self.get_body_argument('bill_total', None)
        service = self.get_body_argument('service', None)
        user_message = self.get_body_argument('message', None)
        total_w_tip = 0;
        error = ''
        # tipCalcForm args = {bill_total, good_service, fair_service, bad_service, message}
        if(bill_total == ''):
            error = 'You did not provide your bill total'
            self.render_template("tip_calc.html", {'error': error})
        else:
            if(service == 'good_service'):
                total_w_tip = round(float(bill_total) * 1.2, 2)
            elif(service == 'fair_service'):
                total_w_tip = round(float(bill_total) * 1.15, 2)
            elif(service == 'bad_service'):
                total_w_tip = round(float(bill_total) * 1.10, 2)
            self.render_template("tip_calc.html", {'total_w_tip': total_w_tip})
        # else:
        #     self.render_template("tip_calc.html", {})
       


class FormSuccessHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        name = self.get_query_argument('name', 'Page2')
        self.render_template("form_submitted.html", {})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/form", FormHandler),
        (r"/form_submitted", FormSuccessHandler),
        (r"/tip_calc", TipCalcHandler),
        (
          r"/static/(.*)",
          tornado.web.StaticFileHandler,
          {'path': 'static'}
        ),
    ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    
    app = make_app()
    PORT = int(os.environ.get('PORT', '8888'))
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()