from datetime import datetime,timedelta

class ProxyModel(object):
    def __init__(self,data):
        self.ip=data['IP']
        self.port = data['Port']
        self.expire_str=data['ExpireTime']

        data_str,time_str=self.expire_str.split(' ')
        year,month,day=data_str.split('-')
        hour,minute,second=time_str.split(':')
        self.expire_time=datetime(year=int(year),month=int(month),day=int(day)
                                 ,hour=int(hour),minute=int(minute),second=int(second))
        self.proxy="https://{}:{}".format(self.ip,self.port)

    @property
    def is_expiring(self):
        now=datetime.now()
        if (self.expire_time-now)<timedelta(seconds=5):
            return True
        else:
            return False