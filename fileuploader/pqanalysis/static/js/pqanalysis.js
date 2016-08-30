// DataTable library for organization of results
$(document).ready(function() {
	$("#pqupload").validate({
		rules: {
			'file[]': {
				required: true,
				extension: 'csv|tsv'
			},
			'analysis_id': {
				required: true,
				alphanumeric:true,
				rangelength:[1,99]
			},
			'submitter': {
				required: true,
				alphanumeric: true,
				rangelength:[1,99]
			}
		},
		messages: {
			'file[]': {
				required: "Please select PCR file(s).",
				extension: "Please upload valid file format."
			}
		}
	});
});
