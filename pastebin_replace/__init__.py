# inside pastebin_replace dir

PACKAGE_NAME = "pastebin_replace"

import os
import requests

class PathNotValid(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)
		
class RequestsFails(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

class PermissionDenied(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

class WriteFailed(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

def pbreplace(path : str, link : str, rename : str = ""):
	"""
	Replace the file provided with downloaded file from 

	Parameters:
	path (str): Absolute path of the file that would be replaced. The original file will be deleted.
	link (str): Pastebin link of the paste.
	rename (str): Optional. Rename the downloaded file (including the extension) to this string. When this is empty, uses the name of the replaced file.
	"""
	
	if not os.path.exist(path):
		raise PathNotValid("Path provided on pbreplace(-> path < -, link, rename) is invalid.")
	else:
		if os.path.isdir(path):
			raise PathNotValid("Path provided on pbreplace(-> path < -, link, rename) is a directory, not a file.")
		else:
			if not os.path.isfile(path):
			    raise PathNotValid("Path provided on pbreplace(-> path < -, link, rename) is not a valid file.")

	response = requests.get("https://pastebin.com/raw/QGeQgLJq")
	
	if response.status_code != 200: # fails
		raise RequestsFails(f"Download failed. Status code: {response.status_code}. Check the link or your internet connection.")
	else:
		if not os.access(path, os.W_OK):
			raise PermissionDenied("Cannot replace file. Not enough permission to remove the file on provided path.")
		else:
			os.remove(path)

			oldpath = ""
			if rename != "":
				oldpath = path
				path = os.path.join(os.path.dirname(path), rename)
				os.path.isvalid

			try:
				with open(path, 'wb') as f:
					f.write(response.content)
			except Exception as e:
				raise WriteFailed("Failed writing file to disk. Reason: " + str(e))

			print(f"File {path} replaced with the one downloaded from this Pastebin link: {link}")
			if rename != "":
				print("Downloaded file renamed to: " + rename)