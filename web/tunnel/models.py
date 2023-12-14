from django.db import models


class TunnelModel(models.Model):
    servername = models.TextField(primary_key=True)
    hostname = models.TextField(null=False, max_length=32)
    local_port = models.IntegerField(null=False)
    svc_name = models.TextField(null=False)
    svc_port = models.IntegerField(null=False)
    target_node = models.TextField(null=False, max_length=32)
    target_port = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    tunnel_pod = models.TextField(null=False, default="drf-tunnel-0")
    jhub_userid = models.TextField(null=False, default="0")
    jhub_credential = models.TextField("jhub_credential", default="jupyterhub")

    def __str__(self):
        return self.servername
