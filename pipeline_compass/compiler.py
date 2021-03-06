from pipeline.compilers import CompilerBase
import scss
import os

# setup scss load path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_paths = scss.LOAD_PATHS.split(',') # split it up so we can a path check.
scss_path = os.path.join(root, 'pipeline_compass', 'compass')

if scss_path not in load_paths:
    load_paths.append(scss_path)
    scss.LOAD_PATHS = ','.join(load_paths)


class CompassCompiler(CompilerBase):
  output_extension = 'css'

  def match_file(self, filename):
    return filename.endswith('.scss')

  def compile_file(self, infile, outfile, outdated=False, force=False):
    if not outdated and not force:
        return # No need to recompiled file
    incode = open(infile).read()
    #Add the inpath to scss
    scss.LOAD_PATHS += (',' + infile[:infile.rindex('/')])
    compiled = scss.Scss().compile(incode)
    if outfile:
        fout=open(outfile,'w')
        fout.write(compiled)
        fout.close()
    return compiled
