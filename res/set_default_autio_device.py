import os
import subprocess
import win10toast
dirname = os.path.dirname(__file__)
icon_path = os.path.join(dirname, 'hp.ico')


class DefaultAudioHandler:
    """
    class for switching default audio devices
    microphone and speakers
    """
    def __init__(self, main_audio_device_name: list[str], sec_audio_device_name: list[str]) -> None:
        """
        init class
        :param main_audio_device_name: [0] - speakers, [1] - microphone
        :param sec_audio_device_name: [0] - headphones, [1] - microphone
        """

        self.external_devs = main_audio_device_name
        self.headphones_devs = sec_audio_device_name

        self.nircmd_path = os.path.join(dirname, 'nircmd.exe')  # get abs path to utility TODO: http://www.nirsoft.net/utils/nircmd.html
        self.toaster = win10toast.ToastNotifier()

    def set_default_sound_device(self, sound_device_name: list[str]) -> None:
        """
        set default audio device to sound_device_name
        :param sound_device_name: list of device names
        """
        for device in sound_device_name:
            cmd0 = f"{self.nircmd_path} setdefaultsounddevice \"{device}\""
            cmd_full = f"{cmd0} 1 && {cmd0} 2"
            subprocess.Popen(cmd_full, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.toaster.show_toast("Default speakers changed to:", f"Audio: {sound_device_name[0]}\nMicro: {sound_device_name[1]}", icon_path=icon_path, duration=3)

    def set_def_hp(self):
        """
        set default audio device to headphones
        """
        self.set_default_sound_device(self.headphones_devs)

    def set_def_ms(self):
        """
        set default audio device to main speakers
        """
        self.set_default_sound_device(self.external_devs)
