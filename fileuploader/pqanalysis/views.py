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
		worklist_options = request.POST.getlist('worklist-options')[0]
		limit_options = request.POST.getlist('limit-options')[0]
		assay_options = request.POST.getlist('assay-analysis')[0]
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

		return add_attachment_done(request, assay_options, format_analysis_id, worklist_options, limit_options)
	return render(request, "pqanalysis/pqanalysis.html")

def add_attachment_done(request, assay, format_analysis_id, worklist_options, limit_options):
	""" 
		(1) Append analysis_id to R markdown output.
		(2) Execute necessary programs
		(3) Go to results page
	"""

	query_db = PqAttachment.objects.filter(analysis_id__exact = format_analysis_id)
	files_dir = os.path.dirname(os.path.abspath(query_db.values()[0]['attachment']))

	if assay == 'paraflu':

		r = R_Caller('paraflu', files_dir)

		if worklist_options == 'paraflu-default-worklist' and limit_options == 'paraflu-default-limit':
			r.set_defaults()
			r.execute()
		elif worklist_options == 'paraflu-default-worklist':
			r.set_defaults()
			r.limits_file = limit_options
			r.execute()
		elif limit_options == 'paraflu-default-limit':
			r = set_defaults()
			r.worklist_file = worklist_options
			r.execute()
		else:
			r.execute(default=False, data_dir=files_dir, assay_type='paraflu', wrk_list=worklist_options,
					  limits_list=limit_options)

	shuttle_dir('paraflu')

	return render(request, "pqanalysis/pqanalysis.html")


def shuttle_dir(assay_location):
	""" Shuttles and saves the output """

	import time
	import shutil

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	GET_DATA = os.path.join(BASE_DIR, 'rcall', 'pqresults', assay_location)
	SAVE_DATA = os.path.join(BASE_DIR, 'rcall', 'pqresults')

	que = []

	# This is a hack, may need to find a way to optimize this
	# It's to wait for the R script to finally finish
	while len(que) <= 0:
		time.sleep(2)
		for results in os.listdir(GET_DATA):
			if results.endswith('.html'):
				que.append(results)
	
	for pq_files in que:
		# (1) Here's where you look up the file and save to database
		# (2) Here's where you move the file
		shutil.move(os.path.join(GET_DATA, pq_files), SAVE_DATA)

def view_results(request):


	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	SAVE_DATA = os.path.join(BASE_DIR, 'rcall', 'pqresults')

	file_dict = {}

	for files in os.listdir(SAVE_DATA):
		if files.endswith('.html'):
			file_dict[files] = os.path.join(SAVE_DATA, files)

	return render(request, 'pqanalysis/pqresults.html', {'file_dict':file_dict})