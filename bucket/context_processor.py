from .bucket import Bucket


def bucket(request):
    return {'bucket': Bucket(request)}
