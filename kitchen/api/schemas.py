from marshmallow import Schema, fields, validate, EXCLUDE

class OrderItemSchema(Schema):
    class Meta:
        # 未知のプロパティは禁止する
        unknown = EXCLUDE
    product = fields.String(required=True)
    size = fields.String(
                        required=True,
                        validate=validate.OneOf(["small", "medium", "large"])
    )
    quantity = fields.Integer(
                            required=True,
                            validate=validate.Range(min=1, min_inclusive=True)
    )


class ScheduleOrderSchema(Schema):
    class Meta:
        # 未知のプロパティは禁止する
        unknown = EXCLUDE
    order = fields.List(fields.Nested(OrderItemSchema), required=True)

class GetScheduledOrderSchema(ScheduleOrderSchema):
    id = fields.UUID(required=True)
    scheduled = fields.DateTime(required=True)
    status = fields.String(
                required=True,
                validate=validate.OneOf(
                    ["pending", "progress", "cancelled", "finished"]
                )
            )

class GetScheduledOrdersSchema(Schema):
    class Meta:
        # 未知のプロパティは禁止する
        unknown = EXCLUDE
    
    schedules = fields.List(
        fields.Nested(GetScheduledOrderSchema),
        required=True
    )
    
class ScheduleStatusSchema(Schema):
    class Meta:
        # 未知のプロパティは禁止する
        unknown = EXCLUDE
    status = fields.String(
                required=True,
                validate=validate.OneOf(
                    ["pending", "progress", "cancelled", "finished"]
                )
            )