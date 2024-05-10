import hgext.convert.convcmd

from hgext.convert.hg import mercurial_source as basesource
#from hgext.convert.subversion import svn_source as basesource # to use subversion as source

import logging
import sys

logging.basicConfig(
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    style='%',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class customsource(basesource):

    def getchanges(self, version, full):
        # returns (filename, rev) list and target, source dictionary
        # files not included in the list is just ignored
        files, copies, cleanp2 = super(customsource, self).getchanges(version, full)
        logger.debug("files = {}".format(files,))
        files_new = []
        files_append = files_new.append
        for x in files:
            if x[0] == b'.hgsub':
                logger.info("Skipping {}".format(x,))
            else:
                files_append(x)
            # End If
        # Next (x)
        return files_new, copies, cleanp2

    def getcommit(self, rev):
        # returns meta data for changeset rev
        c = super(customsource, self).getcommit(rev)
        logger.debug("commit = {}".format(c.__dict__,))
        return c
    # End Def (getcommit)

# End Class (customsource)


logger.debug(sys.version)

hgext.convert.convcmd.source_converters.append((b'customsource', customsource, b'branchsort'))
