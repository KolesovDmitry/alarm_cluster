import uuid

def uniq_name(prefix='nd_'):
    return prefix + uuid.uuid4().hex



