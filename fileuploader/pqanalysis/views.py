from django.shortcuts import render, redirect, render_to_response
from .models import PqAttachment
import datetime, os

def create_timestamp():
	""" Creates the timestamp """
	return ('{:%Y%m%d-%H-%M-%S}'.format(datetime.datetime.now()))

def add_attachment(request):
	if request.method == "POST":
		analysis_id = request.POST['analysis_id']
		program_options = request.POST.getlist['progoptions']
		submitter = request.POST['submitter']
		files = request.FILES.getlist('filelist')

		format_analysis_id = analysis_id + create_timestamp()

		for a_file in files:

			instance = PqAttachment(
				analysis_id = format_analysis_id,
				file_name = a_file.name,
				attachment= a_file,
				submitter= submitter
			)

			instance.save()

		return add_attachment_done(request, analysis_id, progoptions)
	return render(request, "pqanalysis/pqanalysis.html")

def add_attachment_done(request, analysis_id, progoptions):
	""" 
		(1) Append analysis_id to R markdown output.
		(2) See which direction to take through progoptions
			2a. PQ Analysis
			2b. Combine files
		(3) Execute necessary programs
		(4) Go to results page
	"""
	return render(request, "pqanalysis/pqanalysis.html")

