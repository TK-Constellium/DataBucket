This should be an Datamanagement extension on top of Django ORM.

Prototype:
```python
class Project(DataBucket):

    cache_invalidation = {
        "interval": 60 * 60 * 24,
        "refetch_url": "https://www.example.com/api/v1/data",
        "on_change": False,
    }

    class DataInterface(Database):
        name = String(
            max_length=100, is_unique=True, is_required=True, is_changeable=True
        )

        customer = DataBucketConnection(
            DataBucket="Customer",
            type="ManyToMany",
            is_required=True,
            on_delete=dbField.CASCADE,
        )

        shipment = Number(
            decimal_places=2,
            default=0.0,
            unit=WeightUnit.TONNES,
        )

        currency = DataBucketConnection(
            DataBucket="Currency",
            type="ForeignKey",
            is_required=True,
            on_delete=dbField.SET_NULL,
        )

        revenue = Number(
            decimal_places=2,
            default=0.0,
            unit=currency,
        )

        class Meta:
            validation = [
                ["name", "matches regex", r"^[a-zA-Z0-9_]*$"],
            ]

            unique_together = [["name", "customer"]]

```