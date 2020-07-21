from dataclasses import dataclass
from typing import List
from unittest import TestCase

from panamap import Mapper
from panamap_proto import ProtoMappingDescriptor

from tests.messages_pb2 import Simple, Container, ListOfSimple


@dataclass
class SimpleData:
    value: str


@dataclass
class BadCasedData:
    Va_LuE: str


@dataclass
class ContainerData:
    value: SimpleData


@dataclass
class ListOfSimpleData:
    value: List[SimpleData]


class TestProtoMapping(TestCase):
    def test_simple_proto_mapping(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, SimpleData).map_matching().register()

        s = mapper.map(SimpleData("abc"), Simple)

        self.assertEqual(s.__class__, Simple)
        self.assertEqual(s.value, "abc")

        d = mapper.map(Simple(value="def"), SimpleData)

        self.assertEqual(d.__class__, SimpleData)
        self.assertEqual(d.value, "def")

    def test_simple_proto_mapping_with_ignore_case(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, BadCasedData).map_matching(ignore_case=True).register()

        s = mapper.map(BadCasedData("abc"), Simple)

        self.assertEqual(s.__class__, Simple)
        self.assertEqual(s.value, "abc")

        d = mapper.map(Simple(value="def"), BadCasedData)

        self.assertEqual(d.__class__, BadCasedData)
        self.assertEqual(d.Va_LuE, "def")

    def test_container_proto_mapping(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, SimpleData).map_matching().register()
        mapper.mapping(Container, ContainerData).map_matching().register()

        proto = mapper.map(ContainerData(SimpleData("abc")), Container)

        self.assertEqual(proto.__class__, Container)
        self.assertEqual(proto.value.__class__, Simple)
        self.assertEqual(proto.value.value, "abc")

        data = mapper.map(Container(value=Simple(value="def")), ContainerData)

        self.assertEqual(data.__class__, ContainerData)
        self.assertEqual(data.value.__class__, SimpleData)
        self.assertEqual(data.value.value, "def")

    def test_list_to_proto_mapping(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, SimpleData).map_matching().register()
        mapper.mapping(ListOfSimple, ListOfSimpleData).map_matching().register()

        proto = mapper.map(ListOfSimpleData([SimpleData("abc"), SimpleData("def")]), ListOfSimple)

        self.assertEqual(proto.__class__, ListOfSimple)
        self.assertEqual(len(proto.value), 2)
        self.assertEqual(proto.value[0].__class__, Simple)
        self.assertEqual(proto.value[0].value, "abc")
        self.assertEqual(proto.value[1].__class__, Simple)
        self.assertEqual(proto.value[1].value, "def")

        data = mapper.map(ListOfSimple(value=[Simple(value="123"), Simple(value="xyz")]), ListOfSimpleData)
        self.assertEqual(data.__class__, ListOfSimpleData)
        self.assertEqual(len(data.value), 2)
        self.assertEqual(data.value[0].__class__, SimpleData)
        self.assertEqual(data.value[0].value, "123")
        self.assertEqual(data.value[1].__class__, SimpleData)
        self.assertEqual(data.value[1].value, "xyz")
