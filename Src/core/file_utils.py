import os
import subprocess


def FormatConverter(InputFolder, OutputFolder):
     for file in os.listdir(InputFolder):
          var_InputFolder = os.path.join(InputFolder, file)
          var_OutputFolder = os.path.join(OutputFolder, file).replace(
               "mp4", "mp3")
          command = f"ffmpeg -i \"{var_InputFolder}\" -vn -ab 128k -ar 44100 -y \"{var_OutputFolder}\""
          subprocess.call(command, shell=True)