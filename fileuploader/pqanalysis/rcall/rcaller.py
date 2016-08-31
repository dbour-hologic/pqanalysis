""" R caller is used as a helper 
to call R scripts using Python """

import os
import subprocess
import shlex

from subprocess import Popen, PIPE, STDOUT

class R_Caller():

    def __init__(self, assay_type, data_dir, analysis_id, graph, output_dir="./",):

        self.assay = assay_type
        self.data_dir = data_dir
        self.output_dir = output_dir + analysis_id + ".html"
        self.analysis_id = analysis_id
        self.graph_type = graph

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Set the main markdown script to use depending on assay
        if assay_type == 'paraflu':
            self.markdown_file = os.path.join(base_dir, 'pqresults', 'paraflu', 'PQReportCompiler3.Rmd')

    def set_defaults(self):
        """ Sets the default settings if none is specified """

        base_dir = os.path.dirname(os.path.abspath(__file__))

        settings = {
            'paraflu':{'worklist_file': os.path.join(base_dir, 'defaults', 'paraflu','worklist', 'worklist.id.csv'),
                       'limits_file': os.path.join(base_dir, 'defaults', 'paraflu', 'limits', 'assay.limits.csv')
                      }
        }

        if self.assay == 'paraflu':
            self.worklist_file = settings['paraflu']['worklist_file']
            self.limits_file = settings['paraflu']['limits_file']
        else:
            pass

    def execute(self, default=True, *args, **kwargs):

        """ Execute is used as the main entrance point of the 
        program. Execute takes care of the main logic. If default settings
        are used, it will directly call r markdown script, else it will
        use user inputs

        Args:
            defaults - to switch defaults on/off (bool)
            *args - None
            **kwargs - 
              
                (1) data_dir
                (2) assay_type
                (3) wrk_list
                (4) limits_list
                (5) lof
                (6) analysis_id
                (7) graph_type
        Returns:
            If run was executed. (bool)
        """

        logs = None

        if default:
            if self.assay == 'paraflu':
                logs = self.__call_r_markdown(self.markdown_file,
                                              self.output_dir,
                                              self.data_dir,
                                              'paraflu', 
                                              self.worklist_file, 
                                              self.limits_file,
                                              self.analysis_id,
                                              self.graph_type)
        else:
            try:
                markdown_arg = self.markdown_file
                data_arg = kwargs.get('data_dir')
                assay_arg = kwargs.get('assay_type')
                work_arg = kwargs.get('wrk_list')
                limit_arg = kwargs.get('limits_list')
                lof_arg = kwargs.get('lof', "nonspecified")
                analysis_id = kwargs.get('analysis_id')
                graphing_type = kwargs.get('graphing_type', 'time')

                logs = self.__call_r_markdown(markdown_arg, data_arg, assay_arg, 
                                              work_arg, limit_arg, analysis_id, 
                                              graphing_type, lof_arg)

            except KeyError:
                print("MISSING ARGUMENTS")

 
        return logs

    def __call_r_markdown(self, markdown_file, output_dir, data_dir, assay_type,
                        worklist_file, limits_file, analysis_id, graphing_type, 
                        lof_file="nonspecified",):
        
        """ call_r_markdown is a method used for executing the
        R markdown script PQReportCompiler.Rmd. The PQReportCompiler
        takes a directory of 'Panther PCR' files, combines them,
        then runs an analysis on them and outputs a .html file 

        Args:
            markdown_dir - the file where the *.Rmd file is located.
            output_dir - the directory to output the file
            data_dir - the data directory where the PCR data is located.
            assay_type - the assay type analyzed (paraflu, flu, etc)
            worklist_file - the file containing the naming schema
            limits_file - the file containing the PQ ranges
            lof_file - the file containing a list of files to be analyzed (dir used by default)
            analysis_id - the unique tag to group this run
            graphing_type - FVF, time, instrument (changes view of graph)
        Returns:
            None
        Outputs:
            R markdown file
        """

        COMMAND = "Rscript"
        PARAM = "-e"
        RMD_FILE = markdown_file
        OUTPUT_DIR = output_dir
        DATA_DIR = data_dir
        AS_TYPE = assay_type
        WRKLIST = worklist_file
        LIM_FILE = limits_file
        LOF_FILE = lof_file
        ANA_ID = analysis_id
        GRPH_TYPE = graphing_type



        FINAL_CMD = "\"rmarkdown::render(input='%s', output_file='%s', params=list(directory='%s',"\
                                                                                  "assay='%s',"\
                                                                                  "worklist.id='%s',"\
                                                                                  "limits='%s',"\
                                                                                  "lof='%s' ,"\
                                                                                  "analysis.id='%s',"\
                                                                                  "graphing='%s'" \
                                                                                  "))\"" % (RMD_FILE, OUTPUT_DIR,
                                                                                            DATA_DIR, AS_TYPE,
                                                                                            WRKLIST, LIM_FILE, LOF_FILE,
                                                                                            ANA_ID, GRPH_TYPE)

        execute_cmd = [COMMAND, PARAM, FINAL_CMD]
        execute_to_str = " ".join(execute_cmd)
        # // LATER FIX -- WHY DOESN'T CENTOS NOT LIKE SHLEX.SPLIT??
        args=execute_to_str
        # args = shlex.split(execute_to_str)

        logs = subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)

        # run_completed = True

        # while True:

        #     line = logs.stdout.readline()
        #     print(">>> ", line)

        #     if "Execution halted" in line:
        #         print("IT BROKE!!!!!!!!!")
        #         run_completed = False
        #         break

        #     if line = '':
        #         break

        return logs

if __name__ == '__main__':

    """ STANDALONE SCRIPT RUNNER """


    r = R_Caller('paraflu', os.path.join(os.getcwd(), 'data'), "kunfu1.html", "time", "./kunfu1.html")
    r.set_defaults()
    r.execute()

