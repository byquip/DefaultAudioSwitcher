import os
import subprocess
import win10toast


class DefaultAudioHandler:
    def __init__(self, main_audio_device_name: str, hyperx_audio_device_name: str) -> None:
        self.monitor_speakers = main_audio_device_name
        self.headphons = hyperx_audio_device_name
        self.nircmd_path = os.path.abspath("nircmd.exe")  # get abs path to utility TODO: http://www.nirsoft.net/utils/nircmd.html
        self.toaster = win10toast.ToastNotifier()

    def set_default_sound_device(self, sound_device_name: str) -> None:
        os.system(f'{self.nircmd_path} setdefaultsounddevice \"{sound_device_name}\" 1"')
        self.toaster.show_toast("Default Speakers Changed", f"To: {sound_device_name}", icon_path="hp.ico", duration=3)

    def set_def_hp(self):
        self.set_default_sound_device(self.headphons)

    def set_def_ms(self):
        self.set_default_sound_device(self.monitor_speakers)
