import uuid

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from .models import TunnelModel
from .utils import get_random_open_local_port
from .utils import is_port_in_use
from .utils import status_remote
from .utils import stop_and_delete


class TunnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TunnelModel
        fields = [
            "startuuidcode",
            "hostname",
            "local_port",
            "svc_port",
            "target_node",
            "target_port",
        ]

    def is_valid(self, raise_exception=False):
        required_keys = [
            "startuuidcode",
            "hostname",
            "svc_port",
            "target_node",
            "target_port",
        ]
        for key in required_keys:
            if key not in self.initial_data.keys():
                self._validated_data = []
                self._errors = [f"Missing key in input data: {key}"]
                raise ValidationError(self._errors)

        startuuidcode = self.initial_data["startuuidcode"]
        prev_model = TunnelModel.objects.filter(startuuidcode=startuuidcode).first()
        if prev_model is not None:
            stop_and_delete(**prev_model.__dict__)
            prev_model.delete()
        return super().is_valid(raise_exception=raise_exception)

    def to_internal_value(self, data):
        data["local_port"] = get_random_open_local_port()
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["running"] = is_port_in_use(instance.local_port)
        return ret


class RemoteSerializer(Serializer):
    def is_valid(self, raise_exception=False):
        _errors = {}
        required_keys = ["hostname"]
        for key in required_keys:
            if key not in self.initial_data.keys():
                self._validated_data = []
                _errors = [f"Missing key in input data: {key}"]
        if _errors and raise_exception:
            raise ValidationError(_errors)
        return super().is_valid(raise_exception)

    def to_internal_value(self, data):
        uuidcode = (
            self.context["request"]
            .query_params.dict()
            .get("uuidcode", uuid.uuid4().hex)
        )
        data["uuidcode"] = uuidcode
        data["running"] = status_remote(alert_admins=True, raise_exception=True, **data)
        return data