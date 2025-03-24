from odmantic import Model, ObjectId


class Category(Model):
    title: str
    description: str
    owner_id: ObjectId
