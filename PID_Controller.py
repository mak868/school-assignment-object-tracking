
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

    def setKp(self, newValue : int):
        self.__Kp = newValue

    def setKi(self, newValue : int):
        self.__Kp = newValue

    def setKd(self, newValue : int):
        self.__Kp = newValue

    def setTarget(self, target : int):
        self.__target = target

    def setMaxValue(self, newValue: int):
        self.__maxValue = newValue

    def getValue(self) -> int:
        return self.__value

    def process(self, current : int):
        error = self.__target - current
        self.__sumError = self.__sumError + error
        derivError = error - self.__lastError
        self.__lastError = error

        proportional = self.__Kp * error
        integral = self.__Ki * self.__sumError
        derivative = self.__Kd * derivError

        pidValue = proportional + integral + derivative

        if (pidValue > self.__maxValue):
            self.__value = self.__maxValue
        elif (pidValue < 0):
            self.__value = 0
        else:
            self.__value = pidValue
