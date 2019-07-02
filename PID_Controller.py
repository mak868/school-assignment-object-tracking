import datetime

class PID:

    def __init__(self):
        self.__Kp = 0
        self.__Ki = 0
        self.__Kd = 0
        self.__sumError = 0
        self.__lastError = 0
        self.__target = 0
        self.__value = 0
        self.__maxValue = 1
        self.__lastTime = datetime.datetime.now()

    def setKp(self, newValue):
        self.__Kp = newValue

    def setKi(self, newValue):
        self.__Ki = newValue

    def setKd(self, newValue):
        self.__Kd = newValue

    def setTarget(self, target):
        self.__target = target

    def setMaxValue(self, newValue: int):
        self.__maxValue = newValue

    def getValue(self) -> int:
        return self.__value

    def process(self, current : int):
        now = datetime.datetime.now()
        interval = now - self.__lastTime
        dt = (interval.microseconds / 1000) / 1000 # bring to seconds

        self.__lastTime = now
        error = self.__target - current
        self.__sumError = self.__sumError + (error * dt)   # *dt   #clipping

        minSumError = -50
        maxSumError = 50
        self.__sumError = sorted((minSumError, maxSumError, self.__sumError))[1]


        derivError = (error - self.__lastError) / dt      # /dt
        self.__lastError = error

        proportional = self.__Kp * error
        integral = self.__Ki * self.__sumError
        derivative = self.__Kd * derivError

        pidValue = int(proportional + integral + derivative + 50)

        #print("P: {} - I: {} - D: {} PID: {} - Target: {} - Current: {} - error: {}".format(proportional, integral, derivative, pidValue, self.__target, current, error))

        if (pidValue > self.__maxValue):
            self.__value = self.__maxValue
        elif (pidValue < 0):
            self.__value = 0
        else:
            self.__value = pidValue
