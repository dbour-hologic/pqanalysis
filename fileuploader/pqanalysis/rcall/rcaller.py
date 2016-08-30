""" R caller is used as a helper 
to call R scripts using Python """

import os
import subprocess
import shlex

class R_Caller():

    def __init__(self, assay_type, data_dir):
        self.assay = assay_type
        self.data_dir = data_dir

    def set_defaults(self):
        """ Sets the default settings if none is specified """

        base_dir = os.path.dirname(os.path.abspath(__file__))

        settings = {
            'paraflu':{'markdown_file': os.path.join(base_dir, 'pqresults', 'paraflu', 'PQReportCompiler2.Rmd'),
                       'worklist_file': os.path.join(base_dir, 'defaults', 'paraflu','worklist', 'worklist.id.csv'),
                       'limits_file': os.path.join(base_dir, 'defaults', 'paraflu', 'limits', 'assay.limits.csv')
                      }
        }

        if self.assay == 'paraflu':
            self.markdown_file = settings['paraflu']['markdown_file']
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
                (1) markdown_file
                (2) data_dir
                (3) assay_type
                (4) wrk_list
                (5) limits_list
                (6) lof
                (7) str_as_factor
        Returns:
            If run was executed. (bool)
        """

        if default:
            if self.assay == 'paraflu':
                self.__call_r_markdown(self.markdown_file, self.data_dir, 'paraflu', self.worklist_file, self.limits_file)
        else:
            try:
                markdown_arg = kwargs.get('markdown_file')
                data_arg = kwargs.get('data_dir')
                assay_arg = kwargs.get('assay_type')
                work_arg = kwargs.get('wrk_list')
                limit_arg = kwargs.get('limits_list')
                lof_arg = kwargs.get('lof', "nonspecified")
                str_as = kwargs.get('str_as_factor', "FALSE")
                self.__call_r_markdown(markdown_arg, data_arg, assay_arg, work_arg, limit_arg, lof_arg, str_as)
            except KeyError:
                print("MISSING ARGUMENTS")

    def __call_r_markdown(self, markdown_file, data_dir, assay_type,
                        worklist_file, limits_file, lof_file="nonspecified",
                        string_as_factor="FALSE"):
        
        """ call_r_markdown is a method used for executing the
        R markdown script PQReportCompiler.Rmd. The PQReportCompiler
        takes a directory of 'Panther PCR' files, combines them,
        then runs an analysis on them and outputs a .html file 

        Args:
            markdown_dir - the file where the *.Rmd file is located.
            data_dir - the data directory where the PCR data is located.
            assay_type - the assay type analyzed (paraflu, flu, etc)
            worklist_file - the file containing the naming schema
            limits_file - the file containing the PQ ranges
            lof_file - the file containing a list of files to be analyzed (dir used by default)
            string_as_factor - ?
        Returns:
            None
        Outputs:
            R markdown file
        """

        COMMAND = "Rscript"
        PARAM = "-e"
        RMD_FILE = markdown_file
        DATA_DIR = data_dir
        AS_TYPE = assay_type
        WRKLIST = worklist_file
        LIM_FILE = limits_file
        LOF_FILE = lof_file
        STR_AS_F = string_as_factor

        FINAL_CMD = "\"rmarkdown::render(input='%s', params=data.frame(directory='%s',"\
                                                                        "assay='%s',"\
                                                                        "worklist.id='%s',"\
                                                                        "limits='%s',"\
                                                                        "lof='%s' ,"\
                                                                        "stringsAsFactors=%s"\
                                                                        "))\"" % (RMD_FILE, DATA_DIR, AS_TYPE,
                                                                                    WRKLIST, LIM_FILE, LOF_FILE,
                                                                                    STR_AS_F)

        execute_cmd = [COMMAND, PARAM, FINAL_CMD]
        execute_to_str = " ".join(execute_cmd)
        args = shlex.split(execute_to_str)
        subprocess.Popen(args)

if __name__ == '__main__':

    """ STANDALONE SCRIPT RUNNER """

    r = R_Caller('paraflu', os.path.join(os.getcwd(), 'data'))
    r.set_defaults()
    r.execute()

