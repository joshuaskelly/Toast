class MathHelper(object):
    @staticmethod
    def Lerp(fromValue, toValue, step):
        return fromValue + (toValue - fromValue) * step