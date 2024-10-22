import os, ctypes
from json import load

from .logger import Logger

class Utils:
    def __init__(self):
        self.logger = Logger()

    def set_terminal_title(self, title: str):
        """
        Function to set the terminal title in Windows.

        Args:
        ---------
            title (str): The title to set.
        """
        ctypes.windll.kernel32.SetConsoleTitleW(title)

    def get_icon_b64(self, icon_name: str):
        """
        Function to get an icon's base64 string from the JSON file.
        
        Args:
        ---------
            icon_name (str): The name of the icon to get.
            
        Returns:
        ---------
            str: The base64 string of the icon. If the icon is not found, returns None.
        """

        icons = {
            "title_bar_quit": "iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAYAAADhAJiYAAAAAXNSR0IArs4c6QAAAcFJREFUWEftlj9LHUEUxX9HE1TwqwQS0MZGm6dC2iRFQkBsBEkKy4AgCIKlhZ1CIIH8aZIiRAykSGz0M4gfQ7A8cWAeDKuPmVmFPGW3W+6dub89586dFUP2aMh46IByjnQKdQrlFMjF73YP2Z6V9Df3lf247QfAtKTj0jXFCtl+DXwAdiSt5QrYHgW+AYvAgqQ/uTUhXgRkex44TPK3JK0PKhBhPgEvYs458ETSWQ6qFGgC+A3MJBtuSNpsFrA9AnwFniWxL8BLSb4VoLCJ7QB1AMwlm65J2kl6JsAEW18lOeF9qQSm2LKk4Fi07gqU7aD2xwbMHrBSClMNFJUaB77HZu2zvgEeheKJMruS3uYsasaLeuiaPnl4eZx/Ar0BBVvBtFIosS9ABaWeNqBaw9wfINvDY5ntcNJ+NPpnFZgClhP7qk9YtWURJkzsQcd+vwFVNYOqgAoH43WzqAqq6NjbngR+Na6Od5K2/8vVYTvMmwDU/4DNy+m7kblcPwPPY84F8FjSaW5QFikUJ/QS8L7l70dP0lEOpqqHIlSbH7QpSSclMNVApZveJK/YspsUqVnbAeXU6hTqFMopkIsPXQ/9AyubnSU4XZgDAAAAAElFTkSuQmCC",
            "chart": "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAAs9JREFUSEulV0uOFDEMfS/iACMWSCM2XADUJxi6bsIRpq+BhFjBmpt0DyeY4QQsEBISi2Y9UgxJXBXn11VArapTie33/Oy4ifAQgMS38WP3bNm/Zi7aUEMje3/nkyBEcYwjDF+6Tz6yEtUKskv2m28icgXgFQCXcpDjs7/ye0BIMC4U+z2ALyTPdUYbxCJyAOQtwCfJpxoq/asoqoD6ex4B3JL8aBGmk8qmF3lO4Nsqe1tiaYl6RvLnbLtA7EVuCNwpvQcA93UQK8Dz9rRxB+C9Lr4m+bnjmBDxewBHdTyRPF2qtrWqEhG1F90t9mabS5R5YxTL5NRxhpFKxUfxyU5Fdz+Lp2CHgHh1nLQyObpTahfBjnmiY8FRBaURtuVUIBFMdIkZS2NwUCMOQOY+RdtAvMieHaqbPEcK5aiIM4UV9yl1PGpFbqG6zUnDzOz4ImK/F/CYaJWJdKe5gopyasQQKOz08HmflvlE505e/AsCbzTATyS/LojTYkKsFLc5jlRHXXfElSz01DpaE0ARW1X3xKWOa/lb4QQthLLTmo4U5lLM6C6Wk9VDVrU9rAIxdPVUbddmtsJaRmzLyXb/IYUqkAQv5inWJ1NKZmZ6FRFYiOIyZy1zi2BHiLMyS8eZap6asy4E+B/ltNBlEdtWqOW0VXBjxJWqyzwp4qaBjMTV6qOsYw2jV8e9fus7Od5cTqYDLzmOAql6dZhGBNhpwccLQSeUcOWF5550Zy/+iojXYFpzPC85tg1ENwwbyKiOlyiL4bQ/l228FuN9fPPH4Z0aXwaB5vK33rVvxpnLrqf3LYNAbIXXAL6353sr43A6X8LSNckfXVWHRfFyC+KdAK5F0JkxR/NX9BAHikcCB5If6jSZdKerSESeAng5nGsbqktGzNjrAT6Q/LXsaFW9NkHVdJf7/+V0g7j+M7XF6JY9OXTCjD7bjm75a9Ps6WjzN/T//TJ/3xNIAAAAAElFTkSuQmCC",
            "cog": "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAABK1JREFUSEuVl0vIVVUYhp93dRNF6UZZWDQKqUlaQkJhKqmDaCDqb6GZRVGTyC5W2KAGUqkRDQIL0gLJO1EQXcxSIuguQk2iQRRqN0ztLypjv51vn3XO2fv8+/T/rck5rL32+i7v+37ft0X/EmDIP1T/jThb2SjP915qPFq9M/6Psqq3Ndw84rEQDt/7Vv3gQMODnLc9BbMQcXZ5szmK2J2kQyONDY5J/yeltmcC72HGlVi0DQcaw8AsSV/EVrPTfRE3ZKp9WcOyvQNY3PgMtiRp+ag8KA8EHANWv9e2TwM+AqYD+yVdVwZs7wPPgjLamZL+Ho01nayMOFfiCCtKjojNwFXAJuDcfPg9Kc2N1LjwXsScdsb5GVgJHMDcmsN6SUmH60ppw1EDxfb5wEEgfmP9CpyZT8X7RwSrJG3PEd8MbAAuyKCHGI9hzsq3f4e5Ukm/VCNsMtyHY44FTgCrI3JJJ6uXBAyGOwVPgSd04qmc2S5p6QDDwi7mtXB6Ox+IiLYATwA/YlYq6fsRuFQKTmFfAn4RFJCsAZYBQ5n585P0Toe3NXLZDqnMRj4Omirph7o4ROFikeBuYE52Yi/wnKRXa06JwH+y4WvBROBdSdd3tFYxXEb8FeYyxEnDw4JnJHXFZXs98EA7gi4EHTE/pqTHO1K0ywK6ijL9nAo+KKUrOs7VMLYdOLzSIRKwXlLgGrJZApSEAv4EdmT7SxDjyl0zTyntyWx/GnFf3i8QQ5J21SOu43Q1sNcwXrBF0vJ4XNih02mtKI6HvCR9kx2aCnwOjA9+SFqQ97dCBKLfAxZJn9TI1VTebBehCcFaKT2aI/gL+XSjjUkKjLvLLjaBQr9HpXROed4Ohq82+iNJE+qkrFWungu2I5VntGryk0p6JEcQ9TgueL5Furv65PQCcAfwm5QmZcPrgAdbnBhW0sT+MtxuEpWwbZepzqnbJummbPgD8DVGxwTTpPRttL/CvhT4FJgUDUTS3AzNTmBRy3g91dlgTU6FPSTY2iWXWa/UJdeNLYxfy2QZRt4JOgVYAh4XtVWwQFJZB1x4A+L+nJng4WJJu7usrmJs+0vM5SGnXKWelZI77cp2J30j6gjwkKR43vatLad7WyRdp7acDiSl6YMKSKQ4CkMwNxeQuo2Wc4tazf8exLX5yevgjVJ6s78R28Vko04B6TI+3qvouCwg84G38oW5ZHpNlsRKKZfMivw6/ChxLXxR7mZBwrXgZUYBX6x5kvb8l46bm4Q5gapNIs9W7dIYvfq2FiHXgSf1mkS3um2X0tLqhFEjV2bjeWU/hQszWkdBwdjAKZJ0CDOkpA8zlpHybb3z/BOyqrVFmCHpp+qY1TiB2MUUo1vUHgRehnKwi0FgRobhDSndkAtLYFtWK+Bj4HbDMZkVGcjNko70s3HMw15m6Wfl6GP2K+XRp/A+xKxcNmdUVdA/9g2IeNA8XC2NjpQOdSVTETxoq6SYRiqred7ssbpBlQNqeFS19yF3o+57HgbNlhQZGdOqpHqQr1XtlIXhYmBhnsPyQO9dSelwVVpj+ZzpWmxOzOB09VytO1fd733OVO9pmqvHYiffXCVL35feKOkW/wKAqApHETMHZgAAAABJRU5ErkJggg==",
            "bolt": "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAAuJJREFUSEuVV72PT0EUPWcSGgWF+AdEVtjoFKpViUZjE1uQLAW1SoVd26q0JBKisL4SiU7nH5AtFolGQ0Uh2WQb5tj33vzezH0z837Pa97H3Lkf55577zyivwhA8XX41C4HmVHRdJEgFLSG50QFUFBU1m03172crdSc6EyGK1Ua3ZL3RwCuAjjQICIQbICJO38AeEzyj3GkhoqJuDedgy35hwKvJx72+hP7Jx35qcvENPiMvpKTkt8CeKqzZkNN3hZJbpegr6cskR4KSXIAdgHsz5UG2AEPYB/J5p5dNssR0S7ibLX7IGkBwJdMWwg13LZJLk4m+iytNY9aYKWLgF4bDiZeBMMvSLcyWoqp53k5pTXXmfJed0BspJltn22q10huZMiVP5iuUS1HSc8BrGS8sp4s0/FNub/UE1Cqklgu0haAwOiO1W0dV13tF3YAXCH5tsa2qg4vOWaMtqyKSFjsg7GnJFerfaS2sAfzcQif+/Ay3UVjs1r/C+A0yY8FXvXZL/RqwssvE3g1hmo0ndHvPslbw0o1TtQi9tJdCvemJNQ6p28AT5DcHZs+lQYCeGmTwKXItGQwFFBOPi058kM3YCex2gpJegbg8lwCWycekbwxd08fQ8ExSYcAXANwcKDoLIClwohsxuMC6XbaLhYKOx4ErJYJJdnraEee5Nf3qLs2jErABef4zo5FG9GwyZg2Njv8RCG72UvrDIYTlF+SjHxIvMrANL16SlKCjKRhxL8BHSXdr1xNYmWGfhDi2HTqZDLS9YZDxFdJPqlFVm0g8w0PqtRG/J7kuca5MonSiAf5nuJpajqBujmZHCP5/T8yZfg0Q73rszUIwvfWsLAG4qYjH4ycxGuDqUtgvbcM9lnD50GcIdsjwchVS8HgXF0+vti/AS9/m8Amya+Re+OtsXbizVuKiSNj9WE6/pzbKOb16imszmTSFpQZyM9upXwk06n2X2SbQFaXheVa10sD+AfIRU0vHRvupAAAAABJRU5ErkJggg==",
            "joystick": "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAA9pJREFUSEudl72rXUUUxX9r1MJIChGENGpEC3lqpYKm0IgfsTGNBNRoIUh4Vawt8u4zf4CvS4qkETWQQlQQY+EXxPgBihifoigoYqWFRogI8SzvzJlz75xz57z7cOA2c2b22muvvffsK6pLgPMXIYzLrfolqJwZuxb3ZwBzsDHL4/t9V0u3qTqt/0lkuWdbUXUbnGqIxiKxwCxt9FG2RWY7h0p6FZwFz+s2c650wtYO2b4KOAzcD9wF7Fwe296JC8BnwLvAi5L+GYa10Lh1wfa9wEvAdcvAYt4X2Tk7Ptj/EfO0gs6Vsvbu2d4NfA3sABrM24hvgIuputRma3dpAXh+ZofgNuAB4HLgL+AWSb92JdcyzvG2/RFwD/A78LCkL7ZbbdFE03glGg7SZvTBbnYZfS6zC3EmSI+03SHqnZftmw3ftxt+Iiic6lrIspDH7429ojZacd0qaTMC2M0h4HiyCruD9FNXSC2U/YzhZPbkWkm/5f014LnWnjeksN5zZB6tlSzTEDjmys/5zqqk5ETJeDK1vBbdUkgKRGceBd4ogQz7Q9Cb6VzL9AB41eiYYDOfjU6sAseCdLpp7Iy0LiniMMtq2xPDmjJw1mwyjVZkXK51BU26Vj6tgveB+6a/DyTtzQ739jw1ntMyA/c0biagpYyB/cqMM8iBjh2JcUrtGWNJp1vgtOaMOyp2Bk5hCLlwUrgLjdmQ1Nc4GRCNm0py5czYGtitxgPgfpRzJi20u5S9ObkS45zVY8AqNS4Zt8m1uLZ+DJzruC2l+VrUuJbVC4z7YLZjJ9pD25mipOcRZyX9W3c2ybWVxmWo+4xz2VwxrZ4jhsMyOwdN+oJhQ3BUCpcGY0AGThLUsnoMOOl3NXAmv1SZWKV5wyfAPkl/duyz01tm9ZHoUb5wmaQml8uVwIfAnfnbp9OKmSgoOhLZ7AOOAnfMvsNeSX/n7wHoZFiT9EJbB53/9lP5OYw7e4J0rrED+GXQ4/nYa9O2+JiU2sxsILQbGb0uiJ0urlPAk/Gc7ZgPZ3N9H5T0yhD4RuC7/Ix9C7yDeRB5JfY7ma8Qd0u62NouJ4okRxwePp4lHXwZu1l85eKTCFwCbpKU+navbBr7kMzx/m7S8oc4jUj6ZSxzs5bXRzDDDf2HPiE9G6QT/Wex6AuN/RAQdbgdiPq+ZTgYpD/GQEv2tq8xvCqIdmJ0zgPPS3qvvN9zrBwK6gPb8Opg6F/wrGKlINk/PtYVx+kOvvSnyZwOC/8VWsaV3jtsArNZqRiV6tcqwBWni1CPh2UswPUglHbGBSuGveWqLvnLUZWsLrv4DwluzjR5bG4vAAAAAElFTkSuQmCC",
            "discord": "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAA1RJREFUSEull02ITlEYx3//SxRh4SMlnzEWkqTEipRiYSHJTkQis5goShYzycpEkiL5yooFG0VZjGQzVigb8lGkMJQNxnAfc+49973f930np+Z9z3vO8zz/5/98nHNGuCHAoll+XreUlfcyHX9FuoogK0fHttsIepwILGUX8xvDqEOpWG+zVAZOXezMoTqAkp3/ZCysGLWGXNXnIWbcJoJmthLYBIxI6q9CMrOj3tK9QHqW1GpJtrm4RGjhbMEu4AAwzxv4DWwFZgKz/NpnsCHQbWCCX3uLcQHZlUDBUM4JTzLHOCFuZlOAN8CMosfOSFIY2XlNQXwEFinQcKtdMy1a0jGzM0BP2VgHUGWlPgXqdcDF46Il6jZCs0XAS4Nx7Xqtzo10PZoNR6wlx77Ft2TbzK4Au0shbY/S1H5nJB3KFrKy9EOziYKvwORqK4bRcNx5pQqnvyDmSBppcS4A75Jxtal6CmHM+1eKStZR2yYFt5NEZ0IdtdBDwbqWtdTQX+AmsBRYFe+XUAaB18COmvq4G0hbsndRbMZsIvADCArAIbBA0nsv1w2cK6Riv6SLfn++b8XUTozwM1AwqQp4OfC8IrcDkjYk66OtNo24Dsb5NReN6ZK+Z2QGMNYXryCDhYH0zsm1Qm1m24FbHQBPBb41AYdmA4L1+chFqdmsQPeTnk5CfXzU2IkK4D/AQgX64G6H0MJulUO9T9IlR8PCcC7InXrjW3UQYUYfPZLOOr5Zxv0Gh8uHRqSQFNcygxWxjZKLvrhsh6HKw2dUrTeQ+oqhdmwd64bRyZFZ0eup2hFJp4rAxwxOxkS8ZAXOWA+wgny3pPMpcJybzaA7gGur7DhtMCjYC7YxinE1ult9AFwG1uYumTjHv0AbJT3OMXY/QrMlMq6jSDE7XmGsQbjrcoW/Lt2d7EwO+b+nGCOIR8DignMDwB5JbytOrrheQrMA7CDIHRRdHv2GpJ1N2U+eWKORGwSt9rIvgLNRxRdG7pIobprZGuepKzpJn/L7riVcIcUjBbYugx4Z1xToSZ2z7a7c5iJvIWbR61VqHwKpyhjeyW2ew9ntxhdI8uAvCiUhTeNaDHzpn4VcCjp6c+UjWMe+/s2cdakuIM05rqNdwuzMiaxD/wCZo1QyvsRDrAAAAABJRU5ErkJggg==",
            "minus": "iVBORw0KGgoAAAANSUhEUgAAACUAAAAlCAYAAADFniADAAAAAXNSR0IArs4c6QAAAl9JREFUWEetWMlxwzAMBDpJCWklFaYFd+IW0gkzvEHckqXJw6ZwLMDFkg7ChQcBoAj7saq85EsICEWJMEN2+2r1wKODrYH3G0SAIitq2SV4F5SszQawA2VsvLRupz4NbsF04+Kn2+fsyUrsIzBZmmcVTfBcG3t+Es/ZvjkL2sQZGzOiYbF8EABL/TtnkBU4w6htNFs4S0lO02zFFISoyYEkaMNqIGGjrSbujXKUau+kbEhUSp6F1y0r8NPrITTJBlvZTlBsAuyNkiqstZsfKrnRabEVvGPpob4NvAokI8E5fVUMKw1rixxSili30NtOe/uWza0Mz1FTEn2MpDjRfaDRlYQi1iOdq4pOJcXEUVbz1uRO5Vbk9snqQynlGwB+q82gWb8UNe6Rp9KQjIxSKS/hDxF/jkXSC9d/gHp35ykQiZSxZL4mKESEwm5/uiSMoA1UgTeX2NW1BdYGetoutAuUhj/Tqa/taKSIO0MJ0KwR8WW5GaCuycI5fZuwPKl+J6S5lsBKAJo4ztN9v4uA++JIGbqPswWKqjcLNL5G6Ye6KXeynGdXgC0k90ZJSJmxZXJnUuwjoHamGUsbV3meULnwqOvcOVhNuqILTeK7ninY2jq+rnNaZNDChexY7aXUunNkqb/7SHoDiVer7hKWJE6ca79kvMNS6XmHU8/LM40Hs3EqX4d+SYn8o/dCZLvmX29Whup5m1MQXZ3aWJ9CndvDTnVFQo5lB1N/FRqsi4ZuS/3N/7qENDwqyfQxVi26L5mIjByni/dtOJ6UIdEsAbH0rdmzaQsLIAbzo/AJg8A/Bg/vLTpOMb0AAAAASUVORK5CYII="
        }

        return icons.get(icon_name)

    def create_nyx_folders(self):
        nyx_path = os.path.join(os.getenv('APPDATA'), "Nyx") # type: ignore

        # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(nyx_path):
            self.logger.debug("Creating Nyx folder in AppData")
            os.makedirs(nyx_path)

        error_logs_path = os.path.join(nyx_path, "Errors")

        # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(error_logs_path):
            self.logger.debug("Creating Errors folder in Nyx folder")
            os.makedirs(error_logs_path)

        return nyx_path, error_logs_path
