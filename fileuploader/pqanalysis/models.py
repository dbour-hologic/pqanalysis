from django.db import models
from django.utils.timezone import now as timezone_now
import random
import string
import os

def upload_to(instance, filename):
	""" Custom upload modifier method that will help
	create a unique directory to store a group of files.
	The unique directory is generated by a name given
	by the user as well as a timestamp appended to the name.

	Args:
		instance - the file instance from post request (file obj)
		filename - the actual string representation of filename (str)
	Returns:
		the location to save the file (str)
	"""

	base_media_dir = "media/pqanalysis/"
	save_directory = instance.analysis_id
	filename_base, filename_ext = os.path.splitext(filename)

	return base_media_dir + save_directory + "/" + filename_base + filename_ext.lower()

class PqAttachment(models.Model):
	analysis_id = models.CharField(max_length=100)
	file_name = models.CharField(max_length=100)
	attachment = models.FileField(upload_to=upload_to)
	submitter = models.CharField(max_length=100)

class PqResults(models.Model):
	pqresults = models.ForeignKey(PqAttachment, on_delete=models.CASCADE)
	pq_file_name = models.CharField(max_length=100)
	file_dir = models.FileField(upload_to=None)

class CombineResults(models.Model):
	combine_results = models.ForeignKey(PqAttachment, on_delete=models.CASCADE)
	combine_file_name = models.CharField(max_length=100)