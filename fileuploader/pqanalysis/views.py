from django.shortcuts import render, redirect, render_to_response
from .models import PqAttachment
from rcall.rcaller import R_Caller
import datetime, os


def create_timestamp():
	""" Creates the timestamp """
	return ('{:%Y%m%d-%H-%M-%S}'.format(datetime.datetime.now()))

def add_attachment(request):
	if request.method == "POST":
		analysis_id = request.POST['analysis_id']
		worklist_options = request.POST.getlist('worklist-options')
		limit_options = request.POST.getlist('limit-options')
		submitter = request.POST['submitter']
		files = request.FILES.getlist('file[]')

		format_analysis_id = analysis_id + create_timestamp()

		for a_file in files:

			instance = PqAttachment(
				analysis_id = format_analysis_id,
				file_name = a_file.name,
				attachment= a_file,
				submitter= submitter
			)

			instance.save()

		return add_attachment_done(request, format_analysis_id, worklist_options, limit_options)
	return render(request, "pqanalysis/pqanalysis.html")

def add_attachment_done(request, format_analysis_id, worklist_options, limit_options):
	""" 
		(1) Append analysis_id to R markdown output.
		(2) Execute necessary programs
		(3) Go to results page
	"""
	print(worklist_options)
	print(limit_options)

	query_db = PqAttachment.objects.filter(analysis_id__exact = format_analysis_id)
	files_dir = os.path.dirname(os.path.abspath(query_db.values()[0]['attachment']))

	r = R_Caller('paraflu', files_dir)
	r.set_defaults()
	r.execute()

	return render(request, "pqanalysis/pqanalysis.html")

