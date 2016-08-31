from django.shortcuts import render, redirect, render_to_response
from django.conf import settings
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
		graph_options = request.POST.getlist('graph-options')[0]
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

		return add_attachment_done(request, assay_options, format_analysis_id, worklist_options, limit_options, graph_options)
	return render(request, "pqanalysis/pqanalysis.html")

def add_attachment_done(request, assay, format_analysis_id, worklist_options, limit_options, graph_options):
	""" 
		(1) Append analysis_id to R markdown output.
		(2) Execute necessary programs
		(3) Go to results page
	"""

	logs = ""

	query_db = PqAttachment.objects.filter(analysis_id__exact = format_analysis_id)
	files_dir = os.path.join(settings.MEDIA_ROOT, "/".join(query_db.values()[0]['attachment'].split("/")[:-1]))

	if assay == 'paraflu':

		r = R_Caller('paraflu', files_dir, format_analysis_id, graph_options)

		if worklist_options == 'paraflu-default-worklist' and limit_options == 'paraflu-default-limit':
			r.set_defaults()
			logs = r.execute()
		elif worklist_options == 'paraflu-default-worklist':
			r.set_defaults()
			r.limits_file = limit_options
			logs = r.execute()
		elif limit_options == 'paraflu-default-limit':
			r = set_defaults()
			r.worklist_file = worklist_options
			logs = r.execute()
		else:
			logs = r.execute(default=False, data_dir=files_dir, assay_type='paraflu', wrk_list=worklist_options,
					  limits_list=limit_options, graphing_type=graph_options)

	

	log_str = ""

	run_completed = True

	while True:

	    line = logs.stdout.readline()
	    log_str += line + "\n"

	    if "Execution halted" in line:
	        print("FOUND AN ERROR!.")
	        run_completed = False
	        break

	    if line == '':
	        break

	if not run_completed:
		return render(request, "pqanalysis/pqerror.html", {"error_out":log_str})

	program_timed_out = shuttle_dir('paraflu')

	return view_results(request)


def shuttle_dir(assay_location):
	""" Shuttles and saves the output """

	import time
	import shutil

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	GET_DATA = os.path.join(BASE_DIR, 'rcall', 'pqresults', assay_location)
	SAVE_DATA = os.path.join(settings.MEDIA_ROOT, 'pqresults', 'results')

	que = []

	# This is a hack, may need to find a way to optimize this
	# It's to wait for the R script to finally finish

	timed_out = True

	# Maximum waiting time of 480 seconds before timing out.
	for counts in range(480):

		for results in os.listdir(GET_DATA):
			if results.endswith('.html'):
				que.append(results)

		if len(que) <= 0:
			time.sleep(1)
		else:
			timed_out = False
			break
	
	if not timed_out:
		for pq_files in que:
			# (1) Here's where you look up the file and save to database
			pq = PqAttachment.objects.filter(analysis_id__exact = pq_files.replace(".html",""))


			# (2) Here's where you move the file
			try:
				shutil.move(os.path.join(GET_DATA, pq_files), SAVE_DATA)
			except IOError:
				print("File has already moved.")

	return timed_out

def view_results(request):

	SAVE_DATA = os.path.join(settings.MEDIA_ROOT, 'pqresults', 'results')

	file_dict = {}

	for files in os.listdir(SAVE_DATA):
		if files.endswith('.html'):
			try:
				query_result = PqAttachment.objects.filter(analysis_id__exact = files.replace(".html",""))				
				# file_dict[files] = query_result[0] - reimplement after database
				file_dict[files] = os.path.join('pqresults', 'results', files)
			except IndexError:
				# Have to create a fake object here to resemble above result for templating reasons
				file_dict[files] = {"No data found"}
				print("No such file found.")

	return render(request, 'pqanalysis/pqresults.html', {'file_dict':file_dict})