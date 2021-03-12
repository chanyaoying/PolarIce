import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db_session, Room as RoomModel


class Room(SQLAlchemyObjectType):
    class Meta:
        model = RoomModel
        interfaces = (relay.Node, )


# class Employee(SQLAlchemyObjectType):
#     class Meta:
#         model = EmployeeModel
#         interfaces = (relay.Node, )


class Query(graphene.ObjectType): #root  type for GQL
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_rooms = SQLAlchemyConnectionField(Employee.connection)
    
    # Disable sorting over this field
    # all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)

schema = graphene.Schema(query=Query)