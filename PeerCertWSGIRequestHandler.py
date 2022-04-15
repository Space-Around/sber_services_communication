from typing import Any

import werkzeug.serving
import OpenSSL


class PeerCertWSGIRequestHandler(werkzeug.serving.WSGIRequestHandler):
    """Handle request from client"""

    def make_environ(self) -> dict[str, Any]:
        """Serialise client and server cert"""

        environ = super(PeerCertWSGIRequestHandler, self).make_environ()
        x509_binary = self.connection.getpeercert(True)

        server_cert_x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, x509_binary)
        client_cert_x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, environ['SSL_CLIENT_CERT'])

        environ['server_cert'] = server_cert_x509
        environ['client_cert'] = client_cert_x509

        return environ
