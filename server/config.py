class ServerConfig:

    def __init__(self, base_delay=8, var_delay=5, success_rate=0.8):
        # unit is in second
        # total delay is BASE_DELAY + random(VAR_DELAY)
        self.base_delay = base_delay
        self.var_delay = var_delay
        # request success rate
        self.success_rate = success_rate

    def set_base_delay(self, base_delay):
        self.base_delay = base_delay

    def set_var_delay(self, var_delay):
        self.var_delay = var_delay

    def set_success_rate(self, success_rate):
        self.success_rate = success_rate

    def __str__(self):
        return f"base_delay: {self.base_delay}\nvar_delay: {self.var_delay}\bsuccess_rate: {self.success_rate}"
