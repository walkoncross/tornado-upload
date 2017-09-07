import os.path as osp
import os
import random
import string

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options

define("port", default=8899, help="run on the given port", type=int)

default_save_dir = './uploads'

print "Default save dir: " + default_save_dir
if not osp.exists(default_save_dir):
    print "Create defulat save dir: " + default_save_dir
    os.makedirs(default_save_dir)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_form.html")


class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        # print 'request.arguments', self.request.arguments
        # print 'request.query_arguments', self.request.query_arguments
        # print 'request.body_arguments', self.request.body_arguments

        save_dir = self.request.arguments['save_dir'][0]
        if not osp.exists(save_dir):
            save_dir = default_save_dir

        original_fname = file1['filename']
        print "Received file: " + original_fname

        save_fname = osp.join(save_dir, original_fname)

        if osp.exists(save_fname):
            splits = osp.splitext(save_fname)
            fname = ''.join(random.choice(
                string.ascii_lowercase + string.digits) for x in range(6))
            save_fname = splits[0] + '_' + fname + splits[1]

        output_file = open(save_fname, 'wb')
        output_file.write(file1['body'])
        output_file.close()

        print "file %s is uploaded, saved as %s" % (original_fname, save_fname)
        self.finish("file %s is uploaded, saved as %s" %
                    (original_fname, save_fname))


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
