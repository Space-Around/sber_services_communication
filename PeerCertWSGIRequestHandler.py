import werkzeug.serving
import OpenSSL


class PeerCertWSGIRequestHandler(werkzeug.serving.WSGIRequestHandler):

    def make_environ(self):
        environ = super(PeerCertWSGIRequestHandler, self).make_environ()
        x509_binary = self.connection.getpeercert(True)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, x509_binary)
        environ['peercert'] = x509
        return environ